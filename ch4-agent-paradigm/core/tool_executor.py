from typing import Dict, Any
# search 工具

from dotenv import load_dotenv

load_dotenv()

class ToolExecutor:
  """
  一个工具执行器，负责统一注册、调度、管理、执行工具。
  """
  def __init__(self):
    """
    初始化工具箱tools:{toolName, {description, func}}
    """
    self.tools: Dict[str, Dict[str, Any]] = {}

  def registerTool(self, name:str, description:str, func:callable):
    """
    注册工具
    """
    if name in self.tools:
      print(f"警告：工具'{name}已存在，将被覆盖。'")
    self.tools[name] = {"description": description, "func": func}
    print(f"工具{name}已注册。")

  def getTool(self, name:str) -> callable:
    """
    根据工具名获取工具的执行函数
    """
    if name in self.tools:
      return self.tools.get(name,{}).get("func")

  def getAvailableTools(self) -> str:
    """
    获取工具箱中所有工具的格式化描述字符串
    """
    return "\n".join([
      f"- {name}: {info['description']}"
      for name, info in self.tools.items()
    ])
    
# # ----工具初始化与使用示例----
# if __name__ == '__main__':
#   # 1.初始化工具执行器
#   toolExecutor = ToolExecutor()
#   # 2.注册search工具
#   search_description = "一个网页搜索引擎，当你需要回答关于时事、事实以及在你的知识库在你的知识库中找不到的信息时，应使用此工具。"
#   toolExecutor.registerTool("Search", search_description, search)
#   # 3.打印可用工具
#   print("\n--- 可用的工具 ---")
#   print(toolExecutor.getAvailableTools())
#   # 4.智能体Action调用，获取工具，执行工具函数，问一个实时性问题
#   print("\n--- 执行Action：Search['最新的黄金每克价格是多少'] ---")
#   tool_name = "Search"
#   tool_input = "最新的黄金每克价格是多少"
#   tool_function = toolExecutor.getTool(tool_name)
#   if tool_function:
#     observation = tool_function(tool_input)
#     print("--- 观察(observation) ---")
#     print(observation)
#   else:
#     print(f"错误，未找到名为'{tool_name}'的工具。")
