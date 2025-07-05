# XiaoZhi_MCP - 多功能AI工具集成平台

A powerful MCP tool that integrates with various services, allowing AI to access geographic information, weather data, route planning, music control, financial data query and more.

一个强大的MCP工具，集成了多种服务，使AI能够访问地理信息、天气数据、路线规划、音乐控制、金融数据查询等多种功能。

![image](https://github.com/user-attachments/assets/2a8f95c0-f69e-4da8-b059-c04faaa9250a)

## Overview | 概述

MCP-MapNAVI is based on the Model Context Protocol (MCP), which allows AI language models to interact with external map services. Through this tool, AI can geocode addresses, check weather information, and plan driving routes - extending its capabilities beyond text generation.

MCP-MapNAVI基于模型上下文协议(MCP)，允许AI语言模型与外部地图服务交互。通过这个工具，AI可以进行地理编码、查询天气信息和规划驾驶路线 - 将其能力扩展到文本生成之外。

## Features | 特性

- 🗺️ **地理编码** - 将地址转换为经纬度坐标
- 🌤️ **天气查询** - 获取特定城市或地区的天气信息
- 🚗 **驾车路线规划** - 规划两点之间的驾驶路线
- 🎵 **音乐控制** - 根据歌曲名称搜索并播放音乐
- 📈 **股票查询** - 获取实时股票价格和市场数据
- 🔄 **自动重连** - 具有指数退避的WebSocket连接恢复机制
- 🔒 **安全通信** - 通过WebSocket的安全数据传输

## Requirements | 环境要求

- Python 3.7+
- websockets>=11.0.3
- python-dotenv>=1.0.0
- mcp>=1.8.1
- pydantic>=2.11.4
- requests>=2.28.0  # 新增：用于股票查询和网络新闻工具
- cozepy>=0.1.0  # 新增：用于Coze API调用
- yfinance>=0.2.30  # 新增：用于股票数据查询（可选）

## Installation | 安装指南

1. Clone the repository | 克隆仓库:
```bash
git clone https://github.com/shlan01/XiaoZhi_MCP-master.git
```

2. Navigate to the project directory | 进入项目目录:
```bash
cd XiaoZhi_MCP
```

3. Install dependencies | 安装依赖:
```bash
pip install -r requirements.txt
```

4. Install additional required packages | 安装额外必要包:
```bash
pip install websockets python-dotenv mcp pydantic requests cozepy
```

5. (Optional) Install yfinance for local stock data | (可选) 安装yfinance:
```bash
pip install yfinance
```

## Configuration | 配置说明

1. Copy the .env.example file to .env | 复制.env.example文件为.env:
```bash
cp .env.example .env
```

2. 编辑 .env 文件:
```bash
nano .env
```

2. 配置以下参数:
- `MCP_ENDPOINT`: Your MCP endpoint URL (格式: wss://api.xiaozhi.me/mcp/?token=xxx)
- `AMAP_API_KEY`: Your Amap API key (获取地址: https://lbs.amap.com/)
- `COZE_API_TOKEN`: Your Coze API token (获取地址: https://www.coze.cn/)
- `COZE_WORKFLOW_ID`: Your Coze workflow ID for general information queries
- `COZE_USER_ID`: Your Coze user ID (可选)
- `ALPHAVANTAGE_API_KEY`: Your Alpha Vantage API key (获取地址: https://www.alphavantage.co/)

## Quick Start | 快速开始

1. Start the main application | 启动主程序:
```bash
python run.py
```

2. The application will automatically start all configured tools | 应用程序将自动启动所有配置的工具模块

3. To use specific tools, you can also run them individually | 若要单独运行特定工具:
```bash
python mcp_pipe.py Amap_MCP.py
```

## Project Structure | 项目结构

- `mcp_pipe.py`: Main communication pipe that handles WebSocket connections and process management | 处理WebSocket连接和进程管理的主通信管道
- `Amap_MCP.py`: Implementation of Amap map service integration | 高德地图服务集成实现
- `music.py`: Music control tool implementation | 音乐控制工具实现
- `ragflow_mcp.py`: RAG-based information search tool implementation | 基于RAG的信息搜索工具实现
- `stock_query.py`: Stock market data query tool implementation | 股票市场数据查询工具实现
- `web_news.py`: Real-time news and information retrieval tool implementation | 实时新闻和信息检索工具实现
- `run.py`: Entry point for starting all tools | 启动所有工具的入口点
- `.env`: Environment variables configuration file | 环境变量配置文件

## Tools Documentation | 工具文档

### 🌍 Amap_MCP.py - 高德地图服务集成

提供以下功能：
- `geocode(address: str, city: str = "") -> dict`: 将地址转换为地理坐标
- `get_weather(city: str) -> dict`: 获取城市天气信息
- `plan_driving_route(origin: str, destination: str, ...) -> dict`: 规划驾车路线
- `input_tips(keywords: str, ...) -> dict`: 根据关键词提供建议

依赖：
- 高德地图 API 密钥 (`AMAP_API_KEY`)
- `requests` 库用于 HTTP 请求

### 🎵 music.py - 音乐控制工具

提供以下功能：
- `play_music(song_name: str) -> dict`: 根据歌曲名搜索并播放音乐

依赖：
- 音乐 API 密钥 (`MUSIC_API_KEY`)
- 第三方 API `https://api.yaohud.cn/api/music/wy`
- `requests` 和 `playsound` 库

### 📈 stock_query.py - 股票市场数据查询

提供以下功能：
- `get_stock_price(input_query: str) -> dict`: 获取股票实时价格和市场数据

依赖：
- Alpha Vantage API 密钥 (`ALPHAVANTAGE_API_KEY`)
- `requests` 和 `yfinance` 库

### 🌐 web_news.py - 实时新闻检索工具

提供以下功能：
- `get_web_news(input_query: str) -> dict`: 根据关键词获取实时新闻和信息

依赖：
- Coze API 密钥 (`COZE_API_TOKEN`)
- Coze 工作流 ID (`COZE_WORKFLOW_ID`)
- `cozepy` SDK

### 🔍 ragflow_mcp.py - 基于RAG的信息检索工具

提供以下功能：
- `start_search(question: str) -> dict`: 启动搜索任务
- `get_search_status(task_id: str) -> dict`: 获取任务状态
- `get_search_results(task_id: str) -> dict`: 获取搜索结果
- `cancel_search(task_id: str) -> dict`: 取消搜索任务
- `get_active_tasks() -> dict`: 获取所有活跃任务

依赖：
- Ragflow 本地部署实例
- 数据集 ID 和访问令牌
- `requests` 库

### ⚙️ run.py - 主程序启动器

功能：
- 加载 `.env` 环境变量
- 验证必要配置项
- 并行启动所有工具模块
- 统一管理进程生命周期

依赖：
- `dotenv` 库
- `subprocess` 用于进程管理

### 🔄 mcp_pipe.py - MCP协议通信管道

核心功能：
- WebSocket 连接管理
- 自动重连机制（指数退避）
- 双向消息传输（标准输入/输出代理）
- 异常处理和日志记录

依赖：
- `websockets` 库
- `asyncio` 用于异步通信
- `subprocess` 管理子进程

## Creating Your Own MCP Tools | 创建自己的MCP工具

Here's a simple example of creating an MCP tool | 以下是一个创建MCP工具的简单示例:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("YourToolName")

@mcp.tool()
def your_tool(parameter: str) -> dict:
    """Tool description here"""
    # Your implementation
    return {"success": True, "result": result}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

> Note: This is a basic template. Actual implementation may need additional imports and error handling.

## Use Cases | 使用场景

- Mathematical calculations | 数学计算
- Email operations | 邮件操作
- Knowledge base search | 知识库搜索
- Remote device control | 远程设备控制
- Data processing | 数据处理
- Custom tool integration | 自定义工具集成
- Financial data query | 金融数据查询

## Contributing | 贡献指南

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。

## License | 许可证

本项目采用MIT许可证。我们建议你添加一个LICENSE文件以便于他人使用。MIT许可证模板可在[此处](https://opensource.org/licenses/MIT)获取。

## Acknowledgments | 致谢

- 感谢所有贡献者帮助完善这个项目
