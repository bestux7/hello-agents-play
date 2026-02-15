""" 
智能体中的Plan-And-Solve范式，其中的Planner模块
"""
import ast

from llm import HelloAgentsLLM
from prompts import PLANNER_PROMPT_TEMPLATE

class Planner:
  def __init__(self, llm_client: HelloAgentsLLM):
    self.llm_client = llm_client

  def plan(self, question: str) -> list[str]:
    """ 根据用户问题生成一个行动计划 """
    # 准备提示词和messages
    prompt = PLANNER_PROMPT_TEMPLATE.format(question = question)
    messages = [{"role": "user", "content": prompt}]
    print("---正在生成计划---")
    # 调用LLM
    response_txt = self.llm_client.think(messages) or ""
    print(f"√ 计划已生成：\n{response_txt}")
    # 解析LLM输出的列表字符串
    try:
      plan_str = response_txt.split("```python")[1].split("```")[0].strip()
      plan = ast.literal_eval(plan_str) # 使用ast.literal_eval()安全的解析字符串为python列表
      return plan if isinstance(plan, list) else []
    except (ValueError, SyntaxError, IndexError) as e:
      print(f"X 解析计划时出错：{e}")
      print(f"原始响应：{response_txt}")
    except Exception as e:
      print(f"X 解析计划时发生未知错误：{e}")
      return []
