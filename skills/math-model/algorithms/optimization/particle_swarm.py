"""
粒子群优化算法 (Particle Swarm Optimization)
适用于连续函数优化
用法: python particle_swarm.py --func "x**2 + y**2" --bounds "-5,5;-5,5" --particles 50
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, save_fig


def particle_swarm(func, bounds, n_particles=50, n_iter=200,
                   w=0.7, c1=1.5, c2=1.5, seed=42):
    """
    粒子群优化算法

    参数:
        func: callable, 目标函数
        bounds: list of tuples, 各维度上下界
        n_particles: int, 粒子数量
        n_iter: int, 迭代次数
        w: float, 惯性权重
        c1: float, 个体学习因子
        c2: float, 社会学习因子
        seed: int, 随机种子

    返回:
        dict, 最优解、最优值、收敛曲线
    """
    np.random.seed(seed)
    n_dim = len(bounds)
    lb = np.array([b[0] for b in bounds])
    ub = np.array([b[1] for b in bounds])

    # 初始化粒子位置和速度
    pos = lb + (ub - lb) * np.random.rand(n_particles, n_dim)
    vel = np.random.randn(n_particles, n_dim) * 0.1

    # 个体最优
    p_best_pos = pos.copy()
    p_best_fit = np.array([func(p) for p in pos])

    # 全局最优
    g_best_idx = np.argmin(p_best_fit)
    g_best_pos = p_best_pos[g_best_idx].copy()
    g_best_fit = p_best_fit[g_best_idx]

    convergence = [g_best_fit]

    for it in range(n_iter):
        r1 = np.random.rand(n_particles, n_dim)
        r2 = np.random.rand(n_particles, n_dim)

        # 更新速度和位置
        vel = w * vel + c1 * r1 * (p_best_pos - pos) + c2 * r2 * (g_best_pos - pos)
        pos = pos + vel
        pos = np.clip(pos, lb, ub)

        # 计算适应度
        fit = np.array([func(p) for p in pos])

        # 更新个体最优
        better = fit < p_best_fit
        p_best_pos[better] = pos[better]
        p_best_fit[better] = fit[better]

        # 更新全局最优
        best_idx = np.argmin(p_best_fit)
        if p_best_fit[best_idx] < g_best_fit:
            g_best_fit = p_best_fit[best_idx]
            g_best_pos = p_best_pos[best_idx].copy()

        convergence.append(g_best_fit)

    return {
        'best_x': g_best_pos,
        'best_f': g_best_fit,
        'convergence': convergence,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='粒子群优化算法')
    parser.add_argument('--func', type=str, required=True, help='目标函数')
    parser.add_argument('--bounds', type=str, required=True, help='边界（如 "-5,5;-5,5"）')
    parser.add_argument('--particles', type=int, default=50, help='粒子数量')
    parser.add_argument('--iter', type=int, default=200, help='迭代次数')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    bounds = []
    for b in args.bounds.split(';'):
        parts = b.split(',')
        bounds.append((float(parts[0]), float(parts[1])))

    func = eval(f"lambda x: {args.func}")

    result = particle_swarm(func, bounds, n_particles=args.particles, n_iter=args.iter)

    print("\n=== 粒子群优化结果 ===")
    print(f"最优解: {result['best_x']}")
    print(f"最优值: {result['best_f']:.6f}")

    if args.output:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(result['convergence'], color=C["teal"], lw=2)
        ax.set_xlabel("迭代次数", fontsize=14)
        ax.set_ylabel("全局最优适应度", fontsize=14)
        ax.set_title("粒子群优化收敛曲线", fontsize=16, fontweight='bold')
        ax.set_yscale('log')
        save_fig(fig, "pso_convergence", save_dir=os.path.dirname(args.output) or '.')
