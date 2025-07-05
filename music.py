from mcp.server.fastmcp import FastMCP

# 创建 MCP 实例
mcp = FastMCP("MusicPlayer")
import requests
from playsound import playsound
import tempfile
import os
import logging
import threading

# 初始化MCP和日志
logger = logging.getLogger(__name__)
_LOCK = threading.Lock()  # 保留原线程锁

_API_URL = 'https://api.yaohud.cn/api/music/wy'  # 进网站去注册拿到API_KEY
_API_KEY = os.getenv('MUSIC_API_KEY', 'emSQtAcJlyzR9nhrFVY')  # 从环境变量获取API密钥，有默认值备用

@mcp.tool()
def play_music(song_name: str) -> str:
    """
    通过MCP接口播放音乐（线程安全）
    Args:
        song_name: 歌曲名，默认为"好运来"
    Returns:
        str: 播放结果或错误信息
    """
    if not song_name.strip():
        return "错误：歌曲名不能为空"

    with _LOCK:
        try:
            # 1. 调用API获取音乐URL
            logger.info(f"搜索歌曲: {song_name}")
            params = {'key': _API_KEY, 'msg': song_name.strip(), 'n': '1'}
            resp = requests.post(_API_URL, params=params, timeout=10)
            resp.raise_for_status()
            music_url = resp.json()['data']['musicurl']

            # 2. 下载并保存临时文件
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                f.write(requests.get(music_url, timeout=10).content)
                temp_path = f.name

            # 3. 构造JSON响应，适配前端播放控制
            # 返回指向本地流服务的播放指令
            return {
                "type": "audio",
                "format": "opus",
                "source": f"ws://localhost:8765?song={song_name}",
                "protocol_version": 3,
                "audio_params": {
                    "sample_rate": 16000,
                    "channels": 1,
                    "frame_duration": 60
                },
                "transport": "websocket"
            }

        except Exception as e:
            logger.error(f"播放失败: {str(e)}")
            return f"播放失败: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")  # MCP标准输入输出模式
