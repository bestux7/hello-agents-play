"""Reflection Agent实现 - 自我反思与迭代优化的智能体"""

# 默认提示词模板
from typing import Any, Dict, List, Optional

from core.agent import Agent
from core.config import Config
from core.llm import HelloAgentsLLM
from core.message import Message


DEFAULT_PROMPTS = {
    "initial": """
请根据以下要求完成任务：

任务: {task}

请提供一个完整、准确的回答。
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间：

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。
""",
    "refine": """
请根据反馈意见改进你的回答：

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。
"""
}

class Memory:
    """
    简单的短期记忆模块，用于存储智能体的行动与反思轨迹。
    """
    def __init__(self) -> None:
        # 初始化记忆列表
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: Any):
        """ 添加一条记录 """
        self.records.append({"type": record_type, "content": content})
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """ 获取所有记忆拼接成的字符串文本 """
        trajectory = ""
        for record in self.records:
            if record["type"] == "execution":
                trajectory += f"--- 上一轮尝试 (代码) ---\n{record['content']}\n\n"
            elif record["type"] == "reflection":
                trajectory += f"--- 评审员反馈 ---\n{record['content']}\n\n"
        return trajectory.strip()

    def get_last_execiton(self) -> str:
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return ""

class ReflectionAgent(Agent):
    """
    Reflection Agent - 自我反思与迭代优化的智能体

    这个Agent能够：
    1. 执行初始任务
    2. 对结果进行自我反思
    3. 根据反思结果进行优化
    4. 迭代改进直到满意

    特别适合代码生成、文档写作、分析报告等需要迭代优化的任务。

    支持多种专业领域的提示词模板，用户可以自定义或使用内置模板。
    """
    def __init__(
        self, 
        name: str, 
        llm: HelloAgentsLLM, 
        system_prompt: Optional[str]=None, 
        config: Optional[Config]=None,
        max_iterations: int = 3,
        custom_prompt: Optional[Dict[str, str]]=None
    ):
        super().__init__(name, llm, system_prompt, config)
        self.max_iterations = max_iterations
        self.prompt_template = custom_prompt if custom_prompt else DEFAULT_PROMPTS

        self.memory = Memory()

    def run(self, input_text: str, **kwargs) -> str:
        print(f"\n🤖 {self.name} 开始处理任务: {input_text}")
        # 重置记忆
        self.memory = Memory()

        # 1.初始执行
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.prompt_template["initial"].format(task=input_text)
        initial_result = self._get_llm_response(initial_prompt)
        # 加入记忆
        self.memory.add_record("execution", initial_result)

        # 2.反思-优化循环
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i+1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思
            print("\n-> 正在进行反思...")
            last_execution = self.memory.get_last_execiton()
            reflect_prompt = self.prompt_template["reflect"].format(task=input_text, content=last_execution)
            feedback = self._get_llm_response(reflect_prompt)
            self.memory.add_record("reflection", feedback)

            # b. 检查终止条件
            if "无需改进" in feedback or "no need for improvement" in feedback.lower():
                print("\n✅ 反思认为结果已无需改进，任务完成。")
                break

            # c. 优化
            refine_prompt = self.prompt_template["refine"].format(task=input_text, last_attempt=last_execution, feedback=feedback)
            refined_results = self._get_llm_response(refine_prompt)   
            self.memory.add_record("execution", refined_results)
        
        # 获取最后结果
        final_result = self.memory.get_last_execiton()       
        print(f"\n--- 任务完成 ---\n最终结果:\n{final_result}")

        # 保存到历史记录
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_result, "assistant"))

        return final_result  
        

    def _get_llm_response(self, prompt:str, **kwargs) -> str:
        """ 调用LLM获取响应 """
        # 构建message
        messages = [{"role": "user", "content": prompt}]
        return self.llm.invoke(messages, **kwargs) or ""
