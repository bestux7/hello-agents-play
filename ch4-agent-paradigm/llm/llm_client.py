import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
  """
  "Hello Agents"定制的LLM客户端
  用于调用任何兼容OpenAI接口的服务，默认使用流式响应
  """
  def __init__(self, model:str=None, apiKey:str=None, baseUrl:str=None, timeout:int=None):
    """
    初始化客户端，优先使用传入参数，其次从环境变量加载
    """
    self.model = model or os.getenv("LLM_MODEL_ID")
    apiKey = apiKey or os.getenv("LLM_API_KEY")
    baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
    timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
    
    if not all([self.model, apiKey, baseUrl]):
      raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
    self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

  def think(self, messages:List[Dict[str:str]], temperature:float=0) -> str:
    """
    调用大语言模型思考，返回响应
    """
    print(f"🧠 正在调用{self.model}模型...")
    try:
      # 调用client生成回应
      response = self.client.chat.completions.create(
        messages=messages,
        model=self.model,
        temperature=temperature,
        stream=True,
      )
      # 处理流式响应 一行行刷出
      print("✔ 大语言模型响应成功：")
      collected_content = []
      for chunk in response:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        collected_content.append(content)
      print() # 流式输出结束后换行
      return "".join(collected_content)

    except Exception as e:
      print(f"❌ 调用LLM API时发生错误：{e}")
      return None

# -----客户端使用示例-----
# if __name__=='__main__':
#   try:
#     llmClient = HelloAgentsLLM()
#     examplemsgs = [
#       {"role": "system", "content": "You are a helpful assistant that writes Python code."},
#       {"role": "user", "content": "写一个快速排序算法"}
#     ]
#     print("----调用LLM----")
#     responseText = llmClient.think(examplemsgs, temperature=0)
#     if responseText:
#       print("\n\n----完整模型响应----")
#       print(responseText)
#   except ValueError as e:
#     print(e)

