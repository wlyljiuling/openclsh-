#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClash 配置生成器 Web 界面
提供简单易用的网页界面
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import threading
import time
from openclash_generator import OpenClashGenerator

app = Flask(__name__)
app.secret_key = 'openclash_generator_secret_key'

# 全局变量存储生成状态
generation_status = {}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_config():
    """生成配置文件API"""
    try:
        data = request.get_json()
        subscription_url = data.get('subscription_url', '').strip()
        template = data.get('template', 'enhanced')
        
        if not subscription_url:
            return jsonify({'success': False, 'error': '订阅链接不能为空'})
        
        # 生成唯一任务ID
        task_id = str(int(time.time() * 1000))
        generation_status[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': '开始生成配置文件...'
        }
        
        # 在后台线程中生成配置
        thread = threading.Thread(
            target=generate_config_async,
            args=(task_id, subscription_url, template)
        )
        thread.start()
        
        return jsonify({'success': True, 'task_id': task_id})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generate_config_async(task_id, subscription_url, template):
    """异步生成配置文件"""
    try:
        generator = OpenClashGenerator()
        
        # 更新状态
        generation_status[task_id].update({
            'progress': 20,
            'message': '正在获取订阅数据...'
        })
        
        # 生成配置文件
        output_file = f"temp_config_{task_id}.yaml"
        result = generator.generate_config(subscription_url, template, output_file)
        
        if result:
            generation_status[task_id].update({
                'status': 'completed',
                'progress': 100,
                'message': '配置文件生成成功！',
                'file_path': result
            })
        else:
            generation_status[task_id].update({
                'status': 'failed',
                'progress': 0,
                'message': '配置文件生成失败'
            })
            
    except Exception as e:
        generation_status[task_id].update({
            'status': 'failed',
            'progress': 0,
            'message': f'生成失败: {str(e)}'
        })

@app.route('/api/status/<task_id>')
def get_status(task_id):
    """获取生成状态"""
    status = generation_status.get(task_id, {
        'status': 'not_found',
        'message': '任务不存在'
    })
    return jsonify(status)

@app.route('/api/download/<task_id>')
def download_config(task_id):
    """下载配置文件"""
    status = generation_status.get(task_id)
    if not status or status.get('status') != 'completed':
        return jsonify({'error': '文件不存在或未完成'}), 404
        
    file_path = status.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
        
    return send_file(
        file_path,
        as_attachment=True,
        download_name='openclash_config.yaml',
        mimetype='application/x-yaml'
    )

@app.route('/api/templates')
def get_templates():
    """获取可用模板列表"""
    templates = [
        {
            'id': 'basic',
            'name': '基础模板',
            'description': '包含基本的代理分组和规则，适合简单使用'
        },
        {
            'id': 'enhanced',
            'name': '增强模板',
            'description': '包含广告拦截、DNS优化等功能，推荐使用'
        },
        {
            'id': 'gaming',
            'name': '游戏模板',
            'description': '针对游戏优化，包含Steam、Epic等游戏平台规则'
        },
        {
            'id': 'streaming',
            'name': '流媒体模板',
            'description': '针对Netflix、YouTube等流媒体平台优化'
        }
    ]
    return jsonify(templates)

def cleanup_old_files():
    """清理旧的临时文件"""
    while True:
        try:
            current_time = time.time()
            for task_id in list(generation_status.keys()):
                # 删除1小时前的任务记录和文件
                if current_time - int(task_id) / 1000 > 3600:
                    status = generation_status.get(task_id)
                    if status and status.get('file_path'):
                        file_path = status['file_path']
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    del generation_status[task_id]
        except:
            pass
        time.sleep(300)  # 每5分钟清理一次

if __name__ == '__main__':
    # 启动清理线程
    cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
    cleanup_thread.start()
    
    print("🌐 OpenClash 配置生成器 Web 界面")
    print("🚀 启动服务器...")
    print("📱 访问地址: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止服务")
    
    app.run(host='0.0.0.0', port=5000, debug=False)