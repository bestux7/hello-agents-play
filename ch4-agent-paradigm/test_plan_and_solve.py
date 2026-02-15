""" Plan-And-Solve Agent 测试运行实例"""

from llm import HelloAgentsLLM
from agents import PlanAndSolveAgent

# 初始化LLM客户端
llm_client = HelloAgentsLLM()
agent = PlanAndSolveAgent(llm_client)
print(f"Plan-And-Solve Agent初始化完成,模型:{llm_client.model}")
# 调用agent run
question = " 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
response_txt = agent.run(question=question)



