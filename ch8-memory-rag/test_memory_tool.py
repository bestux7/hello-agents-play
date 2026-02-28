""" 测试记忆工具 """
from dotenv import load_dotenv
from pydantic.type_adapter import P
load_dotenv()

from hello_agents import HelloAgentsLLM, SimpleAgent, ToolRegistry
from hello_agents.tools import MemoryTool

llm = HelloAgentsLLM()
agent = SimpleAgent(
    name="记忆助手",
    system_prompt="你是一个记忆助手，你的任务是帮助用户记住信息。",
    llm=llm
)

# 注册记忆工具给agent
memory_tool = MemoryTool(user_id="user123")
tool_registry = ToolRegistry()
tool_registry.register_tool(memory_tool)
agent.tool_registry = tool_registry

# 存储记忆
print("存储记忆...")
result1 = memory_tool.execute("add", content="bing是一个后端开发工程师，主要技术栈是Python和Java，目前主攻Agent开发方向。", memory_type="semantic", importance=0.8)
print(f"记忆1: {result1}")

result2 = memory_tool.execute("add", content="leighton是一个前端开发工程师，主要技术栈是JavaScript和TypeScript，目前主攻Web开发方向。", memory_type="semantic", importance=0.6)
print(f"记忆2: {result2}")

result3 = memory_tool.execute("add", content="mimi是一个产品经理，负责产品规划，目前主攻产品方向。mimi和Bing是恋人。", memory_type="semantic", importance=0.7)
print(f"记忆3: {result3}")

# 查询记忆
print("搜索记忆...")
result = memory_tool.execute("search", query="Bing", limit=3)
print(f"搜索结果: {result}")

# 记忆摘要
print("记忆摘要...")
result = memory_tool.execute("summary")
print(f"记忆摘要: {result}")
