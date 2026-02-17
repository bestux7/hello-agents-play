""" Reflection Agent 测试运行实例 """

from agents import ReflectionAgent
from llm import HelloAgentsLLM

llm_client = HelloAgentsLLM()
agent = ReflectionAgent(llm_client)
print(f"Reflection Agent 初始化完成，模型：{llm_client.model}")

task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"
# task = "编写一个Python函数，对一个列表进行排序，采用快速排序算法"
agent.run(task=task)

