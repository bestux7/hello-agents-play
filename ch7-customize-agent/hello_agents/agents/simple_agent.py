""" 简单Agent """

from typing import Optional
from core.agent import Agent
from core.message import Message
from core.llm import HelloAgentsLLM
from core.config import Config

class SimpleAgent(Agent):
    """ 简单Agent """
    def __init__(
        self, 
        name: str, 
        llm: HelloAgentsLLM, 
        system_prompt: Optional[str]=None, 
        config: Optional[Config]=None
    ):
        super().__init__(name, llm, system_prompt, config)

    # 重写run方法
    def run(self, input_text: str, **kwargs) -> str:
        """ 运行Agent """
        # 拼接获取完整message
        messages = []
        messages.append(Message(content=self.system_prompt, role="system"))
        for msg in self.get_history():
            messages.append(Message(content=msg.content, role=msg.role))
        messages.append(Message(content=input_text, role="user"))
        # 调用Llm获取结果
        response = self.llm.invoke(messages, **kwargs)
        # 结果加入消息历史
        self.add_message(Message(content=input_text, role="user"))
        self.add_message(Message(content=response, role="assistant"))
        return response

    # 流式运行
    def stream_run(self, input_text: str, **kwargs):
        """ 流式运行 """
        # 拼接获取完整message
        messages = []
        messages.append(Message(content=self.system_prompt, role="system"))
        for msg in self.get_history():
            messages.append(Message(content=msg.content, role=msg.role))
        messages.append(Message(content=input_text, role="user"))
        # 调用llm 流式接口获得结果
        full_response = ""
        for chunk in self.llm.stream_invoke(messages, **kwargs):
            full_response += chunk
            yield chunk

        # 结果加入消息历史
        self.add_message(Message(content=input_text, role="user"))
        self.add_message(Message(content=full_response, role="assistant"))
        
