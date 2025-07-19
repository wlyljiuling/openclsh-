#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClash 配置生成器启动脚本
提供统一的启动入口
"""

import os
import sys
import argparse
import subprocess

def start_web_interface():
    """启动Web界面"""
    print("🌐 启动 Web 界面...")
    try:
        subprocess.run([sys.executable, 'web_interface.py'])
    except KeyboardInterrupt:
        print("\n👋 Web 界面已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

def start_interactive():
    """启动交互式命令行"""
    print("💻 启动交互式命令行...")
    try:
        subprocess.run([sys.executable, 'openclash_generator.py', '--interactive'])
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

def start_batch():
    """启动批量处理"""
    print("📦 启动批量处理...")
    config_file = input("请输入配置文件路径: ").strip()
    if not config_file:
        print("❌ 配置文件路径不能为空")
        return
        
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return
        
    try:
        subprocess.run([sys.executable, 'batch_generator.py', '--config', config_file])
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    try:
        subprocess.run([sys.executable, 'test_generator.py'])
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def show_menu():
    """显示主菜单"""
    print("\n🚀 OpenClash 配置生成器")
    print("=" * 50)
    print("1. 启动 Web 界面 (推荐)")
    print("2. 交互式命令行")
    print("3. 批量处理")
    print("4. 运行测试")
    print("5. 退出")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='OpenClash 配置生成器启动脚本')
    parser.add_argument('--web', action='store_true', help='直接启动Web界面')
    parser.add_argument('--interactive', action='store_true', help='直接启动交互式命令行')
    parser.add_argument('--test', action='store_true', help='运行测试')
    
    args = parser.parse_args()
    
    if args.web:
        start_web_interface()
        return
    elif args.interactive:
        start_interactive()
        return
    elif args.test:
        run_tests()
        return
    
    # 显示菜单
    while True:
        show_menu()
        choice = input("请选择操作 (1-5): ").strip()
        
        if choice == '1':
            start_web_interface()
        elif choice == '2':
            start_interactive()
        elif choice == '3':
            start_batch()
        elif choice == '4':
            run_tests()
        elif choice == '5':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()