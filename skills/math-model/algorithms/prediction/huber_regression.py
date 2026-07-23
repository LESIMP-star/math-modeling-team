"""
Huber鲁棒回归校准算法
适用于数据存在异常值的回归校准场景
用法: python huber_regression.py --input data.csv --x_col A --y_col B --output result.png
"""
import argparse
import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, save_fig


def huber_calibrate(x, y, epsilon=1.35):
    """
    Huber鲁棒回归校准

    参数:
        x: array-like, 原始测量值
        y: array-like, 基准值/真实值
        epsilon: float, Huber损失的阈值参数

    返回:
        dict, 包含校准方程、校准后数据、精度指标
    """
    x = np.array(x, dtype=float).reshape(-1, 1)
    y = np.array(y, dtype=float)

    # Huber回归
    model = HuberRegressor(epsilon=epsilon, max_iter=200)
    model.fit(x, y)
    y_pred = model.predict(x)
    alpha = model.coef_[0]
    beta = model.intercept_

    # 跳变修正（3σ原则）
    resid = np.abs(y_pred - y)
    sigma = np.nanstd(resid)
    spikes = resid > 3 * sigma
    for idx in np.where(spikes)[0]:
        lo, hi = max(0, idx - 6), min(len(x), idx + 6)
        y_pred[idx] = np.median(y_pred[lo:hi])

    # 精度指标
    mae_before = mean_absolute_error(y, x.flatten())
    rmse_before = np.sqrt(mean_squared_error(y, x.flatten()))
    r2_before = r2_score(y, x.flatten())

    mae_after = mean_absolute_error(y, y_pred)
    rmse_after = np.sqrt(mean_squared_error(y, y_pred))
    r2_after = r2_score(y, y_pred)

    return {
        'alpha': alpha,
        'beta': beta,
        'equation': f'y = {alpha:.4f} * x + {beta:.4f}',
        'y_calibrated': y_pred,
        'spikes_count': int(spikes.sum()),
        'metrics_before': {'MAE': mae_before, 'RMSE': rmse_before, 'R2': r2_before},
        'metrics_after': {'MAE': mae_after, 'RMSE': rmse_after, 'R2': r2_after},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Huber鲁棒回归校准')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--x_col', type=str, required=True, help='原始测量值列名')
    parser.add_argument('--y_col', type=str, required=True, help='基准值列名')
    parser.add_argument('--epsilon', type=float, default=1.35, help='Huber阈值参数')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    x = data[args.x_col].values
    y = data[args.y_col].values

    result = huber_calibrate(x, y, args.epsilon)

    print("\n=== Huber回归校准结果 ===")
    print(f"校准方程: {result['equation']}")
    print(f"检测到跳变点: {result['spikes_count']} 个")
    print(f"校正前: MAE={result['metrics_before']['MAE']:.4f}, RMSE={result['metrics_before']['RMSE']:.4f}, R²={result['metrics_before']['R2']:.4f}")
    print(f"校正后: MAE={result['metrics_after']['MAE']:.4f}, RMSE={result['metrics_after']['RMSE']:.4f}, R²={result['metrics_after']['R2']:.4f}")

    if args.output:
        fig, ax = plt.subplots(figsize=(12, 6))
        t = np.arange(len(x))
        ax.plot(t, x, color=C["gray"], lw=1.5, alpha=0.7, label="原始值")
        ax.plot(t, y, color=C["blue"], lw=2.0, label="基准值")
        ax.plot(t, result['y_calibrated'], color=C["red"], lw=2.0, ls="--", label="校准后")
        ax.set_xlabel("样本序号")
        ax.set_ylabel("测量值")
        ax.set_title("Huber回归校准对比")
        ax.legend()
        save_fig(fig, "huber_calibration", save_dir=os.path.dirname(args.output) or '.')
