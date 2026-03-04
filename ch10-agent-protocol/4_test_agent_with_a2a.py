""" 智能体 使用A2A协议 """
from dotenv import load_dotenv
from hello_agents.tools.builtin.protocol_tools import A2ATool
load_dotenv()

import re
import threading
import time

from hello_agents import HelloAgentsLLM, SimpleAgent
from hello_agents.protocols.a2a.implementation import A2AServer, A2AClient, A2A_AVAILABLE

llm = HelloAgentsLLM()

# 1.创建技术专家agent服务 使用a2a协议
tech_expert = A2AServer(
    name="tech_expert",
    description="技术专家，回答技术问题"
)
@tech_expert.skill(skill_name="answer")
def answer_tech_question(text: str) -> str:

    match = re.search(r'answer\s+(.+)', text, re.IGNORECASE)
    question = match.group(1).strip() if match else text
    # 实际应用中，这里会调用LLM或知识库
    return f"技术回答：关于'{question}'，我建议您查看我们的技术文档..."

# 2.创建销售顾问agent服务
sales_advisor = A2AServer(
    name="sales_advisor",
    description="销售顾问，回答销售问题"
)
@sales_advisor.skill(skill_name="answer")
def answer_sales_question(text: str) -> str:
    match = re.search(r'answer\s+(.+)', text, re.IGNORECASE)
    question = match.group(1).strip() if match else text
    return f"销售回答：关于'{question}'，我们有特别优惠..."

# 3.启动服务
threading.Thread(target=lambda: tech_expert.run(port=6000), daemon=True).start()
threading.Thread(target=lambda: sales_advisor.run(port=6001), daemon=True).start()
time.sleep(2)   # 休眠两秒，等待启动

# 4. 创建接待员Agent（使用HelloAgents的SimpleAgent）
receptionist = SimpleAgent(
    name="接待员",
    llm=llm,
    system_prompt="""你是客服接待员，负责：
1. 分析客户问题类型（技术问题 or 销售问题）
2. 将问题转发给相应的专家
3. 整理专家的回答并返回给客户

请保持礼貌和专业。"""
)
# 添加技术专家工具
tech_tool = A2ATool(agent_url="http://localhost:6000", name="tech_expert", description="技术专家，回答技术问题")
receptionist.add_tool(tech_tool)

sales_tool = A2ATool(agent_url="http://localhost:6001", name="sales_advisor", description="销售顾问，回答价格、购买相关问题")
receptionist.add_tool(sales_tool)

# 5. 处理客户咨询
def handle_customer_query(query):
    if not A2A_AVAILABLE:
        print("❌ A2A SDK 未安装，请运行: pip install a2a-sdk")
        return None
    print(f"\n客户咨询：{query}")
    print("=" * 50)
    response = receptionist.run(query)
    print(f"\n客服回复：{response}")
    print("=" * 50)

# 测试不同类型的问题
if __name__ == "__main__":
    handle_customer_query("你们的API如何调用？")
    handle_customer_query("企业版的价格是多少？")
    handle_customer_query("如何集成到我的Python项目中？")