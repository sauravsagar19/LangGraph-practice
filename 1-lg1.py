from typing_extensions import TypedDict

class State(TypedDict):
    graph_info: str

#creating nodes
def start_play(state:State):
    print("start_play is being called")
    return {"graph_info":state["graph_info"]+"I am planing to play"}

def cricket(state:State):
    print("Cricket node is being called")
    return {"graph_info":state["graph_info"]+"cricket"}

def badminton(state:State):
    print("Badminton node is being called")
    return {"graph_info":state["graph_info"]+"badminton"}

import random
from typing import Literal

def random_playing(state:State)->Literal['cricket','badminton']:
    if random.random()>0.5:
        return "cricket"
    else : return "badminton"


from IPython.display import Image, display
from langgraph.graph import StateGraph, START,END

#Build Graph

graph=StateGraph(State) # empty graph
graph.add_node("start_play",start_play)
graph.add_node("cricket",cricket)
graph.add_node("badminton",badminton)

#scheduing the flow of the graph
graph.add_edge(START,"start_play")
graph.add_conditional_edges("start_play",random_playing)
graph.add_edge("cricket",END)
graph.add_edge("badminton",END)

built_graph=graph.compile() # compile the graph
res=built_graph.invoke({"graph_info":"Hey, My name is saurav"})
print(res)






