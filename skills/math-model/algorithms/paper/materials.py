"""
支撑材料验证模块
功能：验证支撑材料的完整性
"""

import os
from typing import Dict, List
from pathlib import Path


# 支撑材料清单
SUPPORT_MATERIALS_CHECKLIST = {
    "必选": [
        "所有可运行源程序（.py/.m文件）",
        "自主查阅的数据资料（非赛题原始数据）",
        "较大篇幅中间结果的图表",
        "文献资料（PDF或链接）",
    ],
    "可选": [
        "模型推导过程详细文档",
        "算法伪代码",
        "数据预处理说明",
    ],
    "打包要求": [
        "使用WinRAR压缩",
        "后缀为RAR或ZIP",
        "大小不超过20MB",
        "文件命名清晰",
    ]
}


def validate_support_materials(materials_dir: str) -> Dict:
    """
    验证支撑材料的完整性

    Args:
        materials_dir: 支撑材料目录路径

    Returns:
        验证结果
    """
    issues = []
    warnings = []

    # 检查目录是否存在
    if not os.path.exists(materials_dir):
        return {
            "is_valid": False,
            "issues": ["支撑材料目录不存在"],
            "warnings": [],
            "checklist": {}
        }

    # 检查代码文件
    code_files = []
    for ext in ['.py', '.m', '.R']:
        code_files.extend(Path(materials_dir).rglob(f'*{ext}'))

    if not code_files:
        issues.append("未找到代码文件（.py/.m/.R）")

    # 检查数据文件
    data_files = []
    for ext in ['.xlsx', '.csv', '.json', '.txt']:
        data_files.extend(Path(materials_dir).rglob(f'*{ext}'))

    if not data_files:
        warnings.append("未找到数据文件（.xlsx/.csv/.json/.txt）")

    # 检查图表文件
    figure_files = []
    for ext in ['.png', '.jpg', '.svg', '.pdf']:
        figure_files.extend(Path(materials_dir).rglob(f'*{ext}'))

    if not figure_files:
        warnings.append("未找到图表文件（.png/.jpg/.svg/.pdf）")

    # 检查文献文件
    literature_files = []
    for ext in ['.pdf', '.doc', '.docx']:
        literature_files.extend(Path(materials_dir).rglob(f'*{ext}'))

    if not literature_files:
        warnings.append("未找到文献文件（.pdf/.doc/.docx）")

    # 检查目录结构
    expected_dirs = ['代码', '数据', '图表', '文献']
    actual_dirs = [d.name for d in Path(materials_dir).iterdir() if d.is_dir()]

    missing_dirs = []
    for expected in expected_dirs:
        if not any(expected in actual for actual in actual_dirs):
            missing_dirs.append(expected)

    if missing_dirs:
        warnings.append(f"建议创建以下子目录: {missing_dirs}")

    # 检查打包要求
    archive_files = []
    for ext in ['.rar', '.zip']:
        archive_files.extend(Path(materials_dir).parent.glob(f'*{ext}'))

    if not archive_files:
        warnings.append("未找到压缩包文件（.rar/.zip）")

    # 检查文件大小
    total_size = sum(f.stat().st_size for f in Path(materials_dir).rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)

    if size_mb > 20:
        issues.append(f"支撑材料总大小超过20MB: {size_mb:.2f}MB")

    # 生成清单
    checklist = {
        "代码文件": len(code_files),
        "数据文件": len(data_files),
        "图表文件": len(figure_files),
        "文献文件": len(literature_files),
        "总大小": f"{size_mb:.2f}MB"
    }

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "checklist": checklist
    }


def create_materials_structure(output_dir: str, competition_id: str) -> str:
    """
    创建支撑材料目录结构

    Args:
        output_dir: 输出目录
        competition_id: 参赛编号

    Returns:
        创建的目录路径
    """
    # 创建主目录
    main_dir = os.path.join(output_dir, f"支撑材料_{competition_id}")
    os.makedirs(main_dir, exist_ok=True)

    # 创建子目录
    sub_dirs = ['代码', '数据', '图表', '文献']
    for sub_dir in sub_dirs:
        os.makedirs(os.path.join(main_dir, sub_dir), exist_ok=True)

    # 创建说明文件
    readme_path = os.path.join(main_dir, '说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"参赛编号：{competition_id}\n")
        f.write("=" * 50 + "\n\n")
        f.write("目录结构：\n")
        f.write("├── 代码/          # 求解代码（.py/.m文件）\n")
        f.write("├── 数据/          # 数据文件（.xlsx/.csv文件）\n")
        f.write("├── 图表/          # 输出图表（.png/.svg文件）\n")
        f.write("├── 文献/          # 参考文献（.pdf文件）\n")
        f.write("└── 说明.txt       # 本说明文件\n\n")
        f.write("注意事项：\n")
        f.write("1. 请确保所有代码可运行\n")
        f.write("2. 请确保数据文件完整\n")
        f.write("3. 请确保图表清晰可读\n")
        f.write("4. 请确保文献来源真实\n")
        f.write("5. 总大小不超过20MB\n")

    return main_dir


def generate_materials_report(materials_dir: str) -> str:
    """
    生成支撑材料报告

    Args:
        materials_dir: 支撑材料目录路径

    Returns:
        报告内容
    """
    # 验证材料
    result = validate_support_materials(materials_dir)

    # 生成报告
    report = []
    report.append("# 支撑材料验证报告")
    report.append("")

    # 基本信息
    report.append("## 基本信息")
    report.append(f"- 目录路径: {materials_dir}")
    report.append(f"- 验证状态: {'✅ 通过' if result['is_valid'] else '❌ 未通过'}")
    report.append("")

    # 文件统计
    report.append("## 文件统计")
    for key, value in result['checklist'].items():
        report.append(f"- {key}: {value}")
    report.append("")

    # 问题列表
    if result['issues']:
        report.append("## 问题列表")
        for issue in result['issues']:
            report.append(f"- ❌ {issue}")
        report.append("")

    # 警告列表
    if result['warnings']:
        report.append("## 警告信息")
        for warning in result['warnings']:
            report.append(f"- ⚠️ {warning}")
        report.append("")

    # 建议
    report.append("## 建议")
    report.append("1. 确保所有代码可运行")
    report.append("2. 确保数据文件完整")
    report.append("3. 确保图表清晰可读")
    report.append("4. 确保文献来源真实")
    report.append("5. 总大小不超过20MB")
    report.append("")

    return "\n".join(report)
