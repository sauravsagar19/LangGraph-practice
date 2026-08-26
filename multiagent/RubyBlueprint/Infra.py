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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MAIN_LLM=ChatOpenAI (
    model= 'gpt-4o-mini',
    temperature=0.3,
    api_key=OPENAI_API_KEY,
    max_retries=3
)

FALLBACK_LLM=ChatGoogleGenerativeAI(
    model= 'gemini-1.5-turbo',
    temperature=0.3,
    api_key=GEMINI_API_KEY
)

llm=MAIN_LLM.with_fallbacks(FALLBACK_LLM)
