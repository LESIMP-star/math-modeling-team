"""
相关性分析图
适用于变量间相关性展示
用法: python correlation.py --input data.csv --features x1,x2,x3,y --output fig.png
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import C, save_fig


def correlation_heatmap(data, features=None, title="相关性热力图",
                        save_path=None, save_dir='./output/figures'):
    """
    相关性热力图

    参数:
        data: DataFrame
        features: list, 特征列名（None则用所有数值列）
        title: str, 图表标题
        save_path: str, 保存文件名
        save_dir: str, 保存目录
    """
    if features:
        corr = data[features].corr()
    else:
        corr = data.select_dtypes(include=[np.number]).corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, square=True, linewidths=0.5, ax=ax,
                cbar_kws={'label': '相关系数'})
    ax.set_title(title, fontsize=16, fontweight='bold')

    if save_path:
        save_fig(fig, save_path, save_dir=save_dir)
    return fig


def scatter_matrix(data, features=None, hue_col=None, title="散点矩阵",
                   save_path=None, save_dir='./output/figures'):
    """
    散点矩阵图（配对图）

    参数:
        data: DataFrame
        features: list, 特征列名
        hue_col: str, 分类列名（用于着色）
        title: str, 图表标题
        save_path: str, 保存文件名
        save_dir: str, 保存目录
    """
    if features:
        plot_data = data[features + ([hue_col] if hue_col else [])]
    else:
        plot_data = data

    g = sns.pairplot(plot_data, hue=hue_col, diag_kind='kde',
                     plot_kws={'alpha': 0.6, 's': 30},
                     palette=sns.color_palette("husl", data[hue_col].nunique()) if hue_col else None)
    g.figure.suptitle(title, y=1.02, fontsize=16, fontweight='bold')

    if save_path:
        g.savefig(os.path.join(save_dir, f"{save_path}.png"), dpi=600, bbox_inches='tight')
        plt.close(g.figure)
        print(f"图表已保存: {save_dir}/{save_path}")
    return g


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='相关性分析图')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--features', type=str, default=None, help='特征列名，逗号分隔')
    parser.add_argument('--title', type=str, default='相关性分析', help='图表标题')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    features = [c.strip() for c in args.features.split(',')] if args.features else None
    save_dir = os.path.dirname(args.output) if args.output else './output/figures'

    correlation_heatmap(data, features, title=args.title,
                        save_path='correlation_heatmap', save_dir=save_dir)
