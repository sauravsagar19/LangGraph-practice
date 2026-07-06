import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
mcp=FastMCP("mcp-tool")

load_dotenv()

YOUTUBE_API_SAURAVSAGAR2296=os.getenv("YOUTUBE_API_KEYS_SAURAVSAGAR2296")
YOUTUBE_API_SAURAVSAGARTATA= os.getenv("YOUTUBE_API_KEYS_SAURAVSAGARTATA")

from googleapiclient.discovery import build
# service = build('youtube', 'v3',developerKey=YOUTUBE_API_SAURAVSAGARTATA)

# search_response=service.search().list(
#     q="honey singh latest songs.",
#     part="snippet",
#     maxResults=3

# ).execute()

# print(search_response)

vedio_id="ORMx45xqWkA"
ytt_api = YouTubeTranscriptApi()
transcript=ytt_api.list(vedio_id)
for line in transcript:
    print(f"{line['start']}s: {line['text']}")



# mcp_config = {
#         "youtube-server": {
#             "command": "uv",  # Or the full path to your 'uv' binary
#             "args": [
#                 "run",
#                 "--directory", "/workspaces/LangGraph-practice", #Give the path of the folder where there is pyproject.toml since we are using uv
#                 "multiagent/youtube_agent/mcp_server.py" #path of the mcp_server.py
#             ],
#             "env": {
#                 "YOUTUBE_API_KEY":YOUTUBE_API_SAURAVSAGAR2296
#             }
#         }
#     }

@mcp.tool
def youtube_transcriptor(vedio_url:str):
    pass



