# llm/client.py
"""
openai模型调用
"""
from openai import OpenAI

class OpenAICompatibleClient:
  """
  适配OpenAI接口的大模型客户端
  """

  def __init__(self, model: str, api_key: str, base_url: str):
    # 构造器，初始化参数，创建好client来调用OpenAI
    self.model = model
    self.client = OpenAI(api_key=api_key, base_url=base_url)
  
  def generate(self, prompt: str, system_prompt: str) -> str:
    """调用LLM API来生成回应"""
    print("正在调用大模型...")
    try:
      # 构建messages
      messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
      ]
      # client向model发出消息，得到response
      response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        stream=False
      )
      # 返回结果
      answer = response.choices[0].message.content
      print("大语言模型响应成功.")
      return answer
    except Exception as e:
      print(f"调用LLM模型 API时发生错误:{e}")
      return "错误：调用LLM服务时出错."
    