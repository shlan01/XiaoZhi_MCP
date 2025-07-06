# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
# 新增subprocess导入
import subprocess
# 新增sys导入
import sys

# 加载.env文件
load_dotenv()

# 现在所有模块都可以通过 os.getenv() 获取环境变量
# 获取MCP_ENDPOINT
MCP_ENDPOINT = os.getenv("MCP_ENDPOINT")
if not MCP_ENDPOINT:
    print("错误：未找到MCP接入点配置！")
    print("请在.env文件中正确配置MCP_ENDPOINT")
    sys.exit(1)

# 显示正在使用的MCP_ENDPOINT（隐藏中间部分字符）
print(f"正在使用MCP接入点: {MCP_ENDPOINT[:20]}...{MCP_ENDPOINT[-20:]}")

# 新增环境变量验证函数
def validate_env_vars():
    required_vars = ['MUSIC_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"缺少必要环境变量: {', '.join(missing)}。请检查 .env 文件。")

# 调用验证函数
validate_env_vars()

# 启动单个工具的函数
def start_tool(script_name):
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["MCP_ENDPOINT"] = MCP_ENDPOINT
        
        # 启动子进程
        process = subprocess.Popen(
            [sys.executable, "mcp_pipe.py", script_name],
            env=env,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return process
    except Exception as e:
        print(f"启动工具 {script_name} 时出错: {e}")
        return None

# 启动所有工具
processes = []

# 启动指定工具
tools_to_start = ["Amap_MCP.py", "music.py", "ragflow_mcp.py", "web_news.py", "stock_query.py"]
for tool in tools_to_start:
    print(f"启动工具 {tool}...")
    process = start_tool(tool)
    if process:
        processes.append(process)

print("所有指定工具已启动！")
print(f"当前使用的MCP接入点: {MCP_ENDPOINT[:20]}...{MCP_ENDPOINT[-20:]}")
print("按Enter键终止所有进程...")
input()  # 等待用户输入

# 终止所有进程
print("正在终止所有进程...")
for process in processes:
    try:
        process.terminate()
        process.wait(timeout=5)
    except:
        pass

print("所有进程已终止")

# 示例：检查当前分支并进行相应操作（假设需要）
import subprocess

def get_current_branch():
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"获取当前分支时出错: {e}")
        return None

current_branch = get_current_branch()
if current_branch:
    print(f"当前分支: {current_branch}")
    if current_branch == "主要":
        print("警告：当前分支为'主要'，请切换到其他分支再进行操作。")
else:
    print("无法获取当前分支信息。")
