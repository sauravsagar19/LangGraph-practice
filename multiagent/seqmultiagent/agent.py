
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from langchain_openai import ChatOpenAI
from Tools.agent_tools import search_arxiv, search_wikipedia, human_approval
all_tools=[search_arxiv, search_wikipedia, human_approval]
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it before running the script.")

class Agentclass(BaseModel):
    topic: Optional[str] = "" # the initial input
    research:Optional[str] = "" # The output of the researcher node
    analysis:Optional[str] = "" # The output of the analyst node
    report:Optional[str] = "" # The output of the reporter node
    review:Optional[str] = "" # The Final output of the reviewer node

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=OPENAI_API_KEY
)

# DEFINING NODES
def researcher_node(State:Agentclass):
    search_result=search_wikipedia.invoke({"query_string":State.topic})
    return {"research":search_result}

def analyser_node(State:Agentclass):
    prompt=f'''
    You are a research analyst. Your task is to analyze the research papers provided by the researcher node and extract key insights, trends, and implications related to the topic. Summarize the findings in a clear and concise manner, highlighting any significant discoveries or patterns that emerge from the research.
    reasearch paper - {State.research}
    '''
    analysis=llm.invoke(prompt).content
    return {"analysis":analysis}

def reporter_node(State:Agentclass):
    prompt=f'''
    you are a report writer. your task is to write a comprehensive report based on the analysis of the anylyser node. The report should be well-structured, informative, and accessible to a broad audience. It should include an introduction to the topic, a summary of the key insights from the analysis, and any relevant conclusions or recommendations based on the findings.
    Analysis - {State.analysis}
    '''
    report=llm.invoke(prompt).content
    return {"report":report}

def reviewer_node(State:Agentclass):
    prompt=f'''
    you are a reviewer. your task is to review the report written by the reporter node. The review should assess the clarity, coherence, and overall quality of the report. Provide constructive feedback on any areas that could be improved, such as organization, depth of analysis, or clarity of writing. Additionally, highlight any strengths of the report and suggest ways to enhance its impact and effectiveness.
    Report - {State.report}
    '''
    review=llm.invoke(prompt).content
    return {"review":review}


from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import time
import pprint
current_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

builder=StateGraph(Agentclass)

#adding nodes
builder.add_node("researcher", researcher_node)
builder.add_node("analyser", analyser_node)
builder.add_node("reporter", reporter_node)
builder.add_node("reviewer", reviewer_node)

#adding edges
builder.add_edge(START, "researcher")
builder.add_edge("researcher", "analyser")
builder.add_edge("analyser", "reporter")
builder.add_edge("reporter", "reviewer")
builder.add_edge("reviewer", END)

#compile
graph=builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
# print(display)
with open(f"/workspaces/LangGraph-practice/multiagent/graph_PNG/graph-{current_time}.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
print("Graph compiled! Saved schema visualizer workflow to 'graph_workflow.png'")


response=graph.stream({"topic":"Explain the concept of quantum computing and its potential applications in various industries."})

print("Final Output of the workflow:")
pprint.pprint(response["review"])

# for event in graph.stream({"topic": "Quantum Computing"}):
#     for node_name, output in event.items():
#         print(f"Node '{node_name}' finished.")
    
