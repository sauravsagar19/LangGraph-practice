from typing import Annotated, List
from operator import add
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. DEFINE THE STATE (The Data)
# This schema tells LangGraph WHAT to track and HOW to merge updates.
class AgentState(TypedDict):
    # 'messages' uses 'add' reducer: new lists are APPENDED to the existing list.
    # Without this, every node would overwrite the entire chat history.
    messages: Annotated[List[str], add]
    
    # 'status' has NO reducer: new values simply OVERWRITE the old one.
    status: str

# 2. DEFINE THE NODES (The Workers)
# Nodes accept the full state but only return the PARTIAL updates they are responsible for.
def analyze_node(state: AgentState):
    print(f"🔍 Analyzing: {state['messages'][-1]}")
    # Returns an update: appends a thought to messages, changes status
    return {
        "messages": ["🤖 AI: Analyzing input..."],
        "status": "analyzing"
    }

def respond_node(state: AgentState):
    print(f"💡 Generating response for status: {state['status']}")
    # Returns an update: appends response, changes status again
    return {
        "messages": ["✅ AI: Analysis complete. Here is the result."],
        "status": "complete"
    }

# 3. DEFINE THE STATEGRAPH (The Blueprint)
# We pass AgentState to the graph so it knows how to manage memory.
builder = StateGraph(AgentState)

# Add nodes to the graph
builder.add_node("analyze", analyze_node)
builder.add_node("respond", respond_node)

# Define edges (Control Flow)
builder.add_edge(START, "analyze")       # Start -> Analyze
builder.add_edge("analyze", "respond")   # Analyze -> Respond
builder.add_edge("respond", END)         # Respond -> Finish

# Compile the graph into a runnable application
app = builder.compile()

# 4. EXECUTE
initial_input = {
    "messages": ["👤 User: Hello, can you check this data?"],
    "status": "new"
}

final_state = app.invoke(initial_input)

# Output Verification
print("\n--- Final State ---")
print(f"Total Messages: {len(final_state['messages'])}") 
# Result: 3 (Input + Analyze Thought + Response) -> Proves 'add' reducer worked!
print(f"Final Status: {final_state['status']}") 
# Result: "complete" -> Proves 'overwrite' behavior worked!