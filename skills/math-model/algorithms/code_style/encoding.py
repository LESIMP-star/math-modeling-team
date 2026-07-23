"""
Unicode编码处理模块
功能：处理Unicode特殊字符，确保Windows GBK兼容
"""

import re
from typing import Dict, List, Tuple


# Unicode字符替换映射表
UNICODE_REPLACEMENTS = {
    "²": "**2",
    "³": "**3",
    "→": "->",
    "←": "<-",
    "↑": "^",
    "↓": "v",
    "≥": ">=",
    "≤": "<=",
    "≠": "!=",
    "≈": "~=",
    "±": "+/-",
    "×": "*",
    "÷": "/",
    "∞": "inf",
    "√": "sqrt",
    "∑": "sum",
    "∏": "prod",
    "∫": "int",
    "∂": "del",
    "∇": "grad",
    "∈": "in",
    "∉": "not in",
    "⊂": "subset",
    "⊃": "superset",
    "∪": "union",
    "∩": "intersect",
    "∧": "and",
    "∨": "or",
    "¬": "not",
    "∀": "for all",
    "∃": "exists",
    "∅": "empty",
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "δ": "delta",
    "ε": "epsilon",
    "ζ": "zeta",
    "η": "eta",
    "θ": "theta",
    "ι": "iota",
    "κ": "kappa",
    "λ": "lambda",
    "μ": "mu",
    "ν": "nu",
    "ξ": "xi",
    "π": "pi",
    "ρ": "rho",
    "σ": "sigma",
    "τ": "tau",
    "υ": "upsilon",
    "φ": "phi",
    "χ": "chi",
    "ψ": "psi",
    "ω": "omega",
    "Γ": "Gamma",
    "Δ": "Delta",
    "Θ": "Theta",
    "Λ": "Lambda",
    "Ξ": "Xi",
    "Π": "Pi",
    "Σ": "Sigma",
    "Φ": "Phi",
    "Ψ": "Psi",
    "Ω": "Omega",
}


def replace_unicode_chars(text: str) -> str:
    """
    替换Unicode字符

    Args:
        text: 原始文本

    Returns:
        替换后的文本
    """
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)

    return text


def check_encoding(text: str) -> Dict:
    """
    检查编码兼容性

    Args:
        text: 文本内容

    Returns:
        检查结果
    """
    issues = []

    # 检查是否包含Unicode特殊字符
    unicode_chars = []
    for char in text:
        if char in UNICODE_REPLACEMENTS:
            unicode_chars.append(char)

    if unicode_chars:
        issues.append(f"包含Unicode特殊字符: {unicode_chars[:5]}")

    # 检查是否可以GBK编码
    try:
        text.encode('gbk')
    except UnicodeEncodeError as e:
        issues.append(f"GBK编码错误: {e}")

    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "unicode_chars": unicode_chars
    }


def fix_encoding(text: str) -> str:
    """
    修复编码问题

    Args:
        text: 原始文本

    Returns:
        修复后的文本
    """
    # 1. 替换Unicode字符
    text = replace_unicode_chars(text)

    # 2. 处理其他编码问题
    # 替换全角字符为半角
    fullwidth_to_halfwidth = {
        '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
        '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
        'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E',
        'Ｆ': 'F', 'Ｇ': 'G', 'Ｈ': 'H', 'Ｉ': 'I', 'Ｊ': 'J',
        'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O',
        'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R', 'Ｓ': 'S', 'Ｔ': 'T',
        'Ｕ': 'U', 'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X', 'Ｙ': 'Y',
        'Ｚ': 'Z',
        'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e',
        'ｆ': 'f', 'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j',
        'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o',
        'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't',
        'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y',
        'ｚ': 'z',
        '＋': '+', '－': '-', '＊': '*', '／': '/', '＝': '=',
        '（': '(', '）': ')', '［': '[', '］': ']', '｛': '{', '｝': '}',
        '，': ',', '．': '.', '；': ';', '：': ':', '？': '?', '！': '!',
        '＜': '<', '＞': '>', '＆': '&', '｜': '|', '～': '~', '＾': '^',
    }

    for old, new in fullwidth_to_halfwidth.items():
        text = text.replace(old, new)

    return text


def validate_encoding(text: str) -> Tuple[bool, List[str]]:
    """
    验证编码兼容性

    Args:
        text: 文本内容

    Returns:
        (是否兼容, 问题列表)
    """
    # 检查是否包含Unicode字符
    check_result = check_encoding(text)

    if check_result["has_issues"]:
        return False, check_result["issues"]

    # 尝试GBK编码
    try:
        text.encode('gbk')
        return True, []
    except UnicodeEncodeError as e:
        return False, [f"GBK编码错误: {e}"]


def fix_file_encoding(input_file: str, output_file: str) -> bool:
    """
    修复文件编码

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径

    Returns:
        是否成功
    """
    try:
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 修复编码
        fixed_content = fix_encoding(content)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        return True
    except Exception as e:
        print(f"Error fixing file encoding: {e}")
        return False


def get_safe_filename(filename: str) -> str:
    """
    获取安全的文件名

    Args:
        filename: 原始文件名

    Returns:
        安全的文件名
    """
    # 替换Unicode字符
    safe_name = replace_unicode_chars(filename)

    # 替换其他不安全字符
    unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')

    return safe_name
