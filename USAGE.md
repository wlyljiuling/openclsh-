# 使用指南

## 快速开始

### 1. 安装依赖

```bash
# 运行安装脚本
python install.py

# 或手动安装
pip install -r requirements.txt
```

### 2. 启动方式

#### 方式一：Web界面（推荐）
```bash
python web_interface.py
# 然后访问 http://localhost:5000
```

#### 方式二：交互式命令行
```bash
python openclash_generator.py --interactive
```

#### 方式三：命令行直接生成
```bash
python openclash_generator.py --url "订阅链接" --template enhanced --output config.yaml
```

#### 方式四：统一启动脚本
```bash
python start.py
```

## 详细使用说明

### Web界面使用

1. 启动Web服务：`python web_interface.py`
2. 打开浏览器访问：`http://localhost:5000`
3. 输入订阅链接
4. 选择配置模板
5. 点击"生成配置文件"
6. 等待生成完成后下载

### 命令行使用

#### 基本用法
```bash
python openclash_generator.py --url "https://example.com/subscription" --template enhanced
```

#### 参数说明
- `--url, -u`: 订阅链接（必需）
- `--template, -t`: 配置模板（basic/enhanced/gaming/streaming）
- `--output, -o`: 输出文件路径
- `--interactive, -i`: 交互式模式

### 批量处理

#### 创建配置文件
```bash
python batch_generator.py --sample
```

#### 批量生成
```bash
python batch_generator.py --config batch_config.json --output output_dir
```

#### 配置文件格式
```json
[
  {
    "name": "config_1",
    "url": "https://example.com/subscription1",
    "template": "enhanced"
  },
  {
    "name": "config_2",
    "url": "https://example.com/subscription2",
    "template": "gaming"
  }
]
```

## 配置模板说明

### 基础模板 (basic)
- 包含基本的代理分组和规则
- 适合简单使用场景
- 配置文件较小

### 增强模板 (enhanced) - 推荐
- 包含广告拦截功能
- DNS优化配置
- 完整的分流规则
- 支持多种服务分组

### 游戏模板 (gaming)
- 针对游戏优化
- 包含Steam、Epic Games等游戏平台规则
- 低延迟配置

### 流媒体模板 (streaming)
- 针对流媒体服务优化
- 包含Netflix、YouTube、Spotify等规则
- 高带宽配置

## 支持的订阅格式

- **V2ray订阅**: vmess://
- **Shadowsocks订阅**: ss://
- **Trojan订阅**: trojan://
- **VLESS订阅**: vless://
- **Clash订阅**: YAML格式
- **混合订阅**: 包含多种协议的订阅

## 故障排除

### 常见问题

#### 1. 订阅解析失败
- 检查订阅链接是否正确
- 确认网络连接正常
- 尝试使用其他订阅链接

#### 2. 配置验证失败
- 检查节点信息是否完整
- 确认服务器地址和端口正确
- 查看错误日志获取详细信息

#### 3. Web界面无法访问
- 确认Python Flask已安装
- 检查端口5000是否被占用
- 尝试使用其他端口：`python web_interface.py --port 8080`

#### 4. 依赖安装失败
- 升级pip：`python -m pip install --upgrade pip`
- 使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

### 日志查看

生成过程中的详细日志会显示在控制台，包括：
- 订阅获取状态
- 节点解析进度
- 配置验证结果
- 错误信息

## 高级用法

### 自定义模板

1. 复制现有模板：`cp config/enhanced_template.yaml config/my_template.yaml`
2. 修改配置内容
3. 使用自定义模板：`--template my_template`

### 添加自定义规则

编辑模板文件中的 `rules` 部分：
```yaml
rules:
  # 自定义规则
  - DOMAIN-SUFFIX,example.com,🚀 节点选择
  - IP-CIDR,192.168.1.0/24,🎯 全球直连
  # 其他规则...
```

### 节点分组

生成器会自动根据节点名称进行地区分组：
- 🇭🇰 香港节点
- 🇺🇸 美国节点
- 🇯🇵 日本节点
- 🇸🇬 新加坡节点
- 等等...

## 安全提醒

1. **保护订阅链接**: 不要在公共场所分享订阅链接
2. **定期更新**: 建议定期重新生成配置文件
3. **备份配置**: 保存好生成的配置文件
4. **验证来源**: 只使用可信的订阅源