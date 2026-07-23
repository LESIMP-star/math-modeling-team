"""
代码风格优化模块
功能：降低AIGC检测率，优化代码风格
"""

from .humanize import convert_to_human_style
from .simplify import simplify_variable_name, simplify_comments
from .encoding import replace_unicode_chars, check_encoding

__all__ = [
    'convert_to_human_style',
    'simplify_variable_name',
    'simplify_comments',
    'replace_unicode_chars',
    'check_encoding'
]
