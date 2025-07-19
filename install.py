#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClash 配置生成器安装脚本
自动安装依赖和设置环境
"""

import os
import sys
import subprocess
import platform

def run_command(command, description=""):
    """运行命令并处理错误"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 需要 Python 3.7 或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python 版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    
    # 升级pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级 pip")
    
    # 安装依赖
    if os.path.exists('requirements.txt'):
        return run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装依赖包")
    else:
        # 手动安装主要依赖
        packages = [
            'requests>=2.28.0',
            'pyyaml>=6.0',
            'flask>=2.0.0',
            'click>=8.0.0',
            'colorama>=0.4.0',
            'tqdm>=4.64.0'
        ]
        
        for package in packages:
            if not run_command(f"{sys.executable} -m pip install {package}", f"安装 {package}"):
                return False
        return True

def create_shortcuts():
    """创建快捷方式"""
    system = platform.system()
    
    if system == "Windows":
        # Windows 批处理文件
        with open('start_web.bat', 'w', encoding='utf-8') as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{os.getcwd()}"\n')
            f.write(f'"{sys.executable}" web_interface.py\n')
            f.write(f'pause\n')
        
        with open('generate_config.bat', 'w', encoding='utf-8') as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{os.getcwd()}"\n')
            f.write(f'"{sys.executable}" openclash_generator.py --interactive\n')
            f.write(f'pause\n')
            
        print("✅ 已创建 Windows 快捷方式:")
        print("  - start_web.bat (启动Web界面)")
        print("  - generate_config.bat (命令行生成)")
        
    else:
        # Unix/Linux shell 脚本
        with open('start_web.sh', 'w') as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'cd "{os.getcwd()}"\n')
            f.write(f'"{sys.executable}" web_interface.py\n')
        
        with open('generate_config.sh', 'w') as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'cd "{os.getcwd()}"\n')
            f.write(f'"{sys.executable}" openclash_generator.py --interactive\n')
            
        # 添加执行权限
        os.chmod('start_web.sh', 0o755)
        os.chmod('generate_config.sh', 0o755)
        
        print("✅ 已创建 Unix/Linux 快捷方式:")
        print("  - start_web.sh (启动Web界面)")
        print("  - generate_config.sh (命令行生成)")

def main():
    print("🚀 OpenClash 配置生成器安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败")
        sys.exit(1)
    
    # 创建快捷方式
    create_shortcuts()
    
    print("\n🎉 安装完成!")
    print("\n📖 使用方法:")
    print("1. Web界面: 运行 start_web.* 文件")
    print("2. 命令行: 运行 generate_config.* 文件")
    print("3. 直接运行: python openclash_generator.py --interactive")
    print("4. 批量处理: python batch_generator.py --config config.json")
    
    print("\n💡 提示:")
    print("- 首次使用建议选择 Web 界面")
    print("- 配置模板位于 config/ 目录")
    print("- 生成的配置文件可直接导入 OpenClash")

if __name__ == "__main__":
    main()