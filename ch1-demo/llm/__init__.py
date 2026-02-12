# llm/__init__.py
"""
大模型调用模块
"""
from .client import OpenAICompatibleClient

# 提供给外部使用
__all__ = ['OpenAICompatibleClient']
