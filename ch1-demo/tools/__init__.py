# tools/__init__.py  文件作用：让tools成为Python包
"""
工具类模块 —— 统一管理所有工具函数
"""
from .weather import get_weather
from .attraction import get_attraction

# 工具注册中心
available_tools = {
  "get_weather": get_weather,
  "get_attraction": get_attraction
}

# 导出给外部使用
__all__ = ['get_weather', 'get_attraction', 'available_tools']