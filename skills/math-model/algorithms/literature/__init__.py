"""
文献管理模块
功能：文献搜索、验证、引用生成
"""

from .search import search_literature
from .verify import verify_literature
from .citation import generate_citation

__all__ = ['search_literature', 'verify_literature', 'generate_citation']
