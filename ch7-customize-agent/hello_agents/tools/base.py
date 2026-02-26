""" 工具基类 """

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel

class Tool(ABC):
    """ 工具基类 """
    def __init__(self, name:str, description:str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        """ 执行工具 """
        pass

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """ 获取工具参数定义 """
        pass

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """ 验证参数 """
        required_params = [p.name for p in self.get_parameters() if p.required]
        return all(param in parameters for param in required_params)

    def to_dict(self) -> Dict[str, Any]:
        """ 转换为字典格式 """

        """ 
        把对象字段：
        param = ToolParameter(
            name="city",
            type="string",
            description="城市名称",
            required=True,
            default=None,
        )
        转成键值对形式的字典：
        {
            "name": "city",
            "type": "string",
            "description": "城市名称",
            "required": True,
            "default": None,
        }
        """


        return {
            "name": self.name,
            "description": self.description,
            "parameters": [param.dict() for param in self.get_parameters()]
        }

    def to_openai_schema(self) -> Dict[str, Any]:
        """转换为 OpenAI function calling schema 格式

        用于 FunctionCallAgent，使工具能够被 OpenAI 原生 function calling 使用

        Returns:
            符合 OpenAI function calling 标准的 schema
        """

        parameters = self.get_parameters()
        # 构建properties
        properties = {}
        required = []

        for param in parameters:
            # 基础属性定义
            prop = {
                "type": param.type,
                "description": param.description
            }

            # 如果有默认值，添加到描述中（OpenAI schema不支持default字段）
            if param.default is not None:
                prop["description"] = f"{param.description} 默认值为 {param.default}"

            # 如果是数组属性，添加items定义
            if param.type == "array":
                prop["items"] = {"type": "string"} # 默认字符串数组

            properties[param.name] = prop

            # 如果是必要参数，收集
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }



    def __str__(self) -> str:
        return f"Tool(name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()


class ToolParameter(BaseModel):
    """ 工具参数定义 """
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None




