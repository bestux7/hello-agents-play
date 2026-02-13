# llm/__init__.py
"""
大模型调用模块
"""
from .llm_client import HelloAgentsLLM

# 提供给外部使用
__all__ = ['HelloAgentsLLM']