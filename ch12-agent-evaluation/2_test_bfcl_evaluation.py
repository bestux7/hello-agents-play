""" 评估智能体在BFCL数据集上的效果 """
from dotenv import load_dotenv
load_dotenv()

from hello_agents import HelloAgentsLLM, SimpleAgent
from hello_agents.tools import BFCLEvaluationTool

llm = HelloAgentsLLM()
agent = SimpleAgent(
    name="TestAgent",
    llm=llm
)
# 创建BFCLEvaluationTool工具，自动完成agent执行、result.json文件生成，格式转换、调用官方评估接口、生成最终报告所有步骤
bfcl_tool = BFCLEvaluationTool()
results = bfcl_tool.run(
    agent=agent,
    category="simple_python",
    max_samples=20,
    model_name="Qwen/Qwen3-8B"
)

print(f"准确率: {results['overall_accuracy']:.2%}")
print(f"正确数: {results['correct_samples']}/{results['total_samples']}")