import os
from dotenv import load_dotenv
from fastmcp import FastMCP
mcp=FastMCP("mcp-tool")

load_dotenv()

YOUTUBE_API_SAURAVSAGAR2296=os.getenv("YOUTUBE_API_KEYS_SAURAVSAGAR2296")
YOUTUBE_API_SAURAVSAGARTATA= os.getenv("YOUTUBE_API_KEYS_SAURAVSAGARTATA")



mcp_config = {
        "youtube-server": {
            "command": "uv",  # Or the full path to your 'uv' binary
            "args": [
                "run",
                "--directory", "/workspaces/LangGraph-practice", #Give the path of the folder where there is pyproject.toml since we are using uv
                "multiagent/youtube_agent/mcp_server.py" #path of the mcp_server.py
            ],
            "env": {
                "YOUTUBE_API_KEY":YOUTUBE_API_SAURAVSAGAR2296
            }
        }
    }

@mcp.tool
def youtube_transcriptor(vedio_url:str):
    pass



