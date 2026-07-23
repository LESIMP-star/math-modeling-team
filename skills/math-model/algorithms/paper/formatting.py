"""
论文格式化模块
功能：标题编号、格式验证
"""

import re
from typing import Dict, List, Tuple


def format_section_title(level: int, number: int, title: str) -> str:
    """
    格式化标题编号

    Args:
        level: 标题级别（1=一级, 2=二级, 3=三级）
        number: 编号
        title: 标题内容

    Returns:
        格式化后的标题
    """
    # 中文数字映射
    chinese_numbers = '一二三四五六七八九十'

    if level == 1:
        # 一级标题：中文数字 + 顿号
        if 1 <= number <= 10:
            return f"{chinese_numbers[number-1]}、{title}"
        else:
            return f"{number}、{title}"
    elif level == 2:
        # 二级标题：阿拉伯数字 + 小数点
        return f"{number}.{title}"
    elif level == 3:
        # 三级标题：阿拉伯数字 + 小数点
        return f"{number}.{title}"
    else:
        return title


def validate_section_numbering(text: str) -> Dict:
    """
    验证标题编号规范性

    Args:
        text: 论文内容

    Returns:
        验证结果
    """
    issues = []

    # 检查一级标题格式
    level1_pattern = r'^[一二三四五六七八九十]、.+$'
    level1_matches = re.findall(level1_pattern, text, re.MULTILINE)

    # 检查二级标题格式
    level2_pattern = r'^\d+\..+$'
    level2_matches = re.findall(level2_pattern, text, re.MULTILINE)

    # 检查混用问题
    mixed_pattern = r'^[一二三四五六七八九十]\.\d+.+$'
    mixed_matches = re.findall(mixed_pattern, text, re.MULTILINE)

    if mixed_matches:
        issues.append(f"发现混用格式: {mixed_matches[:3]}")

    # 检查编号连续性
    level1_numbers = []
    for match in level1_matches:
        # 提取中文数字
        for i, char in enumerate('一二三四五六七八九十'):
            if match.startswith(char):
                level1_numbers.append(i + 1)
                break

    # 检查是否连续
    if level1_numbers:
        expected = list(range(level1_numbers[0], level1_numbers[0] + len(level1_numbers)))
        if level1_numbers != expected:
            issues.append(f"一级标题编号不连续: {level1_numbers}")

    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "level1_count": len(level1_matches),
        "level2_count": len(level2_matches),
        "mixed_count": len(mixed_matches)
    }


def extract_section_structure(text: str) -> Dict:
    """
    提取论文章节结构

    Args:
        text: 论文内容

    Returns:
        章节结构字典
    """
    sections = {
        "level1": [],
        "level2": [],
        "level3": []
    }

    # 提取一级标题
    level1_pattern = r'^([一二三四五六七八九十]、.+)$'
    for match in re.finditer(level1_pattern, text, re.MULTILINE):
        sections["level1"].append(match.group(1))

    # 提取二级标题
    level2_pattern = r'^(\d+\..+)$'
    for match in re.finditer(level2_pattern, text, re.MULTILINE):
        sections["level2"].append(match.group(1))

    # 提取三级标题
    level3_pattern = r'^(\d+\.\d+\..+)$'
    for match in re.finditer(level3_pattern, text, re.MULTILINE):
        sections["level3"].append(match.group(1))

    return sections


def check_section_completeness(text: str, required_sections: List[str]) -> Dict:
    """
    检查章节完整性

    Args:
        text: 论文内容
        required_sections: 必需的章节列表

    Returns:
        检查结果
    """
    missing_sections = []

    for section in required_sections:
        if section not in text:
            missing_sections.append(section)

    return {
        "is_complete": len(missing_sections) == 0,
        "missing_sections": missing_sections,
        "total_required": len(required_sections),
        "found": len(required_sections) - len(missing_sections)
    }


def validate_chinese_numbering(text: str) -> Dict:
    """
    验证中文数字编号

    Args:
        text: 论文内容

    Returns:
        验证结果
    """
    issues = []

    # 检查中文数字格式
    chinese_pattern = r'^[一二三四五六七八九十]、'
    matches = re.findall(chinese_pattern, text, re.MULTILINE)

    # 检查是否按顺序
    expected_order = '一二三四五六七八九十'
    actual_order = ''.join([m[0] for m in matches])

    if actual_order and not expected_order.startswith(actual_order):
        issues.append(f"中文数字顺序错误: {actual_order}")

    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "count": len(matches)
    }


def format_table_caption(caption: str, number: int) -> str:
    """
    格式化表格标题

    Args:
        caption: 标题内容
        number: 表格编号

    Returns:
        格式化后的标题
    """
    return f"表 {number} {caption}"


def format_figure_caption(caption: str, number: int) -> str:
    """
    格式化图片标题

    Args:
        caption: 标题内容
        number: 图片编号

    Returns:
        格式化后的标题
    """
    return f"图 {number} {caption}"


def validate_caption_format(text: str) -> Dict:
    """
    验证标题格式

    Args:
        text: 论文内容

    Returns:
        验证结果
    """
    issues = []

    # 检查表格标题格式
    table_pattern = r'表\s*\d+\s+.+'
    table_matches = re.findall(table_pattern, text)

    # 检查图片标题格式
    figure_pattern = r'图\s*\d+\s+.+'
    figure_matches = re.findall(figure_pattern, text)

    # 检查编号是否连续
    table_numbers = [int(re.search(r'\d+', m).group()) for m in table_matches]
    figure_numbers = [int(re.search(r'\d+', m).group()) for m in figure_matches]

    if table_numbers:
        expected = list(range(1, len(table_numbers) + 1))
        if table_numbers != expected:
            issues.append(f"表格编号不连续: {table_numbers}")

    if figure_numbers:
        expected = list(range(1, len(figure_numbers) + 1))
        if figure_numbers != expected:
            issues.append(f"图片编号不连续: {figure_numbers}")

    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "table_count": len(table_matches),
        "figure_count": len(figure_matches)
    }
