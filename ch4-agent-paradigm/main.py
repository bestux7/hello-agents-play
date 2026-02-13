""" 运行实例 """
from agents import ReActAgent
from llm import HelloAgentsLLM
from core import ToolExecutor
from tools import search

# 注册加载工具
tool_executor = ToolExecutor()
search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
tool_executor.registerTool("search", search_description, search)

# 初始化agent
llm_client = HelloAgentsLLM()
max_steps = 5
agent = ReActAgent(llm_client, tool_executor, max_steps)
print(f"agent初始化完毕，模型：{llm_client.model},最大思考轮数：{max_steps}")

# run agent
question = "BTC最新价格是多少"
print(f"开始提问，问题：{question}")
result = agent.run(question)
