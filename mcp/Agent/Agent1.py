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

config = {
    #custom mcp server defined by me
    "mcp-math": {
        "command": "python",
        "args": [str(mcp_servers_dir / "mcp_math.py")],
        "transport": "stdio"
    },
    # custom mcp server defined by me
    "mcp-git": {
        "command": "python",
        "args": [str(mcp_servers_dir / "mcp_git.py")],
        "transport": "stdio"
    },
    # It is availabe on mcp github server , I donnloaded it using pip install mcp-server-time 
    # and then using it .
    "time-server": {
        "command": "python",
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

async def agent(query: str):
    # Create the MCP client directly
    client = MultiServerMCPClient(config)
    
    try:
        # Get all tools from the MCP server
        all_tools = await client.get_tools()
        
        print(f"Loaded {len(all_tools)} tools from MCP servers")
        
        # binding the tools with llm to use them in the graph
        llm_with_tools = llm.bind_tools(all_tools)
        
        # creating a tool node to handle the tools
        tool_node = ToolNode(tools=all_tools)
        
        # creating a graph
        builder = StateGraph(State)
        
        # Define tool_calling_llm to use llm_with_tools
        async def tool_calling_llm_with_tools(state: State):
            return {"messages": [llm_with_tools.invoke(state.messages)]}
        
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
        
        # visualize the graph and saving it
        print("Generating graph visualization...")
        display(Image(graph.get_graph().draw_mermaid_png()))
        
        with open("/workspaces/LangGraph-practice/mcp/graphsPNG/agent1.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
        
        print(f"Processing query: {query}")
        result = await graph.ainvoke({"messages": [{"type": "human", "content": query}]})
        print(result["messages"][-1].content)
        return "Agent execution completed. Result printed above."
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return f"Agent execution failed with error: {e}"

if __name__ == "__main__":
    asyncio.run(agent("add 4 and 5 and then create a joke about the result"))


    



