# we will make a simple chatbot which can call tool based on users query

from dotenv import load_dotenv
from typing import Annotated, List

from langgraph.graph import StateGraph
import os
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import httpx
import pydantic

from pydantic import BaseModel, Field

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
@tool
def arxiv():
    "It will be called when the query is related to any research paper"
    return "Arxiv tool called"
@tool
def wikipedia():
    "It will be called for basic general knowledge question"
    return "Wikipedia tool called"
@tool
def weather():
    "tools for weathers"
    return "weather tool called"


tools=[arxiv,wikipedia,weather]

llm=ChatOpenAI(
    model="gpt-4o-mini"
).bind_tools(tools=tools)

# res=llm.invoke("first tell me the weather and then tell me about attention is all you need research paper")

# print(res.tool_calls)

# Now lets build our Graph 
class State(BaseModel):
    messages: Annotated[List[AnyMessage],add_messages]=Field(default_factory=list)



from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Node Defination

def tool_calling_llm(state:State):
    return {"messages":[llm.invoke(state["messages"])]}


#build graph
builder=StateGraph(State)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools",ToolNode(tools))

#edge
builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)
builder.add_edge("tools",END)
graph=builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
# print(display)
with open("graph_workflow.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
print("Graph compiled! Saved schema visualizer workflow to 'graph_workflow.png'")


