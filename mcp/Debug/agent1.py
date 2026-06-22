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
from graph_def import graph

load_dotenv()
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")


async def agent(query: str):
    # Create the MCP client directly
    try:
        
        # visualize the graph and saving it
        print("Generating graph visualization...")
        display(Image(graph.get_graph().draw_mermaid_png()))
        
        with open("/workspaces/LangGraph-practice/mcp/graphsPNG/agent1.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
        
        print(f"Processing query: {query}")
        result = await graph.ainvoke({"messages": [{"type": "human", "content": query}]})
        print(result["messages"][-1].content)
        return "DONE"
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return f"Agent execution failed with error: {e}"

if __name__ == "__main__":
    asyncio.run(agent("go to this file : /workspaces/LangGraph-practice/my_data/data.text and then tell me the content written in it. change the nujmber to 000 and save it."))

    



