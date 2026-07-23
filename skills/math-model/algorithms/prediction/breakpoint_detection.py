"""
变点检测 + 分阶段拟合
适用于时间序列的阶段划分和趋势分析
用法: python breakpoint_detection.py --input data.csv --col displacement --output result.png
"""
import argparse
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, save_fig


def detect_breakpoints(data, min_size=50, jump=5, pen=10):
    """
    使用ruptures PELT算法检测变点

    参数:
        data: array-like, 时间序列数据
        min_size: int, 最小分段长度
        jump: int, 跳步
        pen: int, 惩罚系数

    返回:
        list, 变点位置索引
    """
    from ruptures import Pelt
    model = Pelt(model="rbf", min_size=min_size, jump=jump).fit(data.reshape(-1, 1))
    breaks = model.predict(pen=pen)
    return breaks


def fit_stages(data, breakpoints):
    """
    分阶段拟合：对数→线性→幂律

    参数:
        data: array-like, 平滑后的时间序列
        breakpoints: list, 变点位置

    返回:
        dict, 各阶段的拟合参数和模型
    """
    n = len(data)
    if len(breakpoints) >= 2:
        T1, T2 = breakpoints[0], breakpoints[-2]
    else:
        T1, T2 = n // 3, 2 * n // 3

    s1, s2, s3 = data[:T1], data[T1:T2], data[T2:]

    def log_m(t, a, b):
        return a * np.log(t + 1) + b

    def lin_m(t, a, b):
        return a * t + b

    def pow_m(t, a, p, b):
        return a * (t + 1) ** p + b

    p1 = curve_fit(log_m, np.arange(len(s1)), s1, p0=[1, s1[0]])[0] if len(s1) > 3 else [0, s1[0]]
    p2 = curve_fit(lin_m, np.arange(len(s2)), s2, p0=[(s2[-1] - s2[0]) / len(s2), s2[0]])[0] if len(s2) > 3 else [0, s2[0]]
    p3 = curve_fit(pow_m, np.arange(len(s3)), s3, p0=[1, 1.2, s3[0]], maxfev=5000)[0] if len(s3) > 3 else [1, 1, s3[0]]

    v1 = (s1[-1] - s1[0]) / len(s1) if len(s1) > 1 else 0
    v2 = (s2[-1] - s2[0]) / len(s2) if len(s2) > 1 else 0
    v3 = (s3[-1] - s3[0]) / len(s3) if len(s3) > 1 else 0

    return {
        'T1': T1, 'T2': T2,
        'stage1': {'model': '对数', 'params': p1.tolist(), 'speed': v1, 'range': (0, T1)},
        'stage2': {'model': '线性', 'params': p2.tolist(), 'speed': v2, 'range': (T1, T2)},
        'stage3': {'model': '幂律', 'params': p3.tolist(), 'speed': v3, 'range': (T2, n)},
    }


def full_analysis(series, smooth_window=None):
    """
    完整分析流程：平滑→速度/加速度→变点检测→分阶段拟合

    参数:
        series: array-like, 原始时间序列
        smooth_window: int, 平滑窗口大小（None则自动）

    返回:
        dict, 完整分析结果
    """
    n = len(series)
    series = np.array(series, dtype=float)

    # 平滑
    if smooth_window is None:
        smooth_window = min(101, n // 10 * 2 + 1)
    if smooth_window % 2 == 0:
        smooth_window += 1
    smoothed = savgol_filter(series, smooth_window, 3)

    # 速度/加速度
    velocity = np.gradient(smoothed)
    acceleration = np.gradient(velocity)

    # 变点检测
    v_smooth = savgol_filter(velocity, min(51, n // 10 * 2 + 1), 3)
    breakpoints = detect_breakpoints(v_smooth)

    # 分阶段拟合
    stages = fit_stages(smoothed, breakpoints)

    return {
        'original': series,
        'smoothed': smoothed,
        'velocity': velocity,
        'acceleration': acceleration,
        'breakpoints': breakpoints,
        'stages': stages,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='变点检测与分阶段拟合')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--col', type=str, required=True, help='目标列名')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    series = data[args.col].values

    result = full_analysis(series)

    print("\n=== 变点检测结果 ===")
    print(f"变点位置: {result['breakpoints']}")
    stages = result['stages']
    print(f"阶段1 (初始变形): T=0~{stages['T1']}, 模型={stages['stage1']['model']}, 速度={stages['stage1']['speed']:.4f}")
    print(f"阶段2 (匀速变形): T={stages['T1']}~{stages['T2']}, 模型={stages['stage2']['model']}, 速度={stages['stage2']['speed']:.4f}")
    print(f"阶段3 (加速变形): T={stages['T2']}~末尾, 模型={stages['stage3']['model']}, 速度={stages['stage3']['speed']:.4f}")

    if args.output:
        n = len(series)
        tx = np.arange(n)
        T1, T2 = stages['T1'], stages['T2']

        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
        labels = ["(a) 数据序列", "(b) 速度", "(c) 加速度"]
        ys = [result['smoothed'], result['velocity'], result['acceleration']]
        cs = [C["black"], C["blue"], C["teal"]]

        for i in range(3):
            ax = axes[i]
            ax.plot(tx, ys[i], color=cs[i], lw=2)
            ax.axvline(T1, color=C["gold"], ls='--', lw=2)
            ax.axvline(T2, color=C["red"], ls='--', lw=2)
            ax.axvspan(0, T1, alpha=0.08, color=C["green"])
            ax.axvspan(T1, T2, alpha=0.08, color=C["blue"])
            ax.axvspan(T2, n, alpha=0.08, color=C["red"])
            ax.set_ylabel(labels[i].split(")")[1])
            ax.set_title(labels[i])

        axes[-1].set_xlabel("时间步")
        save_fig(fig, "breakpoint_detection", save_dir=os.path.dirname(args.output) or '.')
