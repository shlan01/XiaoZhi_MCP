# XiaozhiMCP-MapNAVI | MCP多功能集成工具

A powerful MCP tool that integrates with various services, allowing AI to access geographic information, weather data, route planning, music control, task management and more.

一个强大的MCP工具，集成了多种服务，使AI能够访问地理信息、天气数据、路线规划、音乐控制、任务管理等多种功能。

![image](https://github.com/user-attachments/assets/2a8f95c0-f69e-4da8-b059-c04faaa9250a)
![image](https://github.com/user-attachments/assets/62974a24-02fc-4efe-948d-30c8edab707a)

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
git clone https://github.com/yourusername/XiaozhiMCP-MapNAVI.git
```

2. Navigate to the project directory | 进入项目目录:
```bash
cd XiaozhiMCP-MapNAVI
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

2. Edit the .env file with your favorite editor | 编辑.env文件，设置以下参数:
```bash
nano .env
```

3. Configure the following parameters | 配置以下参数:
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

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详情请查看LICENSE文件。

## Acknowledgments | 致谢

- Thanks to all contributors who have helped shape this project | 感谢所有帮助塑造这个项目的贡献者
- Inspired by the need for extensible AI capabilities | 灵感来源于对可扩展AI能力的需求
