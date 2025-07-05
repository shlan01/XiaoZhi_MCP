# web_news_tool.py
from mcp.server.fastmcp import FastMCP
import sys
import logging
import os
import json  # 用于安全地解析JSON数据

# 导入所需的库
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType  # noqa
from cozepy import COZE_CN_BASE_URL, Stream, WorkflowEvent, WorkflowEventType  # noqa

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
logger = logging.getLogger('web_news')

# 创建 MCP 服务器
mcp = FastMCP("网络新闻")  # 保持已修改的服务器名称

# 从环境变量获取Coze API配置
coze_api_token = os.getenv("COZE_API_TOKEN", "default_token")  # 从环境变量获取API密钥
workflow_id = os.getenv("COZE_WORKFLOW_ID", "default_workflow_id")  # 从环境变量获取工作流ID
user_id = os.getenv("COZE_USER_ID", "default_user_id")  # 从环境变量获取用户ID

# 创建Coze客户端
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)

# 直接工作流查询
def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
    for event in stream:
        if event.event == WorkflowEventType.MESSAGE:
            res_messages = ''
            # 把event.message.content从字符串转为json对象
            event.message.content = json.loads(event.message.content)  # 使用json.loads替代eval

            # 遍历res_messages里的output数组
            for output in event.message.content['output']:
                a = f"{output['title']}：{output['summary']}\n"
                res_messages += a

            return res_messages
        elif event.event == WorkflowEventType.ERROR:
            logger.error(f"获取实时咨询时出错: {str(event.error)}")
            return str(event.error)
        elif event.event == WorkflowEventType.INTERRUPT:
            handle_workflow_iterator(
                coze.workflows.runs.resume(
                    workflow_id=workflow_id,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="hey",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
            )

@mcp.tool()
def get_web_news(input_query: str) -> dict:
    logger.info("调用了get_web_news工具")
    """获取实时资讯。当你需要获取实时的信息，比如汇率、时事、新闻、比赛信息等等，这个工具非常有用。input_query为搜索关键词。"""
    try:
        logger.info(f"搜索信息: {input_query}")
        res_messages = handle_workflow_iterator(
            coze.workflows.runs.stream(
                workflow_id=workflow_id,
                parameters={
                    "input": input_query
                }
            )
        )
        # logger.info(f"搜索结果: {res_messages}")
        return {"success": True, "result": res_messages}

    except Exception as e:
        logger.error(f"获取实时咨询时出错: {str(e)}")
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")