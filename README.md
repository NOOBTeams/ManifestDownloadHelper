<p align="right">
  <a href="README_EN.md">English</a> | 中文
</p>

# Steam游戏清单下载工具

一个用于下载Steam游戏清单文件的命令行工具，支持中文游戏搜索、自动翻译和文件命名优化。

## 功能特性

- 🎮 **游戏搜索**：支持中英文游戏名称搜索
- 🔄 **自动翻译**：自动将中文游戏名翻译为英文，提高搜索准确率
- 📁 **智能命名**：下载文件包含游戏名称和AppID，如"艾尔登法环_1423870.zip"
- 📊 **进度显示**：实时显示下载进度
- 🔄 **多源下载**：支持多个下载源，失败自动切换
- 📝 **历史记录**：自动保存下载历史，方便追踪

## 安装使用

### 环境要求

- Python 3.10+
- 互联网连接

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

#### 基本用法

```bash
# 搜索并下载游戏
python main.py "艾尔登法环"
```

#### 高级选项

```bash
# 限制搜索结果数量
python main.py "原神" -n 5

# 搜索英文游戏
python main.py "elden ring"

# 指定语言和国家
python main.py "游戏名" -l english -c US

# 禁用自动翻译
python main.py "游戏名" --no-translate

# 查看帮助
python main.py -h
```

## 项目结构

```
ManifestDownloadHelper/
├── main.py              # 程序入口
├── config.py            # 配置文件
├── requirements.txt     # 依赖管理
├── src/                 # 源代码
│   ├── __init__.py
│   ├── steam.py         # 核心功能
│   └── utils.py         # 工具函数
├── manifests/           # 下载的清单文件
├── data/                # 数据目录
│   └── history.json     # 历史记录
└── README.md            # 说明文档
```

## 配置说明

配置文件 `config.py` 包以下可配置项：

- `API_SERVERS`: API服务器列表
- `STEAM_SEARCH_API`: Steam搜索API地址
- `SECRET_KEY`: 编码密钥
- `SRCS`: 下载源数量
- `DEFAULT_LANGUAGE`: 默认语言
- `DEFAULT_COUNTRY`: 默认国家

## 历史记录

下载记录保存在 `data/history.json` 中，包含：
- 游戏名称和AppID
- 下载时间
- 文件路径和大小

## 注意事项

1. 本工具仅供学习交流使用，请勿用于商业用途
2. 下载的清单文件仅用于研究目的
3. 请遵守Steam的使用条款
4. 如遇网络问题，会自动尝试其他下载源
5. 国内网络可能无法访问下载源，请须知

## 更新日志

### v0.3.0 (2026-05-30)
- 重构项目结构，模块化设计
- 添加历史记录功能
- 优化文件命名策略
- 改进用户交互界面

### v0.2.0 (2026-03-09)
- 添加多源下载支持
- 实现AppID编码
- 添加进度显示

### v0.1.0 (2026-03-09)
- 初始版本，基本搜索和下载功能