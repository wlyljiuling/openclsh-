#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版启动脚本
自动检测环境并启动项目
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_and_install_packages():
    """检查并安装必需的包"""
    required_packages = {
        'requests': 'requests',
        'yaml': 'pyyaml',
        'flask': 'flask'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            importlib.import_module(module)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n📦 正在安装缺失的包: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ 包安装完成")
        except subprocess.CalledProcessError:
            print("❌ 包安装失败，尝试使用国内镜像...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install',
                    '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple/'
                ] + missing_packages)
                print("✅ 包安装完成")
            except subprocess.CalledProcessError:
                print("❌ 包安装失败，请手动安装")
                return False
    
    return True

def create_simple_config():
    """创建简单的配置生成器"""
    import base64
    import json
    
    print("\n🚀 OpenClash 简单配置生成器")
    print("=" * 50)
    
    # 获取订阅链接
    subscription_url = input("请输入订阅链接: ").strip()
    if not subscription_url:
        print("❌ 订阅链接不能为空")
        return
    
    try:
        import requests
        
        print("📡 正在获取订阅数据...")
        response = requests.get(subscription_url, timeout=30)
        response.raise_for_status()
        
        content = response.text
        
        # 尝试解析为Base64
        try:
            decoded_content = base64.b64decode(content).decode('utf-8')
            content = decoded_content
        except:
            pass
        
        # 简单的配置模板
        config = {
            'port': 7890,
            'socks-port': 7891,
            'allow-lan': True,
            'mode': 'Rule',
            'log-level': 'info',
            'external-controller': '127.0.0.1:9090',
            'proxies': [],
            'proxy-groups': [
                {
                    'name': '🚀 节点选择',
                    'type': 'select',
                    'proxies': ['♻️ 自动选择', 'DIRECT']
                },
                {
                    'name': '♻️ 自动选择',
                    'type': 'url-test',
                    'url': 'http://www.gstatic.com/generate_204',
                    'interval': 300,
                    'proxies': []
                }
            ],
            'rules': [
                'DOMAIN-SUFFIX,local,DIRECT',
                'IP-CIDR,127.0.0.0/8,DIRECT',
                'IP-CIDR,172.16.0.0/12,DIRECT',
                'IP-CIDR,192.168.0.0/16,DIRECT',
                'IP-CIDR,10.0.0.0/8,DIRECT',
                'GEOIP,CN,DIRECT',
                'MATCH,🚀 节点选择'
            ]
        }
        
        # 解析节点（简化版）
        lines = content.strip().split('\n')
        node_names = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('vmess://'):
                try:
                    # 简单解析VMess
                    encoded_data = line[8:]
                    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
                    vmess_data = json.loads(decoded_data)
                    
                    node = {
                        'name': vmess_data.get('ps', 'VMess节点'),
                        'type': 'vmess',
                        'server': vmess_data.get('add'),
                        'port': int(vmess_data.get('port', 443)),
                        'uuid': vmess_data.get('id'),
                        'alterId': int(vmess_data.get('aid', 0)),
                        'cipher': 'auto',
                        'udp': True
                    }
                    
                    if vmess_data.get('tls') == 'tls':
                        node['tls'] = True
                        node['skip-cert-verify'] = False
                    
                    if vmess_data.get('net') == 'ws':
                        node['network'] = 'ws'
                        node['ws-opts'] = {
                            'path': vmess_data.get('path', '/'),
                            'headers': {}
                        }
                        if vmess_data.get('host'):
                            node['ws-opts']['headers']['Host'] = vmess_data.get('host')
                    
                    config['proxies'].append(node)
                    node_names.append(node['name'])
                    
                except Exception as e:
                    print(f"⚠️ 跳过无效节点: {str(e)}")
                    continue
        
        # 更新代理组
        if node_names:
            config['proxy-groups'][0]['proxies'].extend(node_names)
            config['proxy-groups'][1]['proxies'] = node_names
        
        # 保存配置
        import yaml
        output_file = 'openclash_config.yaml'
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ 配置文件已生成: {output_file}")
        print(f"📊 解析到 {len(node_names)} 个节点")
        print("\n📖 使用说明:")
        print("1. 将生成的配置文件上传到OpenClash")
        print("2. 在OpenClash管理界面导入配置")
        print("3. 启动OpenClash服务")
        
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")

def main():
    print("🚀 OpenClash 配置生成器")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        input("按回车键退出...")
        return
    
    # 检查并安装依赖
    if not check_and_install_packages():
        input("按回车键退出...")
        return
    
    # 检查是否有完整项目文件
    if os.path.exists('openclash_generator.py') and os.path.exists('web_interface.py'):
        print("\n✅ 检测到完整项目文件")
        choice = input("选择运行模式 (1-Web界面, 2-命令行, 3-简单模式): ").strip()
        
        if choice == '1':
            try:
                subprocess.run([sys.executable, 'web_interface.py'])
            except KeyboardInterrupt:
                print("\n👋 Web界面已停止")
        elif choice == '2':
            try:
                subprocess.run([sys.executable, 'openclash_generator.py', '--interactive'])
            except Exception as e:
                print(f"❌ 启动失败: {str(e)}")
        else:
            create_simple_config()
    else:
        print("\n⚠️ 未检测到完整项目文件，使用简单模式")
        create_simple_config()
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()