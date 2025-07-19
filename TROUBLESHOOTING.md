# 故障排除指南

## 🐍 Python 环境问题

### 问题1: 'python' 不是内部或外部命令

**症状：**
```
'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

**解决方案：**

#### 方案A: 重新安装Python
1. 访问 https://www.python.org/downloads/
2. 下载最新版本Python
3. 安装时**务必勾选** "Add Python to PATH"
4. 重启命令提示符

#### 方案B: 手动添加环境变量
1. 找到Python安装目录（通常在 `C:\Python311\` 或 `C:\Users\用户名\AppData\Local\Programs\Python\`）
2. 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
3. 在"系统变量"中找到"Path"，点击"编辑"
4. 添加Python安装目录和Scripts目录
5. 重启命令提示符

#### 方案C: 使用完整路径
```bash
C:\Python311\python.exe script.py
```

#### 方案D: 使用py命令
```bash
py script.py
py -3 script.py
```

### 问题2: Python版本过低

**症状：**
```
SyntaxError: invalid syntax
```

**解决方案：**
- 本项目需要Python 3.7+
- 升级到最新版本的Python

## 📦 依赖安装问题

### 问题3: pip 安装失败

**症状：**
```
ERROR: Could not install packages due to an EnvironmentError
```

**解决方案：**

#### 方案A: 升级pip
```bash
python -m pip install --upgrade pip
```

#### 方案B: 使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 方案C: 用户安装
```bash
pip install --user package_name
```

#### 方案D: 管理员权限
以管理员身份运行命令提示符

### 问题4: 网络连接问题

**症状：**
```
ReadTimeoutError: HTTPSConnectionPool
```

**解决方案：**
1. 检查网络连接
2. 使用代理：
   ```bash
   pip install --proxy http://proxy:port package_name
   ```
3. 使用国内镜像源

## 🌐 Web界面问题

### 问题5: 端口被占用

**症状：**
```
OSError: [WinError 10048] 通常每个套接字地址只允许使用一次
```

**解决方案：**

#### 方案A: 查找并关闭占用进程
```bash
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F
```

#### 方案B: 使用其他端口
修改 `web_interface.py` 中的端口号，或者：
```bash
python web_interface.py --port 8080
```

### 问题6: 无法访问Web界面

**症状：**
浏览器显示"无法访问此网站"

**解决方案：**
1. 确认服务已启动
2. 检查防火墙设置
3. 尝试使用 `127.0.0.1:5000` 而不是 `localhost:5000`
4. 检查浏览器代理设置

## 🔧 配置生成问题

### 问题7: 订阅解析失败

**症状：**
```
解析订阅失败: HTTP Error 403
```

**解决方案：**
1. 检查订阅链接是否正确
2. 确认订阅链接未过期
3. 尝试在浏览器中直接访问订阅链接
4. 联系订阅提供商

### 问题8: 节点解析错误

**症状：**
```
解析节点失败: Invalid base64 encoding
```

**解决方案：**
1. 确认订阅格式正确
2. 检查是否为支持的协议类型
3. 尝试使用其他订阅链接

### 问题9: 配置验证失败

**症状：**
```
配置文件验证失败: 缺少必需字段
```

**解决方案：**
1. 检查订阅中的节点信息是否完整
2. 尝试使用不同的配置模板
3. 手动检查生成的配置文件

## 📱 移动设备访问问题

### 问题10: 手机无法访问Web界面

**解决方案：**
1. 确保手机和电脑在同一网络
2. 查看电脑IP地址：`ipconfig`
3. 在手机浏览器访问：`http://电脑IP:5000`
4. 检查Windows防火墙设置
5. 临时关闭防火墙测试

## 🔒 权限问题

### 问题11: 文件写入权限错误

**症状：**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**
1. 以管理员身份运行
2. 检查文件夹权限
3. 更改输出目录到用户文件夹

## 🚀 性能问题

### 问题12: 生成速度慢

**解决方案：**
1. 检查网络连接速度
2. 减少同时处理的节点数量
3. 使用更快的DNS服务器

## 📞 获取帮助

如果以上方案都无法解决问题：

1. **查看日志**: 运行时的错误信息通常包含有用的调试信息
2. **运行测试**: `python test_generator.py` 检查环境配置
3. **简化测试**: 使用 `python run_simple.py` 进行基础功能测试
4. **检查版本**: 确认Python和依赖包版本兼容性

## 🛠️ 调试技巧

### 启用详细日志
在脚本中添加：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 检查环境
```bash
python -c "import sys; print(sys.version)"
python -c "import requests; print(requests.__version__)"
python -c "import yaml; print(yaml.__version__)"
```

### 测试网络连接
```bash
python -c "import requests; print(requests.get('https://www.google.com').status_code)"
```