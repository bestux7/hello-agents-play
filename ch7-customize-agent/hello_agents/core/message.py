""" 消息系统 """
from datetime import datetime
from nt import times
from sqlite3.dbapi2 import Timestamp
from time import sleep
from typing import Any, Dict, List, Literal
from pydantic import BaseModel

MessageRole = Literal["user", "system", "assistant", "tool"]

class Message(BaseModel):
    """ 消息类 """
    role: MessageRole
    content: str
    timestamp: datetime = None
    metadata: List[Dict[str, Any]] = None

    def __init__(self, content: str, role: MessageRole, **kwagrs) -> None:
        super().__init__(
            content=content,
            role=role,
            timestamp=kwagrs.get("timestamp", datetime.now()),
            metadata=kwagrs.get("metadata", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（OpenAI API格式）"""
        return {
            "role": self.role,
            "content": self.content
        }

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"


