from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from multiagent.youtube_agent.state import shared_state
from multiagent.youtube_agent.mcp_server import mcp_config
from langchain_mcp_adapters.client import MultiServerMCPClient
from utility.utility import savePNG, deleteGraphPNG
from youtube_agent.schema import VedioSummary
from langchain_openai import ChatOpenAI
from youtube_agent.prompts import TRANSCRIPT_FETCHER_PROMPT,REPORT_MAKER_PROMPT
client=MultiServerMCPClient(mcp_config)
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


#llm
llm= ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)


# Defining Agent
async def transcriptor_agent(State:shared_state):

    current_agent="Transcriptor_agent"

    async with client: # Safely connect to the MCP server background process using async context

        all_tool= await client.get_tools()
        tool_dict = {tool.name: tool for tool in all_tool}
        fetch_transcript_tool=tool_dict.get("")
        llm_with_tool=llm.bind_tools(all_tool)

        chain=TRANSCRIPT_FETCHER_PROMPT |  llm_with_tool

        res=await chain.invoke({"yt_link":State.url})

        return {
            "transcript": res.content,
            "current_agent" : current_agent,
            "running_summary": "Transcriptor has finished its job."
            }

def reporter_agent(State:shared_state):
    current_agent="reporter_agent"

    llm_with_strucured_output=llm.with_structured_output(VedioSummary)

    chain=REPORT_MAKER_PROMPT | llm_with_strucured_output
    res= chain.invoke({"transcript":State.transcript})

    return {
        "report":res,
        "current_agent":current_agent,
        "running_summary": "Reported has made the report and finished the assigned job."
        }













