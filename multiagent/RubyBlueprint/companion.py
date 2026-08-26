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