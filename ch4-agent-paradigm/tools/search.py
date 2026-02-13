# search 工具
import os
from serpapi import SerpApiClient

def search(query:str) -> str:
  """
  基于serpApi的网页搜索引擎工具，可以智能解析搜索结果，优先返回直接答案或知识图谱信息。
  """
  print(f"🔍 正在执行[serpApi]网页搜索：{query}")
  try:
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
      return "错误:SERPAPI_API_KEY未在 .env文件中配置"
    # 创建client通信返回结果
    params = {
      "engine": "google",
      "q": query,
      "api_key": api_key,
      "gl": "cn",   # 国家代码
      "hl": "zh-cn",  # 语言代码
    }
    client = SerpApiClient(params)
    results = client.get_dict()

    # 智能解析结果：优先寻找最直接的答案
    if "answer_box_list" in results:
      return "\n".join(results["answer_box_list"])
    if "answer_box" in results and "answer" in results["answer_box"]:
      return results["answer_box"]["answer"]
    if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
      return results["knowledge_graph"]["description"]
    # 如果没有直接答案，返回前三个有机结果的摘要
    if "organic_results" in results and results["organic_results"]:
      snippets = [
        f"[{i+1} {res.get('title','')}\n{res.get('snippet','')}]"
        for i, res in enumerate(results["organic_results"][:3])
      ]
      return "\n\n".join(snippets)
  
  except Exception as e:
    return f"搜索时发生错误：{e}"

