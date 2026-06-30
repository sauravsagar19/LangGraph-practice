from typing import Annotated, Literal, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
import os

from prompts.prompts import (
    COMPANION_AGENT_PROMPT,
    GENERAL_AGENT_PROMPT,
    INTERVIEWER_AGENT_PROMPT,
    SUPERVISOR_PROMPT,
)



load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

class global_state(BaseModel):
    is_locked: bool
    current_agent: str
    next_agent: Optional[str] = None
    session_summary: str

    general_memory: Annotated[list, add_messages]
    interviewer_memory: Annotated[list, add_messages]
   # Companion_memory: Annotated[list, add_messages] becasue we dont want supervisor to access private conversation
    final_memory: Annotated[list, add_messages]

class supervisor_response (BaseModel):
    next_agent : Literal["general_agent","Interviewer_agent","Companion_agent","Final_agent"]=Field(
        description="The agent to route the query to next."
    )
    reasoning : str = Field(
        description="Reason for choosing the agent."
    )

supervisor_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

# fallback model is openapi

global_fallback_model=ChatOpenAI (
    model= 'gpt-4o-mini',
    temperature=0.3
)


# DEFINING NODES
def supervisor(State: global_state):
    
    if State.is_locked == True:
        next_agent = State.current_agent

    llm_with_structured_output=supervisor_llm.with_structured_output(supervisor_response)
    chain=SUPERVISOR_PROMPT | llm_with_structured_output
    response=chain.invoke({
        "user_input" : State.general_memory[-1].content,
        "is_locked": State.is_locked,
        "current_agent":State.current_agent,
        "session_summary": State.session_summary,
    })
    return {"next_agent":response.next_agent}

res=supervisor_llm.invoke({"what are you doing?"})
print(res.content)







    




