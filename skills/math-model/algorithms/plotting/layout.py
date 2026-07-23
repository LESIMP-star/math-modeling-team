"""
图表布局调整模块
功能：自动调整图表布局，避免重叠
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, List, Optional


def check_overlap(ax: plt.Axes) -> bool:
    """
    检查图表是否存在重叠

    Args:
        ax: matplotlib Axes对象

    Returns:
        是否存在重叠
    """
    # 获取图例位置
    legend = ax.get_legend()
    if legend:
        legend_bbox = legend.get_window_extent()

        # 获取坐标轴标签
        xlabel = ax.xaxis.label
        ylabel = ax.yaxis.label

        # 检查是否重叠
        if xlabel and ylabel:
            xlabel_bbox = xlabel.get_window_extent()
            ylabel_bbox = ylabel.get_window_extent()

            # 简单重叠检测
            if (legend_bbox.xmax > xlabel_bbox.xmin and
                legend_bbox.ymax > xlabel_bbox.ymin):
                return True

    return False


def find_best_legend_position(ax: plt.Axes) -> str:
    """
    找到最佳的图例位置

    Args:
        ax: matplotlib Axes对象

    Returns:
        最佳位置字符串
    """
    # 获取数据范围
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # 计算数据密度
    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2

    # 获取所有数据点
    all_x = []
    all_y = []
    for line in ax.get_lines():
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())

    if not all_x or not all_y:
        return 'upper right'

    # 计算四个角落的数据密度
    corners = {
        'upper left': (xlim[0], ylim[1]),
        'upper right': (xlim[1], ylim[1]),
        'lower left': (xlim[0], ylim[0]),
        'lower right': (xlim[1], ylim[0]),
    }

    # 找到数据最稀疏的角落
    best_position = 'upper right'
    min_density = float('inf')

    for position, (cx, cy) in corners.items():
        # 计算该区域的数据点数量
        density = sum(1 for x, y in zip(all_x, all_y)
                     if abs(x - cx) < (xlim[1] - xlim[0]) * 0.3 and
                        abs(y - cy) < (ylim[1] - ylim[0]) * 0.3)

        if density < min_density:
            min_density = density
            best_position = position

    return best_position


def auto_adjust_layout(fig: plt.Figure, ax: plt.Axes,
                       legend_position: str = "auto") -> plt.Figure:
    """
    自动调整图表布局

    Args:
        fig: matplotlib Figure对象
        ax: matplotlib Axes对象
        legend_position: 图例位置，"auto"表示自动选择

    Returns:
        调整后的Figure对象
    """
    # 检测重叠
    if check_overlap(ax):
        # 自动调整图例位置
        if legend_position == "auto":
            best_position = find_best_legend_position(ax)
            ax.legend(loc=best_position, bbox_to_anchor=(1.05, 1))
        else:
            ax.legend(loc=legend_position, bbox_to_anchor=(1.05, 1))

        # 调整子图间距
        plt.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.1)

    # 使用tight_layout
    plt.tight_layout()

    return fig


def setup_chinese_font() -> None:
    """
    设置中文字体
    """
    # Windows系统
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False


def setup_english_font() -> None:
    """
    设置英文字体
    """
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
    plt.rcParams['axes.unicode_minus'] = False


def detect_language(text: str) -> str:
    """
    检测文本语言

    Args:
        text: 文本内容

    Returns:
        语言代码："chinese" 或 "english"
    """
    # 中文字符范围
    chinese_chars = sum(1 for char in text if '一' <= char <= '鿿')

    # 判断语言
    if chinese_chars / len(text) > 0.3:
        return "chinese"
    else:
        return "english"


def setup_font_by_language(text: str, language: str = "auto") -> str:
    """
    根据语言自动设置字体

    Args:
        text: 文本内容
        language: 语言代码，"auto"表示自动检测

    Returns:
        实际使用的语言
    """
    if language == "auto":
        language = detect_language(text)

    if language == "chinese":
        setup_chinese_font()
    else:
        setup_english_font()

    return language


def adjust_figure_size(fig: plt.Figure, width: float = 10,
                       height: float = 6) -> plt.Figure:
    """
    调整图表尺寸

    Args:
        fig: matplotlib Figure对象
        width: 宽度（英寸）
        height: 高度（英寸）

    Returns:
        调整后的Figure对象
    """
    fig.set_size_inches(width, height)
    return fig


def add_grid(ax: plt.Axes, alpha: float = 0.3) -> None:
    """
    添加网格线

    Args:
        ax: matplotlib Axes对象
        alpha: 透明度
    """
    ax.grid(True, alpha=alpha, linestyle='--')


def remove_top_right_spines(ax: plt.Axes) -> None:
    """
    移除顶部和右侧边框

    Args:
        ax: matplotlib Axes对象
    """
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


def set_axis_style(ax: plt.Axes, font_size: int = 7,
                   line_width: float = 0.8) -> None:
    """
    设置坐标轴样式

    Args:
        ax: matplotlib Axes对象
        font_size: 字体大小
        line_width: 线宽
    """
    # 设置字体大小
    ax.tick_params(axis='both', which='major', labelsize=font_size)

    # 设置线宽
    ax.spines['left'].set_linewidth(line_width)
    ax.spines['bottom'].set_linewidth(line_width)

    # 移除顶部和右侧边框
    remove_top_right_spines(ax)


def create_publication_style_figure(width: float = 10, height: float = 6,
                                    font_size: int = 7) -> Tuple[plt.Figure, plt.Axes]:
    """
    创建出版风格的图表

    Args:
        width: 宽度（英寸）
        height: 高度（英寸）
        font_size: 字体大小

    Returns:
        (Figure, Axes) 元组
    """
    # 创建图表
    fig, ax = plt.subplots(figsize=(width, height))

    # 设置样式
    set_axis_style(ax, font_size=font_size)
    add_grid(ax)

    return fig, ax
