#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
格式转换器
将解析的节点转换为 Clash 格式
"""

import re
from typing import List, Dict, Any

class ConfigConverter:
    def __init__(self):
        self.country_mapping = {
            # 中文地区映射
            '香港': '🇭🇰 香港',
            '台湾': '🇹🇼 台湾',
            '日本': '🇯🇵 日本',
            '韩国': '🇰🇷 韩国',
            '新加坡': '🇸🇬 新加坡',
            '美国': '🇺🇸 美国',
            '加拿大': '🇨🇦 加拿大',
            '英国': '🇬🇧 英国',
            '德国': '🇩🇪 德国',
            '法国': '🇫🇷 法国',
            '荷兰': '🇳🇱 荷兰',
            '俄罗斯': '🇷🇺 俄罗斯',
            '土耳其': '🇹🇷 土耳其',
            '印度': '🇮🇳 印度',
            '澳大利亚': '🇦🇺 澳大利亚',
            # 英文地区映射
            'hong kong': '🇭🇰 香港',
            'hk': '🇭🇰 香港',
            'taiwan': '🇹🇼 台湾',
            'tw': '🇹🇼 台湾',
            'japan': '🇯🇵 日本',
            'jp': '🇯🇵 日本',
            'korea': '🇰🇷 韩国',
            'kr': '🇰🇷 韩国',
            'singapore': '🇸🇬 新加坡',
            'sg': '🇸🇬 新加坡',
            'united states': '🇺🇸 美国',
            'usa': '🇺🇸 美国',
            'us': '🇺🇸 美国',
            'canada': '🇨🇦 加拿大',
            'ca': '🇨🇦 加拿大',
            'united kingdom': '🇬🇧 英国',
            'uk': '🇬🇧 英国',
            'germany': '🇩🇪 德国',
            'de': '🇩🇪 德国',
            'france': '🇫🇷 法国',
            'fr': '🇫🇷 法国',
            'netherlands': '🇳🇱 荷兰',
            'nl': '🇳🇱 荷兰',
            'russia': '🇷🇺 俄罗斯',
            'ru': '🇷🇺 俄罗斯',
            'turkey': '🇹🇷 土耳其',
            'tr': '🇹🇷 土耳其',
            'india': '🇮🇳 印度',
            'in': '🇮🇳 印度',
            'australia': '🇦🇺 澳大利亚',
            'au': '🇦🇺 澳大利亚',
        }
        
    def convert_nodes(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        转换节点格式为 Clash 兼容格式
        
        Args:
            nodes: 原始节点列表
            
        Returns:
            转换后的节点列表
        """
        converted_nodes = []
        
        for i, node in enumerate(nodes):
            try:
                converted_node = self._convert_single_node(node, i)
                if converted_node:
                    converted_nodes.append(converted_node)
            except Exception as e:
                print(f"转换节点失败: {node.get('name', 'Unknown')} - {str(e)}")
                continue
                
        return converted_nodes
        
    def _convert_single_node(self, node: Dict[str, Any], index: int) -> Dict[str, Any]:
        """转换单个节点"""
        # 基础字段验证
        if not node.get('server') or not node.get('port'):
            return None
            
        # 清理和优化节点名称
        name = self._clean_node_name(node.get('name', f'节点{index+1}'))
        
        # 基础节点信息
        converted_node = {
            'name': name,
            'type': node['type'],
            'server': node['server'],
            'port': int(node['port']),
            'udp': node.get('udp', True)
        }
        
        # 根据协议类型添加特定字段
        if node['type'] == 'vmess':
            converted_node.update({
                'uuid': node['uuid'],
                'alterId': node.get('alterId', 0),
                'cipher': node.get('cipher', 'auto')
            })
            
            # TLS 配置
            if node.get('tls'):
                converted_node['tls'] = True
                converted_node['skip-cert-verify'] = node.get('skip-cert-verify', False)
                if node.get('servername'):
                    converted_node['servername'] = node['servername']
                    
            # 传输协议配置
            if node.get('network'):
                converted_node['network'] = node['network']
                if node['network'] == 'ws' and node.get('ws-opts'):
                    converted_node['ws-opts'] = node['ws-opts']
                elif node['network'] == 'grpc' and node.get('grpc-opts'):
                    converted_node['grpc-opts'] = node['grpc-opts']
                    
        elif node['type'] == 'ss':
            converted_node.update({
                'cipher': node['cipher'],
                'password': node['password']
            })
            
        elif node['type'] == 'trojan':
            converted_node.update({
                'password': node['password'],
                'skip-cert-verify': node.get('skip-cert-verify', False)
            })
            
            if node.get('sni'):
                converted_node['sni'] = node['sni']
                
            if node.get('network'):
                converted_node['network'] = node['network']
                if node['network'] == 'ws' and node.get('ws-opts'):
                    converted_node['ws-opts'] = node['ws-opts']
                    
        elif node['type'] == 'vless':
            converted_node.update({
                'uuid': node['uuid'],
                'flow': node.get('flow', ''),
                'skip-cert-verify': node.get('skip-cert-verify', False)
            })
            
            if node.get('tls'):
                converted_node['tls'] = True
                if node.get('servername'):
                    converted_node['servername'] = node['servername']
                    
            if node.get('network'):
                converted_node['network'] = node['network']
                if node['network'] == 'ws' and node.get('ws-opts'):
                    converted_node['ws-opts'] = node['ws-opts']
                elif node['network'] == 'grpc' and node.get('grpc-opts'):
                    converted_node['grpc-opts'] = node['grpc-opts']
                    
        return converted_node
        
    def _clean_node_name(self, name: str) -> str:
        """清理节点名称"""
        # 移除特殊字符
        name = re.sub(r'[^\w\s\-\u4e00-\u9fff🇦-🇿]', '', name)
        
        # 添加地区标识
        name_lower = name.lower()
        for region, flag in self.country_mapping.items():
            if region in name_lower:
                if not name.startswith('🇦') and not name.startswith('🇧'):  # 如果没有旗帜
                    name = f"{flag} {name}"
                break
                
        return name.strip()
        
    def group_nodes_by_region(self, nodes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """按地区分组节点"""
        groups = {
            '🇭🇰 香港节点': [],
            '🇹🇼 台湾节点': [],
            '🇯🇵 日本节点': [],
            '🇰🇷 韩国节点': [],
            '🇸🇬 新加坡节点': [],
            '🇺🇸 美国节点': [],
            '🇬🇧 英国节点': [],
            '🌍 其他节点': []
        }
        
        for node in nodes:
            name = node['name'].lower()
            assigned = False
            
            if '香港' in name or 'hk' in name or '🇭🇰' in node['name']:
                groups['🇭🇰 香港节点'].append(node['name'])
                assigned = True
            elif '台湾' in name or 'tw' in name or '🇹🇼' in node['name']:
                groups['🇹🇼 台湾节点'].append(node['name'])
                assigned = True
            elif '日本' in name or 'jp' in name or '🇯🇵' in node['name']:
                groups['🇯🇵 日本节点'].append(node['name'])
                assigned = True
            elif '韩国' in name or 'kr' in name or '🇰🇷' in node['name']:
                groups['🇰🇷 韩国节点'].append(node['name'])
                assigned = True
            elif '新加坡' in name or 'sg' in name or '🇸🇬' in node['name']:
                groups['🇸🇬 新加坡节点'].append(node['name'])
                assigned = True
            elif '美国' in name or 'us' in name or '🇺🇸' in node['name']:
                groups['🇺🇸 美国节点'].append(node['name'])
                assigned = True
            elif '英国' in name or 'uk' in name or '🇬🇧' in node['name']:
                groups['🇬🇧 英国节点'].append(node['name'])
                assigned = True
                
            if not assigned:
                groups['🌍 其他节点'].append(node['name'])
                
        # 移除空组
        return {k: v for k, v in groups.items() if v}