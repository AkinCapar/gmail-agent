from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    It holds the conversation history (messages) between the user, the AI, and the Tools.
    The 'add_messages' reducer ensures new messages are appended to the list, not overwritten.
    """
    messages: Annotated[list, add_messages]