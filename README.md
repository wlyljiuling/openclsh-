# OpenClash 配置文件生成器

一个简单易用的 OpenClash 配置文件生成工具，只需提供订阅链接即可生成完美的配置文件。

## 功能特点

- 🚀 支持多种订阅格式（V2ray、Shadowsocks、Trojan等）
- 🎯 自动解析订阅链接并转换为 OpenClash 格式
- 📊 智能分组（按地区、用途等）
- 🛡️ 内置广告拦截规则
- 🌐 支持多种代理规则（YouTube、ChatGPT、Gemini等）
- ⚡ 自动测速和故障转移
- 🔧 可自定义配置模板

## 快速开始

### 方法一：使用 Python 脚本

```bash
# 安装依赖
pip install -r requirements.txt

# 运行生成器
python openclash_generator.py
```

### 方法二：使用 Web 界面

```bash
# 启动 Web 服务
python web_interface.py

# 访问 http://localhost:5000
```

### 方法三：命令行直接生成

```bash
python openclash_generator.py --url "你的订阅链接" --output config.yaml
```

## 使用说明

1. 准备你的订阅链接
2. 运行生成器
3. 输入订阅链接
4. 选择配置模板（可选）
5. 生成配置文件
6. 导入到 OpenClash

## 配置模板

项目提供多种预设模板：

- **基础模板**：包含基本的代理分组和规则
- **增强模板**：包含广告拦截、分流规则等
- **游戏模板**：针对游戏优化的配置
- **流媒体模板**：针对 Netflix、YouTube 等优化

## 目录结构

```
openclash-generator/
├── openclash_generator.py    # 主生成器脚本
├── web_interface.py          # Web 界面
├── config/                   # 配置模板目录
│   ├── basic_template.yaml   # 基础模板
│   ├── enhanced_template.yaml # 增强模板
│   └── rules/               # 规则文件
├── utils/                   # 工具函数
│   ├── parser.py           # 订阅解析器
│   ├── converter.py        # 格式转换器
│   └── validator.py        # 配置验证器
├── static/                 # Web 静态文件
├── templates/              # Web 模板
└── requirements.txt        # 依赖列表
```

## 支持的订阅格式

- V2ray 订阅
- Shadowsocks 订阅
- Trojan 订阅
- Clash 订阅
- 混合订阅

## 许可证

MIT License