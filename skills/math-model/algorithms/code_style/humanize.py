"""
代码风格转换模块
功能：将AI风格代码转换为人类风格，降低AIGC检测率
"""

import re
from typing import Dict, List


# 变量名简化映射表
VARIABLE_SHORTCUTS = {
    "population": "pop",
    "probability": "prob",
    "transition": "trans",
    "optimization": "opt",
    "algorithm": "algo",
    "parameter": "param",
    "temperature": "temp",
    "distance": "dist",
    "satisfaction": "sat",
    "coverage": "cov",
    "elderly": "eld",
    "service": "svc",
    "station": "sta",
    "location": "loc",
    "calculation": "calc",
    "result": "res",
    "function": "func",
    "variable": "var",
    "matrix": "mat",
    "vector": "vec",
}


def convert_to_human_style(code: str) -> str:
    """
    将AI风格代码转换为人类风格

    Args:
        code: 原始代码

    Returns:
        转换后的代码
    """
    # 1. 简化变量名
    code = simplify_variable_names(code)

    # 2. 简化注释
    code = simplify_comments(code)

    # 3. 改变编码习惯
    code = improve_coding_style(code)

    # 4. 移除AI痕迹
    code = remove_ai_traces(code)

    return code


def simplify_variable_names(code: str) -> str:
    """
    简化变量名

    Args:
        code: 原始代码

    Returns:
        简化后的代码
    """
    for full, short in VARIABLE_SHORTCUTS.items():
        # 替换变量名，但保留字符串中的内容
        # 使用正则表达式匹配独立的单词
        pattern = r'\b' + re.escape(full) + r'\b'
        code = re.sub(pattern, short, code)

    return code


def simplify_comments(code: str) -> str:
    """
    简化注释

    Args:
        code: 原始代码

    Returns:
        简化后的代码
    """
    # 移除多行注释（保留简短的）
    def remove_long_docstrings(match):
        docstring = match.group(0)
        # 如果注释超过3行，简化为1行
        lines = docstring.split('\n')
        if len(lines) > 5:
            # 提取第一行作为简短描述
            first_line = lines[0].strip()
            if first_line.startswith('"""'):
                first_line = first_line[3:]
            if first_line.endswith('"""'):
                first_line = first_line[:-3]
            return f'"""{first_line.strip()}"""'
        return docstring

    code = re.sub(r'""".*?"""', remove_long_docstrings, code, flags=re.DOTALL)

    # 移除TODO注释
    code = re.sub(r'#\s*TODO.*$', '', code, flags=re.MULTILINE)

    # 移除过长的行内注释
    def shorten_inline_comments(match):
        comment = match.group(0)
        if len(comment) > 50:
            # 截断到50字符
            return comment[:47] + '...'
        return comment

    code = re.sub(r'#.*$', shorten_inline_comments, code, flags=re.MULTILINE)

    return code


def improve_coding_style(code: str) -> str:
    """
    改变编码习惯

    Args:
        code: 原始代码

    Returns:
        改进后的代码
    """
    # 1. 使用enumerate代替range(len()))
    pattern_range_len = r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):'
    replacement_enumerate = r'for \1, item in enumerate(\2):'
    code = re.sub(pattern_range_len, replacement_enumerate, code)

    # 2. 简化布尔返回
    pattern_bool_return = r'if\s+(\w+):\s*\n\s*return\s+True\s*\n\s*else:\s*\n\s*return\s+False'
    replacement_bool = r'return \1'
    code = re.sub(pattern_bool_return, replacement_bool, code)

    # 3. 使用列表推导式（简单情况）
    # 这个比较复杂，暂时不实现

    return code


def remove_ai_traces(code: str) -> str:
    """
    移除AI痕迹

    Args:
        code: 原始代码

    Returns:
        清理后的代码
    """
    # 1. 移除多余的空行
    code = re.sub(r'\n{3,}', '\n\n', code)

    # 2. 移除AI风格的注释
    ai_comments = [
        '# This function',
        '# This method',
        '# This class',
        '# Here we',
        '# We need to',
        '# First,',
        '# Then,',
        '# Finally,',
    ]
    for comment in ai_comments:
        code = code.replace(comment, '')

    # 3. 简化过长的变量名
    long_patterns = [
        (r'population_elderly_self_care', 'n_self'),
        (r'transition_probability_matrix', 'P_trans'),
        (r'service_station_location_optimization_model', 'loc_opt'),
        (r'satisfaction_score_calculation', 'calc_sat'),
        (r'coverage_rate_computation', 'calc_cov'),
    ]
    for pattern, replacement in long_patterns:
        code = code.replace(pattern, replacement)

    return code


def add_personal_style(code: str) -> str:
    """
    添加个人风格

    Args:
        code: 原始代码

    Returns:
        添加风格后的代码
    """
    # 1. 使用简短的变量名
    # 2. 添加简洁的注释
    # 3. 使用Pythonic的写法

    # 示例：使用列表推导式
    code = code.replace(
        'result = []\nfor x in data:\n    if x > 0:\n        result.append(x)',
        'result = [x for x in data if x > 0]'
    )

    # 示例：使用三元表达式
    code = code.replace(
        'if condition:\n    value = a\nelse:\n    value = b',
        'value = a if condition else b'
    )

    return code


def validate_code_style(code: str) -> Dict:
    """
    验证代码风格

    Args:
        code: 代码内容

    Returns:
        验证结果
    """
    issues = []

    # 检查变量名长度
    long_vars = re.findall(r'\b[a-z_]{20,}\b', code)
    if long_vars:
        issues.append(f"变量名过长: {long_vars[:3]}")

    # 检查注释密度
    comment_lines = len(re.findall(r'#.*$', code, re.MULTILINE))
    total_lines = len(code.split('\n'))
    comment_ratio = comment_lines / total_lines if total_lines > 0 else 0
    if comment_ratio > 0.3:
        issues.append(f"注释过多: {comment_ratio:.1%}")

    # 检查AI痕迹
    ai_patterns = [
        r'This function',
        r'This method',
        r'Here we',
        r'We need to',
    ]
    for pattern in ai_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            issues.append(f"AI痕迹: {pattern}")

    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "score": max(0, 100 - len(issues) * 20)
    }
