"""
Lasso特征选择 + 预警阈值计算
适用于多因素分析和预警系统
用法: python lasso_feature_selection.py --input data.csv --target_col y --feature_cols a,b,c --output result.png
"""
import argparse
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, COLORS, save_fig


def lasso_select_features(X, y, feature_names=None):
    """
    Lasso + 互信息综合特征选择

    参数:
        X: array-like, 特征矩阵 (n_samples, n_features)
        y: array-like, 目标变量
        feature_names: list, 特征名称

    返回:
        dict, 包含特征重要性排名和选中的特征
    """
    n_features = X.shape[1]
    if feature_names is None:
        feature_names = [f'特征{i+1}' for i in range(n_features)]

    # 标准化
    X_scaled = StandardScaler().fit_transform(X)

    # Lasso回归
    lasso = LassoCV(cv=5, max_iter=10000, random_state=42).fit(X_scaled, y)

    # 互信息
    mi = mutual_info_regression(X_scaled, y, random_state=42)

    # 综合排名
    importance = {}
    for name, coef, mi_val in zip(feature_names, np.abs(lasso.coef_), mi):
        importance[name] = {
            'lasso_coef': coef,
            'mutual_info': mi_val,
            'combined': coef + mi_val * 0.5
        }

    ranked = sorted(importance.items(), key=lambda x: x[1]['combined'], reverse=True)

    return {
        'importance': importance,
        'ranked': ranked,
        'selected': [name for name, _ in ranked],
        'lasso_model': lasso,
    }


def calculate_warning_thresholds(values, time_step=1.0):
    """
    计算预警阈值（统计法 + 切线角法）

    参数:
        values: array-like, 位移/变形数据
        time_step: float, 时间步长（小时）

    返回:
        dict, 预警阈值和置信区间
    """
    n = len(values)
    values = np.array(values, dtype=float)

    # 速度计算
    velocity = np.gradient(values) / time_step
    ws = min(51, n // 10 * 2 + 1)
    if ws % 2 == 0:
        ws += 1
    v_smooth = savgol_filter(velocity, ws, 3)

    # 切线角
    theta = np.arctan(v_smooth) * 180 / np.pi

    # 统计法阈值
    v_mean, v_std = np.mean(v_smooth), np.std(v_smooth)
    v_yellow_stat = v_mean + 2.5 * v_std
    v_red_stat = v_mean + 4 * v_std

    # 切线角法阈值
    v_45 = np.tan(np.radians(45))
    v_80 = np.tan(np.radians(80))

    # Bootstrap不确定性分析
    from sklearn.utils import resample
    n_boot = 1000
    yellow_boot, red_boot = [], []
    for _ in range(n_boot):
        idx = resample(range(n))
        vs_boot = v_smooth[idx]
        yellow_boot.append(np.mean(vs_boot) + 2.5 * np.std(vs_boot))
        red_boot.append(np.mean(vs_boot) + 4 * np.std(vs_boot))

    yellow_ci = np.percentile(yellow_boot, [2.5, 97.5])
    red_ci = np.percentile(red_boot, [2.5, 97.5])

    # 预警起点
    t_yellow = np.where(theta > 45)[0]
    t_red = np.where(theta > 80)[0]

    return {
        'velocity': v_smooth,
        'theta': theta,
        'stat_yellow': v_yellow_stat,
        'stat_red': v_red_stat,
        'tangent_45': v_45,
        'tangent_80': v_80,
        'yellow_ci': yellow_ci.tolist(),
        'red_ci': red_ci.tolist(),
        'yellow_start': int(t_yellow[0]) if len(t_yellow) > 0 else None,
        'red_start': int(t_red[0]) if len(t_red) > 0 else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lasso特征选择 + 预警阈值')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--target_col', type=str, required=True, help='目标变量列名')
    parser.add_argument('--feature_cols', type=str, required=True, help='特征列名，逗号分隔')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    feature_cols = [c.strip() for c in args.feature_cols.split(',')]

    y = data[args.target_col].values
    X = data[feature_cols].values

    # 特征选择
    result = lasso_select_features(X, y, feature_cols)

    print("\n=== 特征选择结果 ===")
    for name, info in result['ranked']:
        print(f"  {name}: Lasso系数={info['lasso_coef']:.4f}, 互信息={info['mutual_info']:.4f}, 综合={info['combined']:.4f}")

    # 预警阈值
    thresholds = calculate_warning_thresholds(y)
    print(f"\n=== 预警阈值 ===")
    print(f"  统计法: 黄色>{thresholds['stat_yellow']:.4f}, 红色>{thresholds['stat_red']:.4f}")
    print(f"  切线角法: 45°→v>{thresholds['tangent_45']:.4f}, 80°→v>{thresholds['tangent_80']:.4f}")
    print(f"  黄色预警95%CI: [{thresholds['yellow_ci'][0]:.4f}, {thresholds['yellow_ci'][1]:.4f}]")
    print(f"  红色预警95%CI: [{thresholds['red_ci'][0]:.4f}, {thresholds['red_ci'][1]:.4f}]")

    if args.output:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # 特征重要性
        si = np.argsort([info['combined'] for _, info in result['ranked']])
        names = [result['ranked'][i][0] for i in si]
        vals = [result['ranked'][i][1]['combined'] for i in si]
        ax1.barh(range(len(names)), vals, color=COLORS[:len(names)], edgecolor='black', linewidth=1.5)
        ax1.set_yticks(range(len(names)))
        ax1.set_yticklabels(names)
        ax1.set_xlabel("综合重要性")
        ax1.set_title("Lasso + 互信息特征重要性")

        # 预警图
        n = len(y)
        tx = np.arange(n)
        ax2.plot(tx, thresholds['velocity'], color=C["blue"], lw=2, label="速度")
        ax2.axhline(thresholds['tangent_45'], color=C["gold"], ls='--', lw=1.5)
        ax2.axhline(thresholds['tangent_80'], color=C["red"], ls='--', lw=1.5)
        ax2.fill_between(tx, thresholds['yellow_ci'][0], thresholds['yellow_ci'][1], alpha=0.15, color=C["gold"])
        ax2.fill_between(tx, thresholds['red_ci'][0], thresholds['red_ci'][1], alpha=0.15, color=C["red"])
        ax2.set_xlabel("时间步")
        ax2.set_ylabel("速度")
        ax2.set_title("预警阈值")
        ax2.legend()

        save_fig(fig, "feature_selection_warning", save_dir=os.path.dirname(args.output) or '.')
