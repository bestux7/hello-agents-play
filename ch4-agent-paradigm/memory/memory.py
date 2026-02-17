from typing import Any, Dict, List, Optional


class Memory:
  """ 记忆模块,用于存储智能体的行动与反思轨迹 """
  def __init__(self) -> None:
    """ 初始化一个空的记忆列表records来存储所有记录 {{"record_type":"execution", "content":"执行内容"}, {"reflection":"反思内容", ...}} """
    self.records: List[Dict[str, Any]] = []

  def add_record(self, record_type: str, content: Any):
    """
      向记忆中添加一条新记录。

      参数:
      - record_type (str): 记录的类型 ('execution' 或 'reflection')。
      - content (str): 记录的具体内容 (例如，生成的代码或反思的反馈)。
      """
    record = {"record_type": record_type, "content": content}
    self.records.append(record)
    print(f"添加了一条新的{record_type}记录")

  def get_trajectory(self) -> str:
    """ 将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。 """
    trajectory_parts = []
    for record in self.resords:
      if record["record_type"] == "execution":
        trajectory_parts.append(f"--- 上一轮尝试 (代码) ---\n{record['content']}")
      elif record["record_type"] == "reflection":
        trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
    return "\n\n".join(trajectory_parts)

  def get_last_execution(self) -> Optional[str]:
    """ 获取最后一次执行结果，例如最新生成的代码。如果不存在，返回None。 """
    for record in reversed(self.records):
      if record["record_type"] == "execution":
        return record["content"]
    return None
      
