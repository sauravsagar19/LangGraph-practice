from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

class shared_state(BaseModel):
    current_agent: str = "transciptor"
    next_agent: str = None

    running_summary:str = "" # running summary of the process.

