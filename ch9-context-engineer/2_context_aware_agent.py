""" 具有上下文感知能力的 Agent """
from nt import system
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

from hello_agents import HelloAgentsLLM, Message, SimpleAgent
from hello_agents.tools import MemoryTool, RAGTool
from hello_agents.context import ContextBuilder, ContextConfig

class ContextAwareAgent(SimpleAgent):
    """ 具有上下文感知能力的 Agent 
        使用context_builder构建上下文(用户查询、对话历史、系统指示、工具(MemoryTool和RAGTool))optimized_context，
        作为更强大的系统消息传给LLM
    """

    def __init__(self, name: str, llm: HelloAgentsLLM, **kwargs):
        super().__init__(name=name, llm=llm, system_prompt=kwargs.get("system_prompt", ""))
        # 初始化工具
        self.memory_tool = MemoryTool(user_id=kwargs.get("user_id", "default_user"))
        self.rag_tool = RAGTool(knowledge_base_path=kwargs.get("knowledge_base_path", "./kb"))
        # 初始化上下文构建器
        self.context_builder = ContextBuilder(config=ContextConfig(max_tokens=4000), memory_tool=self.memory_tool, rag_tool=self.rag_tool)
        # 对话历史
        self.conversation_history = []

    def run(self, user_input: str) -> str:
        """ 运行 """
        # 构建上下文
        optimized_context = self.context_builder.build(
            user_query=user_input,
            conversation_history=self.conversation_history,
            system_instructions=self.system_prompt
        )
        # 构建消息
        messages = [
            {"role": "system", "content": optimized_context},
            {"role": "user", "content": user_input}
        ]
        response = self.llm.invoke(messages)
        # 添加到对话历史
        self.conversation_history.append(Message(role="user", content=user_input, timestamp=datetime.now()))
        self.conversation_history.append(Message(role="assistant", content=response, timestamp=datetime.now()))
        # 添加重要交互到记忆系统
        self.memory_tool.execute(
            "add",
            content=f"Q: {user_input}\nA: {response[:200]}...",  # 摘要
            memory_type="episodic",
            importance=0.6
        )
        return response

# 使用示例
agent = ContextAwareAgent(
    name="Python数据分析顾问", 
    llm=HelloAgentsLLM(), 
    system_prompt="你是一位资深的Python数据工程顾问。",
    user_id="user123",
    knowledge_base_path="./data_science_kb"
)
response = agent.run("如何优化Pandas的内存占用?")
print(response)
