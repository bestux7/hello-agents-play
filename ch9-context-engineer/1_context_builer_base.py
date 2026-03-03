""" 快速使用ContextBuilder """
from dotenv import load_dotenv
load_dotenv()

from hello_agents.context import ContextBuilder, ContextConfig
from hello_agents.tools import MemoryTool, RAGTool
from hello_agents.core.message import Message
from datetime import datetime

"""  
    提示工程关注如何最好的编写LLM系统指令提示词来获得更优结果
    上下文工程不仅关注提示本身，还关注如何在推理阶段，维护最优的信息集合(进入上下文窗口的一切信息)
    上下文是给LLM模型调用时看的，决定了模型回答问题的质量
    ContextBuilder的核心是GSSC流水线 gather->select->structure->compress 收集相关上下文为候选包、选择相关性高的包、结构化上下文文本、压缩token空间
    最终构建出我们要的上下文
"""

# 初始化工具
memory_tool = MemoryTool(user_id="user123")
rag_tool = RAGTool(knowledge_base_path="./knowledge_base")

# 创建ContextConfig
config = ContextConfig(
    max_tokens=3000,
    reserve_ratio=0.2,
    min_relevance=0,
    enable_compression=True
)
# 创建ContextBuilder
builder = ContextBuilder(
    config=config,
    memory_tool=memory_tool,
    rag_tool=rag_tool,
)

# 准备对话历史
conversation_history = [
    Message(content="我正在开发一个数据分析工具", role="user", timestamp=datetime.now()),
    Message(content="很好!数据分析工具通常需要处理大量数据。您计划使用什么技术栈?", role="assistant", timestamp=datetime.now()),
    Message(content="我打算使用Python和Pandas,已经完成了CSV读取模块", role="user", timestamp=datetime.now()),
    Message(content="不错的选择!Pandas在数据处理方面非常强大。接下来您可能需要考虑数据清洗和转换。", role="assistant", timestamp=datetime.now()),
]

# 添加记忆
memory_tool.execute(
    "add",
    content="用户正在开发数据分析工具,使用Python和Pandas",
    memory_type="semantic",
    importance=0.8
)
memory_tool.execute(
    "add",
    content="已完成CSV读取模块的开发",
    memory_type="episodic",
    importance=0.7
)

# 构建上下文
context = builder.build(
    user_query="如何优化Pandas的内存占用?",
    conversation_history=conversation_history,
    system_instructions="你是一位资深的Python数据工程顾问。你的回答需要:1) 提供具体可行的建议 2) 解释技术原理 3) 给出代码示例"
)

print("=" * 80)
print("构建的上下文:")
print("=" * 80)
print(context)
print("=" * 80)
