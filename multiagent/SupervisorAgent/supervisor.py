from typing import Annotated, Literal, Optional


from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from .prompts.prompts import GENERAL_AGENT_PROMPT, SUPERVISOR_PROMPT , INTERVIEWER_AGENT_PROMPT, COMPANION_AGENT_PROMPT

class global_state(BaseModel):
    is_locked: bool
    current_agent: str
    next_agent: Optional[str] = None
    session_summary: str

    general_memory: Annotated[list, add_messages]
    interviewer_memory: Annotated[list, add_messages]
   # Companion_memory: Annotated[list, add_messages] becasue we dont want supervisor to access private conversation
    final_memory: Annotated[list, add_messages]

class supervisor_respone (BaseModel):
    next_agent : Literal["general_agent","Interviewer_agent","Companion_agent","Final_agent"]=Field(
        description="The agent to route the query to next."
    )
    resoning : str = Field(
        description="Reason for choosing the agent."
    )

# DEFINING NODES

def supervisor(State: global_state):
    prompt=SUPERVISOR_PROMPT



