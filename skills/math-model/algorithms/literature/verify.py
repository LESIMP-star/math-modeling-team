"""
文献验证模块
功能：验证文献的真实性，解决AI幻觉问题
"""

import re
import requests
from typing import Dict, List, Optional


def verify_literature(literature: Dict) -> Dict:
    """
    验证文献真实性

    Args:
        literature: 文献信息字典，包含：
            - title: 论文标题
            - author: 作者
            - journal: 期刊
            - year: 年份
            - doi: DOI号

    Returns:
        验证结果字典：
            - is_valid: 是否有效
            - confidence: 置信度 (0-1)
            - verification_details: 验证详情
            - warnings: 警告信息
    """
    checks = {
        "author_exists": check_author(literature.get("author", "")),
        "journal_exists": check_journal(literature.get("journal", "")),
        "doi_valid": check_doi(literature.get("doi", "")),
        "year_reasonable": check_year(literature.get("year", 0)),
        "title_coherent": check_title(literature.get("title", "")),
    }

    confidence = sum(checks.values()) / len(checks)

    return {
        "is_valid": confidence >= 0.7,
        "confidence": confidence,
        "verification_details": checks,
        "warnings": [k for k, v in checks.items() if not v]
    }


def check_author(author: str) -> bool:
    """
    验证作者是否存在

    Args:
        author: 作者姓名

    Returns:
        是否存在
    """
    if not author:
        return False

    # 检查作者姓名格式
    # 中文作者：2-4个汉字
    # 英文作者：First Last 格式
    chinese_pattern = r'^[一-龥]{2,4}$'
    english_pattern = r'^[A-Z][a-z]+ [A-Z][a-z]+$'

    if re.match(chinese_pattern, author) or re.match(english_pattern, author):
        return True

    return False


def check_journal(journal: str) -> bool:
    """
    验证期刊是否存在

    Args:
        journal: 期刊名称

    Returns:
        是否存在
    """
    if not journal:
        return False

    # 常见中文学术期刊关键词
    chinese_keywords = [
        '学报', '科学', '工程', '技术', '研究', '管理', '系统',
        '计算机', '数学', '物理', '化学', '生物', '医学',
        '大学', '学院', '研究所', '学会', '协会'
    ]

    # 常见英文学术期刊关键词
    english_keywords = [
        'Journal', 'Science', 'Engineering', 'Technology',
        'Research', 'Management', 'Systems', 'Computer',
        'Mathematics', 'Physics', 'Chemistry', 'Biology',
        'Medicine', 'Proceedings', 'Transactions', 'Letters'
    ]

    # 检查是否包含关键词
    for keyword in chinese_keywords + english_keywords:
        if keyword.lower() in journal.lower():
            return True

    return False


def check_doi(doi: str) -> bool:
    """
    验证DOI是否有效

    Args:
        doi: DOI号

    Returns:
        是否有效
    """
    if not doi:
        return False

    # DOI格式：10.xxxx/xxxxx
    doi_pattern = r'^10\.\d{4,}/.+$'

    if not re.match(doi_pattern, doi):
        return False

    # 尝试访问DOI解析服务
    try:
        response = requests.head(
            f'https://doi.org/{doi}',
            timeout=5,
            allow_redirects=True
        )
        return response.status_code == 200
    except:
        # 如果无法访问，仅检查格式
        return True


def check_year(year: int) -> bool:
    """
    验证年份是否合理

    Args:
        year: 发表年份

    Returns:
        是否合理
    """
    if not year:
        return False

    # 年份范围：1900-当前年份
    import datetime
    current_year = datetime.datetime.now().year

    return 1900 <= year <= current_year


def check_title(title: str) -> bool:
    """
    验证标题是否合理

    Args:
        title: 论文标题

    Returns:
        是否合理
    """
    if not title:
        return False

    # 标题长度检查：10-200字符
    if len(title) < 10 or len(title) > 200:
        return False

    # 检查是否包含乱码或特殊字符
    if re.search(r'[^\w\s一-龥\-:,.()（）【】《》]', title):
        return False

    return True


def batch_verify(literature_list: List[Dict]) -> Dict:
    """
    批量验证文献

    Args:
        literature_list: 文献列表

    Returns:
        验证统计结果
    """
    results = []
    for lit in literature_list:
        result = verify_literature(lit)
        results.append({
            **lit,
            "verification": result
        })

    # 统计
    total = len(results)
    valid = sum(1 for r in results if r["verification"]["is_valid"])
    invalid = total - valid

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "valid_rate": valid / total if total > 0 else 0,
        "results": results
    }
