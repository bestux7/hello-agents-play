"""Plan and Solve Agent实现 - 分解规划与逐步执行的智能体"""

import ast
from typing import Dict, List, Optional
from core.llm import HelloAgentsLLM
from core.agent import Agent
from core.message import Message
from core.config import Config

# 默认规划器提示词模板
DEFAULT_PLANNER_PROMPT = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

# 默认执行器提示词模板
DEFAULT_EXECUTOR_PROMPT = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决"当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对"当前步骤"的回答:
"""

class Planner:
    """规划器 - 负责将复杂问题分解为简单步骤"""
    def __init__(self, llm: HelloAgentsLLM, prompt_template: Optional[str]=None) -> None:
        self.llm = llm
        self.prompt_template = prompt_template if prompt_template else DEFAULT_PLANNER_PROMPT

    def plan(self, question:str, **kwargs) -> List[str]:
        """ 生成执行计划 """
        # 构建提示词
        prompt = self.prompt_template.format(question=question)
        messages = [{"role": "user", "content": prompt}]
        print("--- 正在生成计划 ---")
        response_txt = self.llm.invoke(messages=messages, **kwargs) or ""
        print(f"✅ 计划已生成:\n{response_txt}")

        try:
            # 提取Python代码块中的计划字符串
            plan_str = response_txt.split("```python")[1].split("```")[0].strip()
            # 获取计划列表
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_txt}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []

class Executor:
    """执行器 - 负责按计划逐步执行"""
    def __init__(self, llm: HelloAgentsLLM, prompt_template: Optional[str]=None) -> None:
        self.llm = llm
        self.prompt_template = prompt_template if prompt_template else DEFAULT_EXECUTOR_PROMPT

    def execute(self, question: str, plan: list[str], **kwargs) -> str:
        """ 按计划执行任务 """
        history = ""
        final_answer = ""
        print("\n--- 正在执行计划 ---")
        for i, step in enumerate(plan, 1):
            print(f"\n-> 正在执行步骤 {i}/{len(plan)}: {step}")
            prompt = self.prompt_template.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step
            )
            messages = [{"role": "user", "content": prompt}]
            response_txt = self.llm.invoke(messages, **kwargs)
            history += f"步骤 {i}: {step}\n结果: {response_txt}\n\n"
            print(f"✅ 步骤 {i} 已完成，结果: {final_answer}")

        final_answer = response_txt
        return final_answer

class PlanAndSolveAgent(Agent):
    """
    Plan and Solve Agent - 分解规划与逐步执行的智能体
    
    这个Agent能够：
    1. 将复杂问题分解为简单步骤
    2. 按照计划逐步执行
    3. 维护执行历史和上下文
    4. 得出最终答案
    
    特别适合多步骤推理、数学问题、复杂分析等任务。
    """
    def __init__(
        self, 
        name: str, 
        llm: HelloAgentsLLM, 
        system_prompt: Optional[str]=None, 
        config: Optional[Config]=None,
        custom_prompt: Optional[Dict[str, str]]=None
    ):
        super().__init__(name, llm, system_prompt, config)
        # 初始化提示词模板
        if custom_prompt:
            planner_prompt = custom_prompt["planner"]
            executor_prompt = custom_prompt["executor"]
        else:
            planner_prompt = None
            executor_prompt = None
        # 初始化Planner和Executor
        self.planner = Planner(llm, planner_prompt)
        self.executor = Executor(llm, executor_prompt)

    def run(self, input_text: str) -> str:
        """ 运行Plan and Solve Agent """
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")
        # 生成计划
        plan = self.planner.plan(input_text)
        if not plan:
            final_answer = "无法生成有效的行动计划，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "assistant"))
            return final_answer

        # 执行计划
        final_answer = self.executor.execute(input_text, plan)
        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))

        return final_answer




