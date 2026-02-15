"""
提示词模块
"""
from .react_prompts import REACT_PROMPT_TEMPLATE
from .executor_prompts import EXECUTOR_PROMPT_TEMPLATE
from .planner_prompts import PLANNER_PROMPT_TEMPLATE

__all__ = ['REACT_PROMPT_TEMPLATE', 'EXECUTOR_PROMPT_TEMPLATE', 'PLANNER_PROMPT_TEMPLATE']