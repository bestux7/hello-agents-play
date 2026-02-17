""" Plan-And-Solve规划执行智能体 """

# 先规划、再执行。将任务分解为清晰的步骤，再逐一执行
# 核心优势：结构性、稳定性 适用于处理结构性强、可以被清晰分解的复杂逻辑任务

from llm import HelloAgentsLLM
from planners import Planner
from solvers import Executor

class PlanAndSolveAgent:
  def __init__(self, llm_client: HelloAgentsLLM):
    """ 初始化智能体，创建规划和执行器 """
    self.llm_client = llm_client
    self.planner = Planner(llm_client)
    self.executor = Executor(llm_client)

  def run(self, question: str) -> str:
    """ 运行智能体，先规划再执行，返回结果 """
    print(f"\n--- 开始处理问题 ---\n问题：{question}")

    # 1.planner生成计划
    plan = self.planner.plan(question)
    if not plan:
      print("\n--- 任务终止--- \n无法成功有效的行动计划")
      return
    # 2.调用执行器执行
    final_answer = self.executor.execute(question, plan)
    print(f"\n--- 任务完成 --- \n最终答案：{final_answer}")
