#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量配置生成器
支持批量处理多个订阅链接
"""

import os
import sys
import json
import argparse
from typing import List, Dict
from openclash_generator import OpenClashGenerator

class BatchGenerator:
    def __init__(self):
        self.generator = OpenClashGenerator()
        
    def process_batch(self, config_file: str, output_dir: str = "output"):
        """
        批量处理配置文件
        
        Args:
            config_file: 批量配置文件路径
            output_dir: 输出目录
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.endswith('.json'):
                configs = json.load(f)
            else:
                # 简单文本格式，每行一个订阅链接
                lines = f.read().strip().split('\n')
                configs = []
                for i, line in enumerate(lines):
                    if line.strip():
                        configs.append({
                            'name': f'config_{i+1}',
                            'url': line.strip(),
                            'template': 'enhanced'
                        })
        
        print(f"📋 找到 {len(configs)} 个配置任务")
        
        success_count = 0
        failed_configs = []
        
        for i, config in enumerate(configs, 1):
            name = config.get('name', f'config_{i}')
            url = config.get('url', '')
            template = config.get('template', 'enhanced')
            
            print(f"\n🔄 处理配置 {i}/{len(configs)}: {name}")
            
            if not url:
                print(f"❌ 跳过 {name}: 缺少订阅链接")
                failed_configs.append({'name': name, 'error': '缺少订阅链接'})
                continue
                
            try:
                output_file = os.path.join(output_dir, f"{name}.yaml")
                result = self.generator.generate_config(url, template, output_file)
                
                if result:
                    print(f"✅ {name} 生成成功: {output_file}")
                    success_count += 1
                else:
                    print(f"❌ {name} 生成失败")
                    failed_configs.append({'name': name, 'error': '生成失败'})
                    
            except Exception as e:
                print(f"❌ {name} 生成失败: {str(e)}")
                failed_configs.append({'name': name, 'error': str(e)})
        
        # 输出统计信息
        print(f"\n📊 批量处理完成:")
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {len(failed_configs)}")
        
        if failed_configs:
            print(f"\n❌ 失败的配置:")
            for config in failed_configs:
                print(f"  - {config['name']}: {config['error']}")
                
        # 生成报告
        report_file = os.path.join(output_dir, "batch_report.json")
        report = {
            'total': len(configs),
            'success': success_count,
            'failed': len(failed_configs),
            'failed_configs': failed_configs
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"📄 报告已保存: {report_file}")

def create_sample_config():
    """创建示例配置文件"""
    sample_config = [
        {
            "name": "config_1",
            "url": "https://example.com/subscription1",
            "template": "enhanced"
        },
        {
            "name": "config_2", 
            "url": "https://example.com/subscription2",
            "template": "gaming"
        },
        {
            "name": "config_3",
            "url": "https://example.com/subscription3", 
            "template": "streaming"
        }
    ]
    
    with open('batch_config_sample.json', 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
        
    print("📝 示例配置文件已创建: batch_config_sample.json")

def main():
    parser = argparse.ArgumentParser(description='OpenClash 批量配置生成器')
    parser.add_argument('--config', '-c', help='批量配置文件路径')
    parser.add_argument('--output', '-o', default='output', help='输出目录')
    parser.add_argument('--sample', action='store_true', help='创建示例配置文件')
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_config()
        return
        
    if not args.config:
        print("❌ 请指定配置文件路径")
        print("💡 使用 --sample 创建示例配置文件")
        return
        
    if not os.path.exists(args.config):
        print(f"❌ 配置文件不存在: {args.config}")
        return
        
    batch_generator = BatchGenerator()
    batch_generator.process_batch(args.config, args.output)

if __name__ == "__main__":
    main()