from typing import Annotated, Literal, Optional, List
from pathlib import Path
import sys
from IPython.display import display, Image
from dotenv import load_dotenv
from langchain.messages import SystemMessage
from langchain_openai import ChatOpenAI, data
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph, add_messages
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage  , HumanMessage,trim_messages ,RemoveMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import json
from pydantic import BaseModel, Field
import os
from Infra import llm
from agent_tools import * 


class GeneralState(BaseModel):
    Thread_id: Optional[str] = Field(default=None, description="The thread ID for the conversation.")
    CurrentAgent:str="general"
    last_user_msg:str
    messages: Annotated[list,add_messages] = []
    pending_tool_name: Optional[str]
    pending_tool_args: Optional[dict]
    is_destructive_action: bool
    user_approval_granted: Optional[bool]
    non_private_summary_update: Optional[str]


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# class general_res(BaseModel):
#     response: str
#     tool_name: Optional[str]
#     # tool_args: Optional[dict]
#     is_destructive_action: bool
#     user_approval_granted: Optional[bool]
#     non_private_summary_update: Optional[str]

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt uses MessagesPlaceholder to maintain full conversation context
general_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Ruby, a helpful voice assistant. Answer queries concisely and use available tools to assist the user."),
    MessagesPlaceholder(variable_name="messages"),
])
tools=[arxiv,wikipedia,weather,delete_file,clear_cache,open_yt]
llm_with_tools=llm.bind_tools(tools=tools)

general_chain=general_agent_prompt | llm_with_tools


#Node

def general_node(state: GeneralState) -> dict:
    res=general_chain.invoke(messages=state.messages)
    return {"messages":[res]}

def tool_execution_node(state:GeneralState)->dict:
    last_msg=state.messages[-1]
    if not last_msg.tool_calls:
        return {}
    tool_call=last_msg.tool_calls[0]


