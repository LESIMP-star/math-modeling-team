"""
灵敏度分析图
适用于模型参数灵敏度分析展示
用法: python sensitivity.py --input data.csv --param_col param --result_col result --output fig.png
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import C, save_fig


def sensitivity_plot(data, param_col, result_col, title="灵敏度分析",
                     save_path=None, save_dir='./output/figures'):
    """
    灵敏度分析折线图

    参数:
        data: DataFrame, 包含参数列和结果列
        param_col: str, 参数列名
        result_col: str, 结果列名
        title: str, 图表标题
        save_path: str, 保存文件名
        save_dir: str, 保存目录
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data[param_col], data[result_col], 'o-', color=C["blue"], lw=2.5, markersize=8)
    ax.fill_between(data[param_col], data[result_col], alpha=0.15, color=C["blue"])
    ax.set_xlabel(param_col, fontsize=14)
    ax.set_ylabel(result_col, fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    if save_path:
        save_fig(fig, save_path, save_dir=save_dir)
    return fig


def tornado_plot(params, sensitivities, title="龙卷风图", save_path=None, save_dir='./output/figures'):
    """
    龙卷风图（参数灵敏度排序）

    参数:
        params: list, 参数名称
        sensitivities: list, 灵敏度值
        title: str, 图表标题
        save_path: str, 保存文件名
        save_dir: str, 保存目录
    """
    sorted_idx = np.argsort(np.abs(sensitivities))
    sorted_params = [params[i] for i in sorted_idx]
    sorted_sens = [sensitivities[i] for i in sorted_idx]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [C["red"] if s > 0 else C["blue"] for s in sorted_sens]
    ax.barh(range(len(sorted_params)), sorted_sens, color=colors, edgecolor='black', linewidth=1.2)
    ax.set_yticks(range(len(sorted_params)))
    ax.set_yticklabels(sorted_params, fontsize=12)
    ax.set_xlabel("灵敏度系数", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axvline(0, color='black', lw=1)

    if save_path:
        save_fig(fig, save_path, save_dir=save_dir)
    return fig


def multi_param_sensitivity(results_dict, title="多参数灵敏度分析",
                            save_path=None, save_dir='./output/figures'):
    """
    多参数灵敏度热力图

    参数:
        results_dict: dict, {参数名: [不同取值下的结果]}
        title: str, 图表标题
        save_path: str, 保存文件名
        save_dir: str, 保存目录
    """
    params = list(results_dict.keys())
    values = np.array(list(results_dict.values()))

    # 标准化
    values_norm = (values - values.min(axis=1, keepdims=True)) / \
                  (values.max(axis=1, keepdims=True) - values.min(axis=1, keepdims=True) + 1e-10)

    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(values_norm, aspect='auto', cmap='RdBu_r', vmin=0, vmax=1)
    ax.set_yticks(range(len(params)))
    ax.set_yticklabels(params, fontsize=12)
    ax.set_xlabel("参数取值水平", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    plt.colorbar(im, ax=ax, label="标准化结果")

    if save_path:
        save_fig(fig, save_path, save_dir=save_dir)
    return fig


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='灵敏度分析图')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--param_col', type=str, required=True, help='参数列名')
    parser.add_argument('--result_col', type=str, required=True, help='结果列名')
    parser.add_argument('--title', type=str, default='灵敏度分析', help='图表标题')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    save_dir = os.path.dirname(args.output) if args.output else './output/figures'

    sensitivity_plot(data, args.param_col, args.result_col,
                     title=args.title, save_path='sensitivity', save_dir=save_dir)
