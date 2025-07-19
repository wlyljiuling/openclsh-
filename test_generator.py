#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本
验证配置生成器的功能
"""

import os
import sys
import yaml
from utils.parser import SubscriptionParser
from utils.converter import ConfigConverter
from utils.validator import ConfigValidator

def test_parser():
    """测试订阅解析器"""
    print("🧪 测试订阅解析器...")
    
    # 测试 VMess 节点解析
    vmess_url = "vmess://eyJ2IjoiMiIsInBzIjoi6K+V6K+V6IqC54K5IiwiYWRkIjoiZXhhbXBsZS5jb20iLCJwb3J0IjoiNDQzIiwiaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwYWIiLCJhaWQiOiIwIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSIsImhvc3QiOiJleGFtcGxlLmNvbSIsInBhdGgiOiIvIiwidGxzIjoidGxzIn0="
    
    parser = SubscriptionParser()
    try:
        node = parser._parse_vmess(vmess_url)
        if node:
            print("✅ VMess 解析测试通过")
        else:
            print("❌ VMess 解析测试失败")
    except Exception as e:
        print(f"❌ VMess 解析测试失败: {str(e)}")

def test_converter():
    """测试格式转换器"""
    print("🧪 测试格式转换器...")
    
    # 测试节点
    test_nodes = [
        {
            'name': '香港节点1',
            'type': 'vmess',
            'server': 'hk.example.com',
            'port': 443,
            'uuid': '12345678-1234-1234-1234-1234567890ab',
            'alterId': 0,
            'cipher': 'auto',
            'tls': True,
            'network': 'ws',
            'ws-opts': {
                'path': '/',
                'headers': {'Host': 'hk.example.com'}
            }
        }
    ]
    
    converter = ConfigConverter()
    try:
        converted_nodes = converter.convert_nodes(test_nodes)
        if converted_nodes and len(converted_nodes) == 1:
            print("✅ 节点转换测试通过")
        else:
            print("❌ 节点转换测试失败")
    except Exception as e:
        print(f"❌ 节点转换测试失败: {str(e)}")

def test_validator():
    """测试配置验证器"""
    print("🧪 测试配置验证器...")
    
    # 测试配置
    test_config = {
        'port': 7890,
        'socks-port': 7891,
        'allow-lan': True,
        'mode': 'Rule',
        'log-level': 'info',
        'proxies': [
            {
                'name': '测试节点',
                'type': 'vmess',
                'server': 'example.com',
                'port': 443,
                'uuid': '12345678-1234-1234-1234-1234567890ab'
            }
        ],
        'proxy-groups': [
            {
                'name': '🚀 节点选择',
                'type': 'select',
                'proxies': ['测试节点']
            }
        ],
        'rules': [
            'DOMAIN-SUFFIX,example.com,🚀 节点选择',
            'MATCH,DIRECT'
        ]
    }
    
    validator = ConfigValidator()
    try:
        if validator.validate_config(test_config):
            print("✅ 配置验证测试通过")
        else:
            print("❌ 配置验证测试失败")
    except Exception as e:
        print(f"❌ 配置验证测试失败: {str(e)}")

def test_template_loading():
    """测试模板加载"""
    print("🧪 测试模板加载...")
    
    templates = ['basic', 'enhanced', 'gaming', 'streaming']
    
    for template in templates:
        template_file = f"config/{template}_template.yaml"
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if config and isinstance(config, dict):
                    print(f"✅ {template} 模板加载成功")
                else:
                    print(f"❌ {template} 模板格式错误")
        except Exception as e:
            print(f"❌ {template} 模板加载失败: {str(e)}")

def test_yaml_syntax():
    """测试YAML语法"""
    print("🧪 测试YAML语法...")
    
    yaml_files = [
        'config/basic_template.yaml',
        'config/enhanced_template.yaml',
        'config/gaming_template.yaml',
        'config/streaming_template.yaml'
    ]
    
    for yaml_file in yaml_files:
        if os.path.exists(yaml_file):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                print(f"✅ {yaml_file} 语法正确")
            except yaml.YAMLError as e:
                print(f"❌ {yaml_file} 语法错误: {str(e)}")
        else:
            print(f"⚠️ {yaml_file} 文件不存在")

def main():
    print("🧪 OpenClash 配置生成器测试")
    print("=" * 50)
    
    # 运行所有测试
    test_parser()
    test_converter()
    test_validator()
    test_template_loading()
    test_yaml_syntax()
    
    print("\n📊 测试完成!")
    print("💡 如果所有测试都通过，说明项目配置正确")

if __name__ == "__main__":
    main()