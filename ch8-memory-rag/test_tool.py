""" 测试Memory和Rag工具 """
from dotenv import load_dotenv
load_dotenv()

from hello_agents import HelloAgentsLLM, SimpleAgent, ToolRegistry
from hello_agents.tools import MemoryTool, RAGTool


# 创建LLM实例
llm = HelloAgentsLLM()

# 创建agent
agent = SimpleAgent(
    name="智能助手",
    llm=llm,
    system_prompt="你是一个有记忆和知识检索能力的AI助手"
)

# 创建工具注册表
tool_registry = ToolRegistry()
# 添加记忆工具
memory_tool = MemoryTool(user_id="user123")
tool_registry.register_tool(memory_tool)
# 添加Rag工具
rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
tool_registry.register_tool(rag_tool)

agent.tool_registry = tool_registry

response = agent.run("你好，请记住我是Bing，我正在学习AI Agent开发")
print(response)

