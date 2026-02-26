# demo.py
import re
import os

from llm import OpenAICompatibleClient
from prompts import AGENT_SYSTEM_PROMPT
from tools import available_tools
from dotenv import load_dotenv

# Agent-Loop:感知-思考(规划、选择工具)-行动-观察-感知...

# 1.配置LLM客户端
load_dotenv() # 加载.env文件环境变量

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

llm = OpenAICompatibleClient(
  model=MODEL_NAME,
  api_key=API_KEY,
  base_url=BASE_URL
)
print(f"使用LLM模型：{MODEL_NAME}\n" + "="*40)

# 2.初始化prompt
user_prompt = "你好，请帮我查询一下今天长春的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求：{user_prompt}"]
print(f"用户输入：{user_prompt}\n" + "="*40)

# 3.运行主循环
for i in range(5): # 最大循环次数5次
  print(f"---循环{i+1}---\n")
  # 3.1构建prompt
  full_prompt = "\n".join(prompt_history)

  # 3.2调用LLM进行思考
  llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
  # 模型可能会输出多余的Thought-Action，需要截断，只要第一组
  match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
  # 通配的match对：Thought: 用户想知道北京的天气，我需要先调用get_weather工具  Action: get_weather(city="北京")
  if match:
    truncated = match.group(1).strip()
    if truncated != llm_output.strip():
      llm_output = truncated
      print("已截断多余的Thought-Action对")
  print(f"模型输出:\n{llm_output}]\n")
  prompt_history.append(llm_output) # 思考输出拼接到提示词历史中

  # 3.3解析llm_output(Thought-Action对)并执行行动
  action_match = re.search(r"Action:(.*)", llm_output, re.DOTALL)
  if not action_match:
    print("解析错误：模型输出中未找到Action.")
    break
  action_str = action_match.group(1).strip()  # 'Action: get_weather(city="北京")'

  if action_str.startswith("finish"):
    final_answer = re.search('finish\(answer="(.*)"\)', action_str).group(1)
    print(f"任务完成，最终答案：{final_answer}")
    break
  # 工具名、参数字符串、参数键值对
  tool_name = re.search(r"(\w+)\(", action_str).group(1)  # get_weather
  args_str = re.search(r"\((.*)\)", action_str).group(1)  #'city="北京"'
  kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str)) # {'city': '北京'}
  # 调用工具执行参数
  if tool_name in available_tools:
    observation = available_tools[tool_name](**kwargs)  # **kwargs字典解包
  else:
    observation = f"错误:未定义的工具'{tool_name}'"

  # 3.4 记录观察结果
  observation_str = f"Observation:{observation}"
  print(f"{observation_str}\n" + "="*40)
  prompt_history.append(observation_str)  # 观察结果拼接到提示词历史中




