""" 自定义MCP服务——天气查询 """
from typing import Dict
from dotenv import load_dotenv
load_dotenv()

import json, requests
from datetime import datetime

from hello_agents.protocols import MCPServer

# 创建MCP服务器
weather_server = MCPServer(name="weather_server", description="真实天气查询服务")

CITY_MAP = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou",
    "深圳": "Shenzhen", "杭州": "Hangzhou", "成都": "Chengdu",
    "重庆": "Chongqing", "武汉": "Wuhan", "宁波": "Ningbo",
    "南京": "Nanjing", "长春": "Changchun", "苏州": "Suzhou"
}

def get_weather_data(city: str) -> Dict[str, str]:
    """ 通过调用 wttr.in API 获取天气数据 """
    city_en = CITY_MAP.get(city, city)
    url = f"https://wttr.in/{city_en}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current_condition"][0]

    return {
        "city": city,
        "temperature": float(current["temp_c"]),
        "feels_like": float(current["FeelsLikeC"]),
        "humidity": int(current["humidity"]),
        "condition": current["weatherDesc"][0]["value"],
        "wind_speed": round(float(current["windspeedKmph"]) / 3.6, 1),
        "visibility": float(current["visibility"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_weather(city: str) -> str:
    """ 获取指定城市的天气信息 返回json """
    try:
        weather_data = get_weather_data(city=city)
        return json.dumps(weather_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "city": city}, ensure_ascii=False)

def list_supported_cities() -> str:
    """列出所有支持的中文城市"""
    result = {"cities": list(CITY_MAP.keys()), "count": len(CITY_MAP)}
    return json.dumps(result, ensure_ascii=False, indent=2)

def get_server_info() -> str:
    """获取服务器信息"""
    info = {
        "name": "Weather MCP Server",
        "version": "1.0.0",
        "tools": ["get_weather", "list_supported_cities", "get_server_info"]
    }
    return json.dumps(info, ensure_ascii=False, indent=2)

# 工具注册到服务器
weather_server.add_tool(get_weather)
weather_server.add_tool(list_supported_cities)
weather_server.add_tool(get_server_info)

if __name__ == "__main__":
    weather_server.run()

    # 临时测试：直接调用 server 脚本里的函数
    # import sys
    # sys.path.insert(0, '.')
    # print(get_weather("苏州"))  # 先验证函数本身
    # # print(get_server_info())