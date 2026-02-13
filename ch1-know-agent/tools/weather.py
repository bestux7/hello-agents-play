# tools/weather.py
"""
天气工具类
"""

import re
import requests
import json

def get_weather(city: str) -> str:
  """
  通过调用 wttr.in API 查询真实的天气信息
  """
  # API端点
  url = f"https://wttr.in/{city}?format=j1"

  try:
    # 调用API请求，获取返回数据
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # 解析数据，获取天气描述和温度信息
    current_condition = data['current_condition'][0]
    weather_desc = current_condition['weatherDesc'][0]['value']
    temp_c = current_condition['temp_C']
    # 返回格式化的天气信息(自然语言)
    return f"{city}当前天气:{weather_desc},气温{temp_c}℃"

  # 异常处理
  except requests.exceptions.RequestException as e:
    return f"错误：查询天气时遇到网络问题 - {e}"
  except (KeyError,IndexError) as e:
    return f"错误：解析天气数据时遇到问题,可能是城市名无效 - {e}"



