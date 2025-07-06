from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import uuid
from typing import List, Dict, Optional

def get_or_create_session_id(session_id: Optional[str]) -> str:
    """Return the provided session_id or generate a new one."""
    return session_id or str(uuid.uuid4())

def history_to_lc_messages(history: List[Dict]) -> List[BaseMessage]:
    """Convert chat history from DB to LangChain message objects."""
    messages = []
    for i in range(0, len(history), 2):
        if i < len(history):
            messages.append(HumanMessage(content=history[i]["content"]))
        if i + 1 < len(history):
            messages.append(AIMessage(content=history[i + 1]["content"]))
    return messages

def append_message(history: List[BaseMessage], message: BaseMessage) -> List[BaseMessage]:
    """Return a new list with the message appended."""
    return history + [message] 