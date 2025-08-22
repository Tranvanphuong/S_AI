
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from main import basic_agent, get_current_time

from IPython.display import Image, display

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def ask(state: State):
    return {"messages": [basic_agent.invoke(state["messages"])]}
graph_builder.add_node("ask", ask)

graph_builder.add_edge(START, "ask")
graph_builder.add_edge("ask", END)
basic_agent_graph = graph_builder.compile()

try:
    display(Image(basic_agent_graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

def ask_basic_agent(messages: list):
    print("Human: " + messages[-1]["content"])

    for event in basic_agent_graph.stream({"messages": messages}):
        for value in event.values():
            print("AI:", value["messages"][-1].content)

question = [{
                "role": "system",
                "content": "Bạn là AVA, trợ lý số của công ty cổ phần MISA.",
            },
             {
                "role": "system",
                "content": f'''Thông tin bổ sung:
                            - Thời gian hiện tại: {get_current_time()}''',
            },
            {
                "role": "user",
                "content": "Cho tôi biết thời gian hiện tại?",
            }]
ask_basic_agent(question)