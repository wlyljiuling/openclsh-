#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置验证器
验证生成的配置文件是否正确
"""

import yaml
from typing import Dict, Any, List

class ConfigValidator:
    def __init__(self):
        self.required_fields = {
            'port': int,
            'socks-port': int,
            'allow-lan': bool,
            'mode': str,
            'log-level': str,
            'proxies': list,
            'proxy-groups': list,
            'rules': list
        }
        
        self.proxy_required_fields = {
            'vmess': ['name', 'type', 'server', 'port', 'uuid'],
            'ss': ['name', 'type', 'server', 'port', 'cipher', 'password'],
            'trojan': ['name', 'type', 'server', 'port', 'password'],
            'vless': ['name', 'type', 'server', 'port', 'uuid']
        }
        
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置文件
        
        Args:
            config: 配置字典
            
        Returns:
            验证是否通过
        """
        try:
            # 验证基础字段
            if not self._validate_basic_fields(config):
                return False
                
            # 验证代理节点
            if not self._validate_proxies(config.get('proxies', [])):
                return False
                
            # 验证代理组
            if not self._validate_proxy_groups(config.get('proxy-groups', [])):
                return False
                
            # 验证规则
            if not self._validate_rules(config.get('rules', [])):
                return False
                
            print("✅ 配置文件验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置验证失败: {str(e)}")
            return False
            
    def _validate_basic_fields(self, config: Dict[str, Any]) -> bool:
        """验证基础字段"""
        for field, field_type in self.required_fields.items():
            if field not in config:
                print(f"❌ 缺少必需字段: {field}")
                return False
                
            if not isinstance(config[field], field_type):
                print(f"❌ 字段类型错误: {field} 应为 {field_type.__name__}")
                return False
                
        return True
        
    def _validate_proxies(self, proxies: List[Dict[str, Any]]) -> bool:
        """验证代理节点"""
        if not proxies:
            print("❌ 没有代理节点")
            return False
            
        for i, proxy in enumerate(proxies):
            if not isinstance(proxy, dict):
                print(f"❌ 代理节点 {i} 格式错误")
                return False
                
            proxy_type = proxy.get('type')
            if proxy_type not in self.proxy_required_fields:
                print(f"❌ 不支持的代理类型: {proxy_type}")
                return False
                
            # 验证必需字段
            required_fields = self.proxy_required_fields[proxy_type]
            for field in required_fields:
                if field not in proxy:
                    print(f"❌ 代理节点 {proxy.get('name', i)} 缺少字段: {field}")
                    return False
                    
            # 验证端口范围
            port = proxy.get('port')
            if not isinstance(port, int) or port < 1 or port > 65535:
                print(f"❌ 代理节点 {proxy.get('name', i)} 端口无效: {port}")
                return False
                
        return True
        
    def _validate_proxy_groups(self, proxy_groups: List[Dict[str, Any]]) -> bool:
        """验证代理组"""
        if not proxy_groups:
            print("❌ 没有代理组")
            return False
            
        required_group_fields = ['name', 'type', 'proxies']
        
        for i, group in enumerate(proxy_groups):
            if not isinstance(group, dict):
                print(f"❌ 代理组 {i} 格式错误")
                return False
                
            for field in required_group_fields:
                if field not in group:
                    print(f"❌ 代理组 {group.get('name', i)} 缺少字段: {field}")
                    return False
                    
            if not isinstance(group['proxies'], list) or not group['proxies']:
                print(f"❌ 代理组 {group['name']} 没有代理节点")
                return False
                
        return True
        
    def _validate_rules(self, rules: List[str]) -> bool:
        """验证规则"""
        if not rules:
            print("⚠️ 没有规则，将使用默认规则")
            return True
            
        valid_rule_types = [
            'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD',
            'IP-CIDR', 'IP-CIDR6', 'GEOIP', 'MATCH',
            'PROCESS-NAME', 'RULE-SET'
        ]
        
        for i, rule in enumerate(rules):
            if not isinstance(rule, str):
                print(f"❌ 规则 {i} 格式错误")
                return False
                
            parts = rule.split(',')
            if len(parts) < 2:
                print(f"❌ 规则 {i} 格式错误: {rule}")
                return False
                
            rule_type = parts[0]
            if rule_type not in valid_rule_types:
                print(f"⚠️ 未知规则类型: {rule_type}")
                
        return True
        
    def validate_yaml_syntax(self, yaml_content: str) -> bool:
        """验证 YAML 语法"""
        try:
            yaml.safe_load(yaml_content)
            return True
        except yaml.YAMLError as e:
            print(f"❌ YAML 语法错误: {str(e)}")
            return False