"""
论文格式验证模块
功能：标题编号、格式验证、支撑材料检查
"""

from .formatting import format_section_title, validate_section_numbering
from .validation import validate_paper_format, check_references
from .materials import validate_support_materials, create_materials_structure
from .appendix import verify_code_insertion

__all__ = [
    'format_section_title',
    'validate_section_numbering',
    'validate_paper_format',
    'check_references',
    'validate_support_materials',
    'create_materials_structure',
    'verify_code_insertion'
]
