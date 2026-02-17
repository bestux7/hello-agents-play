""" 反思智能体 Reflection Agent 初始行动->循环(反思->优化)->结果"""
# 执行-反思-优化 迭代循环
# 核心优势：高质量、可靠性、鲁棒性。典型的用成本换质量，token消耗大，任务耗时长，提示复杂，适用于对结果的可靠性和准确性有极高要求的场景。

from llm import HelloAgentsLLM
from memory import Memory
from prompts import INITIAL_PROMPT_TEMPLATE, REFLECT_PROMPT_TEMPLATE, REFINE_PROMPT_TEMPLATE

class ReflectionAgent:
  def __init__(self, llm_client: HelloAgentsLLM, max_iterations=3) -> None:
    self.llm_client = llm_client
    self.memory = Memory()
    self.max_iterations = max_iterations

  def run(self, task: str):
    print(f"\n--- 开始处理任务 ---\n任务: {task}")
    
    # 1.初始执行任务
    print("\n--- 正在进行初始尝试 ---")
    initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
    initial_code = self._get_llm_response(initial_prompt)
    self.memory.add_record("execution", initial_code)

    # 2.反思与优化
    for i in range(self.max_iterations):
      print(f"\n--- 第 {i+1}/{self.max_iterations} 轮迭代 ---")
      # a.反思
      print("\n-> 正在进行反思...")
      last_code = self.memory.get_last_execution()
      reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=task, code=last_code)
      feedback = self._get_llm_response(reflect_prompt)
      self.memory.add_record("reflection", feedback)

      # b.检查是否需要停止 终止条件
      if "无需改进" in feedback:
        print("\n✅ 反思认为代码已无需改进，任务完成。")
        break

      # c.优化
      print("\n-> 正在进行优化...")
      refine_prompt = REFINE_PROMPT_TEMPLATE.format(task=task, last_code_attempt=last_code, feedback=feedback)
      refined_code = self._get_llm_response(refine_prompt)
      self.memory.add_record("execution", refined_code)
    
    # 3.结束，返回最后生成的代码
    final_code = self.memory.get_last_execution()
    print(f"\n--- 任务完成 ---\n最终生成的代码:\n```python\n{final_code}\n```")
    return final_code


  def _get_llm_response(self, prompt: str) -> str:
    """ 辅助方法，用于构建msg并调用LLM获取响应 """
    messages = [{"role": "user", "content": prompt}]
    response_txt = self.llm_client.think(messages) or ""
    return response_txt