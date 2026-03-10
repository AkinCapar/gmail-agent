import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from gmail_agent.client.state import GraphState
from gmail_agent.server.mcp_server import get_latest_emails, send_email

load_dotenv()

from langchain_core.tools import tool

@tool
def tool_get_latest_emails(max_results: int = 5) -> str:
    """Reads and summarizes the latest emails from the user's INBOX."""
    return get_latest_emails(max_results)

@tool
def tool_send_email(to: str, subject: str, body: str) -> str:
    """Sends an email to the specified address with the given subject and body."""
    return send_email(to, subject, body)

tools = [tool_get_latest_emails, tool_send_email]

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: GraphState):
    """The AI brain processes the messages and decides whether to reply or use a tool."""
    messages = state["messages"]
    
    sys_msg = {
        "role": "system", 
        "content": "You are a highly capable and professional Executive Assistant. "
                   "You manage the user's Gmail account. Always confirm tool executions clearly."
    }
    
    response = llm_with_tools.invoke([sys_msg] + messages)
    return {"messages": [response]}

workflow = StateGraph(GraphState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")

def should_continue(state: GraphState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue, ["tools", END])

workflow.add_edge("tools", "agent")

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")