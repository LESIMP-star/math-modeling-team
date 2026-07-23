"""
K-Means聚类算法
适用于数据分类、模式识别
用法: python kmeans.py --input data.csv --features x,y --k 3 --output result.png
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, COLORS, save_fig


def kmeans_cluster(X, k_range=None, seed=42):
    """
    K-Means聚类，自动选择最优K

    参数:
        X: array-like, 特征矩阵
        k_range: list, 尝试的K值范围
        seed: int, 随机种子

    返回:
        dict, 聚类结果、最优K、轮廓系数
    """
    if k_range is None:
        k_range = range(2, min(11, len(X)))

    X_scaled = StandardScaler().fit_transform(X)

    # 肘部法 + 轮廓系数
    inertias = []
    silhouettes = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=seed, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))

    best_k = list(k_range)[np.argmax(silhouettes)]
    best_km = KMeans(n_clusters=best_k, random_state=seed, n_init=10)
    labels = best_km.fit_predict(X_scaled)

    return {
        'labels': labels,
        'centers': best_km.cluster_centers_,
        'best_k': best_k,
        'inertias': inertias,
        'silhouettes': silhouettes,
        'k_range': list(k_range),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='K-Means聚类')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--features', type=str, required=True, help='特征列名，逗号分隔')
    parser.add_argument('--k', type=int, default=None, help='聚类数（None则自动选择）')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    feature_cols = [c.strip() for c in args.features.split(',')]
    X = data[feature_cols].values

    k_range = range(2, min(11, len(X))) if args.k is None else range(args.k, args.k + 1)
    result = kmeans_cluster(X, k_range)

    print("\n=== K-Means聚类结果 ===")
    print(f"最优K: {result['best_k']}")
    print(f"各K轮廓系数: {dict(zip(result['k_range'], [f'{s:.4f}' for s in result['silhouettes']]))}")

    if args.output and X.shape[1] >= 2:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # 肘部法
        axes[0].plot(result['k_range'], result['inertias'], 'o-', color=C["blue"], lw=2)
        axes[0].set_xlabel("K")
        axes[0].set_ylabel("惯性 (Inertia)")
        axes[0].set_title("肘部法")

        # 聚类结果（取前两个特征）
        for i in range(result['best_k']):
            mask = result['labels'] == i
            axes[1].scatter(X[mask, 0], X[mask, 1], c=COLORS[i % len(COLORS)],
                           s=40, alpha=0.6, label=f'簇 {i+1}')
        axes[1].set_xlabel(feature_cols[0])
        axes[1].set_ylabel(feature_cols[1])
        axes[1].set_title(f'K-Means聚类 (K={result["best_k"]})')
        axes[1].legend()

        save_fig(fig, "kmeans_result", save_dir=os.path.dirname(args.output) or '.')
