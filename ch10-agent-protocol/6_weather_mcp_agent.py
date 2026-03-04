""" 集成自定义天气查询mcp到智能体 """

from dotenv import load_dotenv
load_dotenv()

from hello_agents import HelloAgentsLLM, SimpleAgent
from hello_agents.protocols.mcp import MCPClient
from hello_agents.tools import MCPTool

def create_weather_assistant():
    """创建天气助手"""
    llm = HelloAgentsLLM()

    assistant = SimpleAgent(
        name="天气助手",
        llm=llm,
        system_prompt="""你是天气助手，可以查询城市天气。
        - 使用 get_weather 工具查询天气，支持中文城市名。
        - 使用 list_supported_cities 列出所有支持的中文城市
        - 使用 get_server_info 获取服务器信息
"""
    )

    # 添加天气mcp工具
    server_script = "./6_weather_mcp_server.py"
    weather_tool = MCPTool(server_command=["python", server_script])
    assistant.add_tool(weather_tool)
    
    return assistant


def interactive():
    """交互模式"""
    assistant = create_weather_assistant()

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        response = assistant.run(user_input)
        print(f"助手: {response}")


if __name__ == "__main__":
    interactive()