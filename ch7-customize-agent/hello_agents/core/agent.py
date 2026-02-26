""" Agent抽象基类 """

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from .llm import HelloAgentsLLM
from .config import Config
from .message import Message

class Agent(ABC):
    """ Agent抽象基类 """
    def __init__(
        self, 
        name: str, 
        llm: HelloAgentsLLM, 
        system_prompt: Optional[str]=None, 
        config: Optional[Config]=None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history = List[Message] = []

    # 抽象方法
    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """ 抽象方法，子类必须实现 run 方法 """
        pass

    # 公用方法
    def add_message(self, message: Message):
        """ 添加消息到历史记录中 """
        self._history.append(message)

    def clear_history(self):
        """ 清空历史记录 """
        self._history.clear()

    def get_history(self) -> List[Message]:
        """ 获取历史记录 """
        return self._history.copy()

    def __str__(self) -> str:
        return f"Agent(name={self.name}, provider={self.llm.provider})"


