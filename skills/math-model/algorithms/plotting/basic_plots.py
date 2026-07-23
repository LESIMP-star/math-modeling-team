"""
基础绘图工具
适用于数学建模竞赛论文图表生成
支持：折线图、柱状图、散点图、饼图、热力图
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 设置专业风格
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.figsize'] = (8, 6)


def line_plot(data, x_col, y_cols, title="", xlabel="", ylabel="", save_path=None):
    """折线图：适用于趋势分析"""
    fig, ax = plt.subplots()
    for col in y_cols:
        ax.plot(data[x_col], data[col], marker='o', markersize=4, label=col)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    plt.close(fig)
    return fig


def bar_plot(data, x_col, y_col, title="", xlabel="", ylabel="", save_path=None):
    """柱状图：适用于对比分析"""
    fig, ax = plt.subplots()
    colors = sns.color_palette("husl", len(data))
    ax.bar(data[x_col], data[y_col], color=colors)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    plt.close(fig)
    return fig


def scatter_plot(data, x_col, y_col, title="", xlabel="", ylabel="", save_path=None):
    """散点图：适用于相关性分析"""
    fig, ax = plt.subplots()
    ax.scatter(data[x_col], data[y_col], alpha=0.6, edgecolors='white', s=60)
    # 添加趋势线
    z = np.polyfit(data[x_col], data[y_col], 1)
    p = np.poly1d(z)
    ax.plot(data[x_col], p(data[x_col]), "r--", alpha=0.8, label=f'趋势线 (斜率={z[0]:.4f})')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend()
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    plt.close(fig)
    return fig


def heatmap_plot(data, title="", save_path=None):
    """热力图：适用于相关性矩阵"""
    fig, ax = plt.subplots()
    corr = data.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold')
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    plt.close(fig)
    return fig


def pie_plot(labels, sizes, title="", save_path=None):
    """饼图：适用于占比分析"""
    fig, ax = plt.subplots()
    colors = sns.color_palette("pastel", len(labels))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
           startangle=90, pctdistance=0.85)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title(title, fontsize=14, fontweight='bold')
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    plt.close(fig)
    return fig


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='基础绘图工具')
    parser.add_argument('--type', type=str, required=True,
                        choices=['line', 'bar', 'scatter', 'heatmap', 'pie'],
                        help='图表类型')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV/Excel)')
    parser.add_argument('--output', type=str, default='output.png', help='输出图片路径')
    parser.add_argument('--title', type=str, default='', help='图表标题')
    parser.add_argument('--x', type=str, help='X轴列名')
    parser.add_argument('--y', type=str, nargs='+', help='Y轴列名（可多个）')

    args = parser.parse_args()
    data = pd.read_csv(args.input) if args.input.endswith('.csv') else pd.read_excel(args.input)

    if args.type == 'line':
        line_plot(data, args.x, args.y, title=args.title, save_path=args.output)
    elif args.type == 'bar':
        bar_plot(data, args.x, args.y[0], title=args.title, save_path=args.output)
    elif args.type == 'scatter':
        scatter_plot(data, args.x, args.y[0], title=args.title, save_path=args.output)
    elif args.type == 'heatmap':
        heatmap_plot(data, title=args.title, save_path=args.output)
    elif args.type == 'pie':
        pie_plot(data[args.x].tolist(), data[args.y[0]].tolist(),
                 title=args.title, save_path=args.output)
