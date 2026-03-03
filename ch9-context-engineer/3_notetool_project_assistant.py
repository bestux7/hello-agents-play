"""长期项目助手,集成 NoteTool 和 ContextBuilder"""
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

from hello_agents import SimpleAgent
from hello_agents.core.llm import HelloAgentsLLM
from hello_agents.core.message import Message
from hello_agents.tools import MemoryTool, NoteTool, RAGTool
from hello_agents.context import ContextBuilder, ContextConfig, ContextPacket

class ProjectAssistant(SimpleAgent):
    """ 长期项目助手,集成 NoteTool 和 ContextBuilder 
        NoteTool 是为"长时程任务"提供的结构化外部记忆组件。它以 Markdown 文件作为载体，头部使用 YAML 前置元数据记录关键信息，正文用于记录状态、结论、阻塞与行动项等内容。
        主要功能：使用NoteTool来记录项目运行状态、结论、阻塞、行动， 并结合ContextBuilde，作为ContextPacket包，有效的生成项目运行上下文
    """
    def __init__(self, name: str, project_name: str, **kwargs):
        super().__init__(name=name, llm=HelloAgentsLLM(), **kwargs)

        self.project_name = project_name
        # 初始化工具
        # self.memory_tool = MemoryTool(user_id=project_name)
        # self.rag_tool = RAGTool(knowledge_base_path=f"./{project_name}_kb")
        self.note_tool = NoteTool(workspace=f"./{project_name}_notes")
        
        # 初始化上下文构建器
        self.context_builder = ContextBuilder(
            # memory_tool=self.memory_tool,
            # rag_tool=self.rag_tool,
            config=ContextConfig(max_tokens=4000)
        )

        # 对话历史
        self.conversation_history = []

    def run(self, user_input: str, note_as_action: bool=False) -> str:
        """ 运行助手，自动集成笔记 """
        
        # 1.从NoteTool检索用户查询相关的笔记
        relevant_notes = self._retrieve_relevant_notes(user_input)

        # 2.将相关笔记转换成候选包格式
        note_packets = self._notes_to_packets(relevant_notes)

        # 3.构建上下文
        optimized_context = self.context_builder.build(
            user_query=user_input,
            conversation_history=self.conversation_history,
            system_instructions=self._build_system_instructions(),
            additional_packets=note_packets
        )

        # 4.调用LLM
        messages = [
            {"role": "system", "content": optimized_context},
            {"role": "user", "content": user_input}
        ]
        response = self.llm.invoke(messages)

        # 5.记录交互为笔记
        if note_as_action:
            self._save_as_note(user_input, response)

        # 6.更新对话历史
        self._update_history(user_input, response)

        return response

    def _retrieve_relevant_notes(self, query: str, limit: int=3) -> List[Dict]:
        """ 检索相关笔记 """
        
        try:
            # 1.优先从note tool中检索blocker和action类型的笔记
            blockers_raw = self.note_tool.run(
                {
                    "action": "list",
                    "note_type": "blocker",
                    "limit": 2
                }
            )

            # 2.通用搜索
            search_results_raw = self.note_tool.run(
                {
                    "action": "search",
                    "query": query,
                    "limit": limit
                }
            )

            blockers = self._ensure_list_of_dicts(blockers_raw)
            search_results = self._ensure_list_of_dicts(search_results_raw)            

            # 3.合并结果并去重 返回
            all_notes = {}
            for note in blockers + search_results:
                if not isinstance(note, dict):
                    continue
                note_id = (
                    note.get("note_id")
                    or note.get("id")
                    or note.get("uuid")
                    or note.get("title")
                    or str(hash(str(note)))
                )
                all_notes[note_id] = note
            return list(all_notes.values())[:limit]
        except Exception as e:
            print(f"[WARNING] 笔记检索失败: {e}")
            return []

    def _ensure_list_of_dicts(self, data) -> List[Dict]:
            """将 NoteTool 返回规范化为字典列表"""
            import json
            if data is None:
                return []
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception:
                    return []
            if isinstance(data, dict):
                # 兼容 {"items": [...]} 或单条记录
                if "items" in data and isinstance(data["items"], list):
                    return [item for item in data["items"] if isinstance(item, dict)]
                return [data]
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
            return []

    def _notes_to_packets(self, notes: List[Dict]) -> List[ContextPacket]:
        """ 将笔记转换为上下文包 """
        packets = []

        for note in notes:
            title = note.get("title", "")
            body = note.get("content", "")
            content = f"[笔记:{title}]\n{body}"

            note_type = note.get("type") or note.get("note_type") or "note"
            note_id = (
                note.get("note_id")
                or note.get("id")
                or note.get("uuid")
                or title
                or str(hash(str(note)))
            )

            packets.append(ContextPacket(
                    content=content,
                    timestamp=datetime.fromisoformat(note['updated_at']),
                    token_count=len(content)//4, # 简单估算
                    relevance_score=0.75,   # 笔记相关性较高
                    metadata={
                        "type": "note",
                        "note_type": note_type,
                        "note_id": note_id
                    }
                )
            )
        return packets
            
    def _save_as_note(self, user_input: str, response: str):
        """ 将交互存为笔记 """

        try:
            # 判断note_type类型
            if "问题" in user_input or "阻塞" in user_input:
                note_type = "blocker"
            elif "计划" in user_input or "下一步" in user_input:
                note_type = "action"
            else:
                note_type = "conclusion"

            self.note_tool.run({
                    "action": "create",
                    "title": f"{user_input[:30]}...",
                    "content": f"## 问题\n{user_input}\n\n## 分析\n{response}",
                    "note_type": note_type,
                    "tags": [self.project_name, "auto_generated"]
            })
        except Exception as e:
            print(f"[WARNING] 笔记保存失败: {e}")


    def _build_system_instructions(self) -> str:
        """构建系统指令"""
        return f"""你是 {self.project_name} 项目的长期助手。

        你的职责:
        1. 基于历史笔记提供连贯的建议
        2. 追踪项目进展和待解决问题
        3. 在回答时引用相关的历史笔记
        4. 提供具体、可操作的下一步建议

        注意:
        - 优先关注标记为 blocker 的问题
        - 在建议中说明依据来源(笔记、记忆或知识库)
        - 保持对项目整体进度的认识"""


    def _update_history(self, user_input: str, response: str):
        """ 更新对话历史 """
        
        self.conversation_history.append(
            Message(content=user_input, role="user", timestamp=datetime.now())
        )

        self.conversation_history.append(
            Message(content=response, role="assistant", timestamp=datetime.now())
        )

        # 限制历史长度为10
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

def main():
    # 使用
    assistant = ProjectAssistant(name="项目助手", project_name="data_pipeline_refactoring")
    # 第一次交互
    print("第一次交互:记录项目状态")
    response = assistant.run(
        user_input="我们已经完成了数据模型层的重构,测试覆盖率达到85%。下一步计划重构业务逻辑层。",
        note_as_action=True)
    print(f"第一次交互响应：{response}")
    
    # 第二次交互
    print("第二次交互:提出问题")
    response = assistant.run(
        user_input="在重构业务逻辑层时,我遇到了依赖版本冲突的问题,该如何解决?"
    )
    print(f"第二次交互响应：{response}")
    
    # 摘要
    summary = assistant.note_tool.run({"action": "summary"})
    print(f"摘要：{summary}")

if __name__ == "__main__":
    main()