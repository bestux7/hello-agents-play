""" 
智能体中的Plan-And-Solve范式，其中的Solver模块
"""
from llm import HelloAgentsLLM
from prompts import EXECUTOR_PROMPT_TEMPLATE

class Executor:
  def __init__(self, llm_client: HelloAgentsLLM):
    self.llm_client = llm_client

  def execute(self, question: str, plan: list[str]) -> str:
    """ 根据plan逐步solve执行解决问题 """
    history = "" # 用于存储历史步骤和结果的字符串
    print("\n---正在执行计划---")

    # 遍历执行plan步骤
    for i, step in enumerate(plan):
      print(f"\n -> 正在执行步骤{i+1}/{len(plan)}: {step}")
      # 构建提示词和消息
      prompt = EXECUTOR_PROMPT_TEMPLATE.format(question=question, plan=plan, history=history, current_step=step)
      messages = [{"role": "user", "content": prompt}]
      # 调用大模型,获取当前步结果
      response_txt = self.llm_client.think(messages) or ""

      # 更新历史记录，为下一步做准备
      history += f"步骤{i+1}：{step}\n结果：{response_txt}\n\n"
      print(f"步骤{i+1} 已完成，结果：{response_txt}")
    
    # 循环结束，输出答案
    final_answer = response_txt
    return final_answer
      