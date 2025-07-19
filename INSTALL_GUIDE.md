# 安装指南

## 🐍 Python 环境安装

### Windows 系统

#### 方法1: 从官网下载（推荐）
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载最新版本的Python（3.7+）
3. 运行安装程序，**重要：勾选"Add Python to PATH"**
4. 完成安装后重启命令提示符

#### 方法2: 使用Microsoft Store
1. 打开Microsoft Store
2. 搜索"Python"
3. 安装Python 3.11或更高版本

#### 方法3: 使用Chocolatey
```powershell
# 以管理员身份运行PowerShell
choco install python
```

### 验证安装
打开命令提示符或PowerShell，运行：
```bash
python --version
# 或
py --version
```

如果显示版本号，说明安装成功。

## 📦 项目依赖安装

### 自动安装（推荐）
```bash
python install.py
```

### 手动安装
```bash
# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install requests pyyaml flask click colorama tqdm
```

### 使用国内镜像（如果下载慢）
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 🚀 运行项目

### 1. Web界面（最简单）
```bash
python web_interface.py
```
然后打开浏览器访问：http://localhost:5000

### 2. 交互式命令行
```bash
python openclash_generator.py --interactive
```

### 3. 统一启动脚本
```bash
python start.py
```

## 🔧 常见问题解决

### 问题1: 'python' 不是内部或外部命令
**解决方案：**
1. 重新安装Python，确保勾选"Add Python to PATH"
2. 或者使用完整路径运行：`C:\Python311\python.exe script.py`
3. 或者尝试使用 `py` 命令代替 `python`

### 问题2: pip 安装失败
**解决方案：**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 如果权限问题，使用用户安装
pip install --user package_name
```

### 问题3: 模块导入错误
**解决方案：**
确保在项目根目录运行脚本，或者设置PYTHONPATH：
```bash
set PYTHONPATH=%cd%
python script.py
```

### 问题4: 端口被占用
**解决方案：**
```bash
# 查看端口占用
netstat -ano | findstr :5000

# 杀死占用进程
taskkill /PID <进程ID> /F

# 或者使用其他端口
python web_interface.py --port 8080
```

## 🎯 快速测试

运行测试确保一切正常：
```bash
python test_generator.py
```

如果所有测试通过，说明环境配置正确。

## 📱 移动设备访问

如果需要在手机上访问Web界面：
1. 确保电脑和手机在同一网络
2. 查看电脑IP地址：`ipconfig`
3. 在手机浏览器访问：`http://电脑IP:5000`

## 🔒 防火墙设置

如果无法访问Web界面，可能需要允许Python通过防火墙：
1. 打开Windows防火墙设置
2. 允许Python.exe通过防火墙
3. 或者临时关闭防火墙测试