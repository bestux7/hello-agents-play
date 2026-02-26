""" 测试ToolChain工具链 """

from hello_agents.tools.chain import ToolChain

def create_research_chain() -> ToolChain:
    """ 创建一个研究工具链：搜索->计算->总结 """

    chain = ToolChain(
        name="research_and_calculate",
        description="搜索信息并进行计算"
    )

    # 1. 搜索信息
    chain.add_step(
        tool_name="search",
        input_template="{input}",
        output_key="search_result"
    )

    # 2. 根据搜索结果进行计算(如果需要的话)
    chain.add_step(
        tool_name="calculator",
        input_template="根据以下信息计算相关数值：{search_result}",
        output_key="calculation_result"
    )

    return chain