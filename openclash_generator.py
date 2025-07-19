#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClash 配置文件生成器
支持多种订阅格式，自动生成完美的 OpenClash 配置
"""

import os
import sys
import json
import yaml
import base64
import requests
import argparse
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Any, Optional
import re
from utils.parser import SubscriptionParser
from utils.converter import ConfigConverter
from utils.validator import ConfigValidator

class OpenClashGenerator:
    def __init__(self):
        self.parser = SubscriptionParser()
        self.converter = ConfigConverter()
        self.validator = ConfigValidator()
        
    def generate_config(self, subscription_url: str, template: str = "enhanced", output_file: str = None) -> str:
        """
        生成 OpenClash 配置文件
        
        Args:
            subscription_url: 订阅链接
            template: 配置模板类型
            output_file: 输出文件路径
            
        Returns:
            生成的配置文件路径
        """
        print("🚀 开始生成 OpenClash 配置文件...")
        
        # 1. 解析订阅链接
        print("📡 正在获取订阅数据...")
        nodes = self.parser.parse_subscription(subscription_url)
        print(f"✅ 成功解析 {len(nodes)} 个节点")
        
        # 2. 加载配置模板
        print(f"📋 加载配置模板: {template}")
        template_config = self._load_template(template)
        
        # 3. 转换节点格式
        print("🔄 转换节点格式...")
        clash_nodes = self.converter.convert_nodes(nodes)
        
        # 4. 生成完整配置
        print("⚙️ 生成完整配置...")
        config = self._build_config(template_config, clash_nodes)
        
        # 5. 验证配置
        print("🔍 验证配置文件...")
        if self.validator.validate_config(config):
            print("✅ 配置文件验证通过")
        else:
            print("❌ 配置文件验证失败")
            return None
            
        # 6. 保存配置文件
        if not output_file:
            output_file = "openclash_config.yaml"
            
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
        print(f"🎉 配置文件已生成: {output_file}")
        return output_file
        
    def _load_template(self, template_name: str) -> Dict[str, Any]:
        """加载配置模板"""
        template_file = f"config/{template_name}_template.yaml"
        if not os.path.exists(template_file):
            template_file = "config/enhanced_template.yaml"
            
        with open(template_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
            
    def _build_config(self, template: Dict[str, Any], nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """构建完整配置"""
        config = template.copy()
        
        # 添加节点
        config['proxies'] = nodes
        
        # 更新代理组
        node_names = [node['name'] for node in nodes]
        self._update_proxy_groups(config, node_names)
        
        return config
        
    def _update_proxy_groups(self, config: Dict[str, Any], node_names: List[str]):
        """更新代理组"""
        if 'proxy-groups' not in config:
            return
            
        for group in config['proxy-groups']:
            if group['name'] == '🚀 节点选择':
                # 添加所有节点到节点选择组
                group['proxies'] = ['♻️ 自动选择', 'DIRECT'] + node_names
            elif group['name'] == '♻️ 自动选择':
                # 添加所有节点到自动选择组
                group['proxies'] = node_names
            elif group['name'] == '🐟 漏网之鱼':
                # 添加所有节点到漏网之鱼组
                group['proxies'] = ['🚀 节点选择', '🎯 全球直连', '♻️ 自动选择'] + node_names

def main():
    parser = argparse.ArgumentParser(description='OpenClash 配置文件生成器')
    parser.add_argument('--url', '-u', help='订阅链接')
    parser.add_argument('--template', '-t', default='enhanced', help='配置模板 (basic/enhanced/gaming/streaming)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式模式')
    
    args = parser.parse_args()
    
    generator = OpenClashGenerator()
    
    if args.interactive or not args.url:
        # 交互式模式
        print("🎯 OpenClash 配置文件生成器")
        print("=" * 50)
        
        subscription_url = input("请输入订阅链接: ").strip()
        if not subscription_url:
            print("❌ 订阅链接不能为空")
            return
            
        print("\n可用模板:")
        print("1. basic - 基础模板")
        print("2. enhanced - 增强模板 (推荐)")
        print("3. gaming - 游戏模板")
        print("4. streaming - 流媒体模板")
        
        template_choice = input("请选择模板 (默认: enhanced): ").strip()
        template_map = {
            '1': 'basic',
            '2': 'enhanced',
            '3': 'gaming',
            '4': 'streaming'
        }
        template = template_map.get(template_choice, 'enhanced')
        
        output_file = input("输出文件名 (默认: openclash_config.yaml): ").strip()
        if not output_file:
            output_file = "openclash_config.yaml"
            
    else:
        subscription_url = args.url
        template = args.template
        output_file = args.output
        
    try:
        result = generator.generate_config(subscription_url, template, output_file)
        if result:
            print(f"\n🎉 配置文件生成成功!")
            print(f"📁 文件位置: {os.path.abspath(result)}")
            print("\n📖 使用说明:")
            print("1. 将生成的配置文件上传到 OpenClash")
            print("2. 在 OpenClash 管理界面导入配置")
            print("3. 启动 OpenClash 服务")
        else:
            print("❌ 配置文件生成失败")
            
    except Exception as e:
        print(f"❌ 生成过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()