# Reasoning and Action 推理与行动智能体ReAct 感知-思考-行动(调用工具)-观察-感知
# 优点：高可解释性(Thought链清晰)、动态规划与纠错能力(走一步看一步)、工具协同能力
# 缺点：对LLM能力强依赖、执行效率问题(多次调用LLM)、提示词脆弱(依赖提示词模块)、可能陷入局部最优(步进决策缺乏长远看能力)
# 核心优势：环境适应性、动态纠错能力 适用于探索性、需要外部工具输入的任务

import re
from llm import HelloAgentsLLM
from core import ToolExecutor
from prompts import REACT_PROMPT_TEMPLATE

class ReActAgent:
  def __init__(self, llm_client:HelloAgentsLLM, tool_executor:ToolExecutor, max_steps:int=5):
    self.llm_client = llm_client
    self.tool_executor = tool_executor
    self.max_steps = max_steps
    self.history = []

  def run(self, question:str):
    """
    运行智能体
    """
    self.history = [] # 每次运行时重置历史记录
    current_step = 0

    while current_step < self.max_steps:
      current_step += 1
      print(f"--- 第{current_step}步 ---")
      # 1.格式化提示词
      tools_desc = self.tool_executor.getAvailableTools()
      history_str = "\n".join(self.history)
      prompt = REACT_PROMPT_TEMPLATE.format(
        tools=tools_desc,
        question=question,
        history=history_str
      )
      # 2.调用LLM思考
      messages = [{"role":"user", "content":prompt}]
      response_txt = self.llm_client.think(messages=messages)
      if not response_txt:
        print("错误：LLM未能返回有效响应。")
        break
      # 3.解析思考结果 Thought-Action
      thought, action = self._parse_output(response_txt)
      if thought:
        print(f"思考：{thought}")
      if not action:
        print("警告：未能解析出有效的Action,流程终止。")
        break
      # 4.调用工具执行Action
      if action.startswith("Finish"):
        # 如果是Finish指令，提取最终答案并结束 
        final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
        print(f"🎉 最终答案：{final_answer}")
        return final_answer
      tool_name, tool_input = self._parse_action(action)
      if not tool_name or not tool_input:
        continue
      print(f"行动:{tool_name}[{tool_input}]")
      tool_function = self.tool_executor.getTool(tool_name)
      if not tool_function:
        observation = f"错误：未找到名为'{tool_name}'的工具"
      else:
        # 执行行动，得到观察
        observation = tool_function(tool_input)
      # 5.整合观察结果
      print(f"👀 观察:")
      print(observation)
      # 将本轮的action和observation添加到history中
      self.history.append(f"Action:{action}")
      self.history.append(f"Observation:{observation}")

    # 循环结束
    print("已达到最大步数，流程终止。")
    return None

  def _parse_output(self, text: str):
      """解析LLM的输出，提取Thought和Action。"""
      thought_match = re.search(r"Thought: (.*)", text)
      action_match = re.search(r"Action: (.*)", text)
      thought = thought_match.group(1).strip() if thought_match else None
      action = action_match.group(1).strip() if action_match else None
      return thought, action

  def _parse_action(self, action_text: str):
      """解析Action字符串，提取工具名称和输入。"""
      match = re.match(r"(\w+)\[(.*)\]", action_text)
      if match:
          return match.group(1), match.group(2)
      return None, None

    
    