"""
DBSCAN密度聚类算法
适用于噪声数据聚类、任意形状簇识别
用法: python dbscan.py --input data.csv --features x,y --eps 0.5 --min_samples 5
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, COLORS, save_fig


def dbscan_cluster(X, eps=0.5, min_samples=5):
    """
    DBSCAN密度聚类

    参数:
        X: array-like, 特征矩阵
        eps: float, 邻域半径
        min_samples: int, 最小样本数

    返回:
        dict, 聚类结果
    """
    X_scaled = StandardScaler().fit_transform(X)

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(X_scaled)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    return {
        'labels': labels,
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'core_sample_indices': db.core_sample_indices_,
    }


def suggest_eps(X, k=5):
    """用K距离图建议eps值"""
    X_scaled = StandardScaler().fit_transform(X)
    nn = NearestNeighbors(n_neighbors=k)
    nn.fit(X_scaled)
    distances, _ = nn.kneighbors(X_scaled)
    k_distances = np.sort(distances[:, -1])
    return k_distances


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DBSCAN密度聚类')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--features', type=str, required=True, help='特征列名，逗号分隔')
    parser.add_argument('--eps', type=float, default=0.5, help='邻域半径')
    parser.add_argument('--min_samples', type=int, default=5, help='最小样本数')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    data = pd.read_csv(args.input)
    feature_cols = [c.strip() for c in args.features.split(',')]
    X = data[feature_cols].values

    result = dbscan_cluster(X, eps=args.eps, min_samples=args.min_samples)

    print("\n=== DBSCAN聚类结果 ===")
    print(f"聚类数: {result['n_clusters']}")
    print(f"噪声点: {result['n_noise']}")

    if args.output and X.shape[1] >= 2:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # K距离图
        k_distances = suggest_eps(X)
        axes[0].plot(k_distances, color=C["blue"], lw=2)
        axes[0].axhline(args.eps, color=C["red"], ls='--', lw=1.5, label=f'eps={args.eps}')
        axes[0].set_xlabel("样本排序")
        axes[0].set_ylabel(f"K距离")
        axes[0].set_title("K距离图 (选择eps)")
        axes[0].legend()

        # 聚类结果
        labels = result['labels']
        unique_labels = set(labels)
        for i, label in enumerate(unique_labels):
            if label == -1:
                color = C["gray"]
                label_name = "噪声"
                marker = 'x'
            else:
                color = COLORS[i % len(COLORS)]
                label_name = f'簇 {label + 1}'
                marker = 'o'
            mask = labels == label
            axes[1].scatter(X[mask, 0], X[mask, 1], c=color, s=40,
                           alpha=0.6, marker=marker, label=label_name)
        axes[1].set_xlabel(feature_cols[0])
        axes[1].set_ylabel(feature_cols[1])
        axes[1].set_title(f'DBSCAN聚类 ({result["n_clusters"]}簇, {result["n_noise"]}噪声)')
        axes[1].legend()

        save_fig(fig, "dbscan_result", save_dir=os.path.dirname(args.output) or '.')
