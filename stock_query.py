# stock_query.py
from mcp.server.fastmcp import FastMCP
import sys
import logging
import os
import requests  # 用于发起HTTP请求

# 导入yfinance库
import yfinance as yf

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger('stock_query_tool')

# 创建 MCP 服务器
mcp = FastMCP("股票查询")  # 保持已修改的服务器名称

@mcp.tool()
def get_stock_price(input_query: str) -> dict:
    """
    获取股票实时价格。当您需要查询股票的当前价格时，可以使用这个工具。
    input_query为股票代码（例如：AAPL代表苹果公司）。
    """
    try:
        logger.info(f"收到股票查询请求: {input_query}")
        
        # 使用Alpha Vantage API获取股票数据
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return {"success": False, "error": "未配置有效的Alpha Vantage API密钥"}
        
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={input_query}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            return {
                "success": True,
                "result": {
                    "symbol": input_query,
                    "price": quote["05. price"],
                    "highest": quote["06. high"],
                    "lowest": quote["07. low"],
                    "volume": quote["08. volume"],
                    "time": quote["07. latest trading day"]  # 使用最新的交易日作为时间
                }
            }
        else:
            return {"success": False, "error": "无法获取股票数据或股票代码无效"}
            
    except Exception as e:
        logger.error(f"处理股票查询请求时出错: {str(e)}")
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")