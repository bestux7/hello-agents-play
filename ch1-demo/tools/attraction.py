# tools/Attraction.py
"""
景点工具类
"""
import os
import re
from sys import exception
from tavily import TavilyClient
import tavily

def get_attraction(city: str, weather: str) -> str:
  """
  根据城市和天气，调用Tavily Search API搜索景点推荐
  """
  # 1.配置api_key
  api_key = os.environ.get("TAVILY_API_KEY")
  if not api_key:
    return "错误：未配置TAVILY_API_KEY环境变量."
  # 2.初始化TavilyClient客户端
  tavily = TavilyClient(api_key=api_key)
  # 3.构建查询语句
  query = f"'{city}'在'{weather}'天气下最值得去的景点推荐及理由"
  
  try:
    # 4.调用客户端查询并获取结果
    response = tavily.search(query=query, search_depth="basic", include_answer=True)
    if response.get("answer"):
      return response["answer"]
    # 5.如果没有综合性回答结果，则格式化原始结果
    formatted_results = []
    for result in response.get("results",[]): # response.get(key,defaultValue) 从字典中获取key为"results"的值，如果没有返回[]
      formatted_results.append(f"-{result['title']}:{result['content']}")
    # 返回结果
    if not formatted_results:
      return "抱歉，没有找到相关的旅游景点推荐."
    return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)
  # 异常处理
  except Exception as e:
    return f"错误：执行Tavily搜索时出现网络问题 - {e}"
