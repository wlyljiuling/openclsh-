#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
订阅解析器
支持多种订阅格式的解析
"""

import base64
import json
import re
import requests
import yaml
from urllib.parse import urlparse, parse_qs, unquote
from typing import List, Dict, Any, Optional

class SubscriptionParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ClashforWindows/0.20.39'
        })
        
    def parse_subscription(self, url: str) -> List[Dict[str, Any]]:
        """
        解析订阅链接
        
        Args:
            url: 订阅链接
            
        Returns:
            节点列表
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            content = response.text
            
            # 尝试不同的解析方式
            nodes = []
            
            # 1. 尝试解析为 Clash 格式
            try:
                clash_config = yaml.safe_load(content)
                if isinstance(clash_config, dict) and 'proxies' in clash_config:
                    return clash_config['proxies']
            except:
                pass
                
            # 2. 尝试解析为 Base64 编码的节点列表
            try:
                decoded_content = base64.b64decode(content).decode('utf-8')
                nodes.extend(self._parse_node_list(decoded_content))
            except:
                # 3. 直接解析节点列表
                nodes.extend(self._parse_node_list(content))
                
            return nodes
            
        except Exception as e:
            print(f"解析订阅失败: {str(e)}")
            return []
            
    def _parse_node_list(self, content: str) -> List[Dict[str, Any]]:
        """解析节点列表"""
        nodes = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            try:
                # 解析不同协议的节点
                if line.startswith('vmess://'):
                    node = self._parse_vmess(line)
                elif line.startswith('ss://'):
                    node = self._parse_shadowsocks(line)
                elif line.startswith('trojan://'):
                    node = self._parse_trojan(line)
                elif line.startswith('vless://'):
                    node = self._parse_vless(line)
                else:
                    continue
                    
                if node:
                    nodes.append(node)
                    
            except Exception as e:
                print(f"解析节点失败: {line[:50]}... - {str(e)}")
                continue
                
        return nodes
        
    def _parse_vmess(self, vmess_url: str) -> Optional[Dict[str, Any]]:
        """解析 VMess 节点"""
        try:
            # 移除 vmess:// 前缀
            encoded_data = vmess_url[8:]
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
            
            # 处理 TLS
            if vmess_data.get('tls') == 'tls':
                node['tls'] = True
                node['skip-cert-verify'] = False
                if vmess_data.get('sni'):
                    node['servername'] = vmess_data.get('sni')
                    
            # 处理传输协议
            network = vmess_data.get('net', 'tcp')
            if network == 'ws':
                node['network'] = 'ws'
                node['ws-opts'] = {
                    'path': vmess_data.get('path', '/'),
                    'headers': {}
                }
                if vmess_data.get('host'):
                    node['ws-opts']['headers']['Host'] = vmess_data.get('host')
            elif network == 'grpc':
                node['network'] = 'grpc'
                node['grpc-opts'] = {
                    'grpc-service-name': vmess_data.get('path', '')
                }
                
            return node
            
        except Exception as e:
            print(f"解析 VMess 节点失败: {str(e)}")
            return None
            
    def _parse_shadowsocks(self, ss_url: str) -> Optional[Dict[str, Any]]:
        """解析 Shadowsocks 节点"""
        try:
            # 解析 ss:// 格式
            url_parts = urlparse(ss_url)
            
            # 解码用户信息
            if '@' in url_parts.netloc:
                auth_part, server_part = url_parts.netloc.split('@')
                try:
                    decoded_auth = base64.b64decode(auth_part).decode('utf-8')
                    method, password = decoded_auth.split(':', 1)
                except:
                    # 如果不是 base64 编码，直接分割
                    method, password = auth_part.split(':', 1)
            else:
                # 整个 netloc 是 base64 编码的
                decoded_netloc = base64.b64decode(url_parts.netloc).decode('utf-8')
                auth_part, server_part = decoded_netloc.split('@')
                method, password = auth_part.split(':', 1)
                
            server, port = server_part.split(':')
            
            # 获取节点名称
            query_params = parse_qs(url_parts.query)
            name = unquote(url_parts.fragment) if url_parts.fragment else 'SS节点'
            
            node = {
                'name': name,
                'type': 'ss',
                'server': server,
                'port': int(port),
                'cipher': method,
                'password': password,
                'udp': True
            }
            
            return node
            
        except Exception as e:
            print(f"解析 Shadowsocks 节点失败: {str(e)}")
            return None
            
    def _parse_trojan(self, trojan_url: str) -> Optional[Dict[str, Any]]:
        """解析 Trojan 节点"""
        try:
            url_parts = urlparse(trojan_url)
            
            node = {
                'name': unquote(url_parts.fragment) if url_parts.fragment else 'Trojan节点',
                'type': 'trojan',
                'server': url_parts.hostname,
                'port': url_parts.port or 443,
                'password': url_parts.username,
                'udp': True,
                'skip-cert-verify': False
            }
            
            # 解析查询参数
            query_params = parse_qs(url_parts.query)
            
            if 'sni' in query_params:
                node['sni'] = query_params['sni'][0]
                
            if 'type' in query_params and query_params['type'][0] == 'ws':
                node['network'] = 'ws'
                node['ws-opts'] = {
                    'path': query_params.get('path', ['/'])[0],
                    'headers': {}
                }
                if 'host' in query_params:
                    node['ws-opts']['headers']['Host'] = query_params['host'][0]
                    
            return node
            
        except Exception as e:
            print(f"解析 Trojan 节点失败: {str(e)}")
            return None
            
    def _parse_vless(self, vless_url: str) -> Optional[Dict[str, Any]]:
        """解析 VLESS 节点"""
        try:
            url_parts = urlparse(vless_url)
            
            node = {
                'name': unquote(url_parts.fragment) if url_parts.fragment else 'VLESS节点',
                'type': 'vless',
                'server': url_parts.hostname,
                'port': url_parts.port or 443,
                'uuid': url_parts.username,
                'udp': True,
                'skip-cert-verify': False
            }
            
            # 解析查询参数
            query_params = parse_qs(url_parts.query)
            
            if 'security' in query_params and query_params['security'][0] == 'tls':
                node['tls'] = True
                if 'sni' in query_params:
                    node['servername'] = query_params['sni'][0]
                    
            if 'type' in query_params:
                network = query_params['type'][0]
                if network == 'ws':
                    node['network'] = 'ws'
                    node['ws-opts'] = {
                        'path': query_params.get('path', ['/'])[0],
                        'headers': {}
                    }
                    if 'host' in query_params:
                        node['ws-opts']['headers']['Host'] = query_params['host'][0]
                elif network == 'grpc':
                    node['network'] = 'grpc'
                    node['grpc-opts'] = {
                        'grpc-service-name': query_params.get('serviceName', [''])[0]
                    }
                    
            return node
            
        except Exception as e:
            print(f"解析 VLESS 节点失败: {str(e)}")
            return None