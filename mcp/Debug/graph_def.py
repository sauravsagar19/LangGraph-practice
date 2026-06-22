# It is same as Agent/Agent1.py . But for debugging purpose I am creating a copy of it in Debug folder and then I will make changes to it for debugging without affecting the original one.
'''Its the host'''
# 1. MCP Client & Tool Adapter
from langchain_mcp_adapters.client import MultiServerMCPClient

# 2. LangGraph Core
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# 3. Standard Async/AsyncIO (required for MCP communication)
import asyncio
from pydantic import BaseModel, Field

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated, List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from IPython.display import Image, display

import sys
from pathlib import Path
import os

load_dotenv()
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")

llm = ChatOpenAI(model="gpt-4o-mini")

# Get the absolute path to the mcp_servers directory
mcp_servers_dir = Path(__file__).parent.parent / "mcp_servers"
python_executable = sys.executable

config = {
    # custom mcp server defined by me
    "mcp-math": {
        "command": python_executable,
        "args": [str(mcp_servers_dir / "mcp_math.py")],
        "transport": "stdio"
    },
    # custom mcp server defined by me
    "mcp-git": {
        "command": python_executable,
        "args": [str(mcp_servers_dir / "mcp_git.py")],
        "transport": "stdio"
    },
    # It is available on mcp github server, I downloaded it using pip install mcp-server-time
    # and then using it.
    "time-server": {
        "command": python_executable,
        "args": ["-m", "mcp_server_time"],
        "transport": "stdio"
    },
    # MCP using http transport
    "dadjokes": {
        "transport": "http", # MCP maps 'streamable-http' to 'http'
        "url": "https://gateway.pipeworx.io/dadjokes/mcp"
    }
}

class State(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages] = Field(default_factory=list)

client = MultiServerMCPClient(config)
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
# Get all tools from the MCP server
all_tools = loop.run_until_complete(client.get_tools())

print(f"Loaded {len(all_tools)} tools from MCP servers")

# binding the tools with llm to use them in the graph
llm_with_tools = llm.bind_tools(all_tools)

# creating a tool node to handle the tools
tool_node = ToolNode(tools=all_tools)

# creating a graph
builder = StateGraph(State)

# Define tool_calling_llm to use llm_with_tools
async def tool_calling_llm_with_tools(state: State):
    return {"messages": [await llm_with_tools.ainvoke(state.messages)]}

# adding nodes
builder.add_node("tool_calling_node", tool_calling_llm_with_tools)
builder.add_node("tools", tool_node)

# creating edges
builder.add_edge(START, "tool_calling_node")
builder.add_conditional_edges(
    "tool_calling_node",
    tools_condition
)
builder.add_edge("tools", "tool_calling_node")

# compiling graph
graph = builder.compile()