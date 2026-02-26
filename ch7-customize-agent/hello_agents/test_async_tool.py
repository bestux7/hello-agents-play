""" 测试异步工具执行 """
import asyncio
from hello_agents import AsyncToolExecutor, ToolRegistry
from my_advanced_search import MyAdvancedSearchTool
from calculator import calculate
from dotenv import load_dotenv

load_dotenv()

async def test_parallel_execution():
    """ 测试异步并行工具执行 """

    registry = ToolRegistry()
    # 注册搜索和计算工具
    search_tool = MyAdvancedSearchTool()
    registry.register_function(
        name="search", 
        description="高级搜索工具，整合Tavily和SerpAPI多个搜索源，提供更全面的搜索结果", 
        func=search_tool.search)

    registry.register_function(
        name="calculator",
        description="简单的数学计算工具，支持基本运算(+,-,*,/)和sqrt函数",
        func=calculate
    )
    
    # 创建异步工具执行器
    executor = AsyncToolExecutor(registry)

    # 定义并行任务
    tasks = [
        {"tool_name": "search", "input_data": "如何使用hello-agents?"},
        {"tool_name": "search", "input_data": "最好的agent框架是什么?"},
        {"tool_name": "calculator", "input_data": "1 + 1"},
        {"tool_name": "calculator", "input_data": "sqrt(100)"}
    ]

    # 并行执行
    results = await executor.execute_tools_parallel(tasks=tasks)

    # 打印结果
    for i, result in enumerate(results):
        print(f"Task {i+1}: {result}")

if __name__ == "__main__":
    asyncio.run(test_parallel_execution())
