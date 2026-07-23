"""
模拟退火算法 (Simulated Annealing)
适用于连续优化、组合优化
用法: python simulated_annealing.py --func "x**2 + y**2" --bounds "-5,5;-5,5" --temp 1000
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, save_fig


def simulated_annealing(func, bounds, T_init=1000, T_min=1e-8,
                        alpha=0.99, n_iter=1000, seed=42):
    """
    模拟退火算法

    参数:
        func: callable, 目标函数
        bounds: list of tuples, 各维度上下界
        T_init: float, 初始温度
        T_min: float, 终止温度
        alpha: float, 降温系数
        n_iter: int, 每个温度的迭代次数
        seed: int, 随机种子

    返回:
        dict, 最优解、最优值、收敛曲线
    """
    np.random.seed(seed)
    n_dim = len(bounds)
    lb = np.array([b[0] for b in bounds])
    ub = np.array([b[1] for b in bounds])

    # 初始解
    x = lb + (ub - lb) * np.random.rand(n_dim)
    f = func(x)

    best_x = x.copy()
    best_f = f

    T = T_init
    history = [best_f]
    temp_history = [T]

    while T > T_min:
        for _ in range(n_iter):
            # 邻域搜索
            x_new = x + np.random.randn(n_dim) * T * 0.01
            x_new = np.clip(x_new, lb, ub)
            f_new = func(x_new)

            # Metropolis准则
            delta = f_new - f
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                x = x_new
                f = f_new

                if f < best_f:
                    best_f = f
                    best_x = x.copy()

        T *= alpha
        history.append(best_f)
        temp_history.append(T)

    return {
        'best_x': best_x,
        'best_f': best_f,
        'convergence': history,
        'temperatures': temp_history,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='模拟退火算法')
    parser.add_argument('--func', type=str, required=True, help='目标函数')
    parser.add_argument('--bounds', type=str, required=True, help='边界（如 "-5,5;-5,5"）')
    parser.add_argument('--temp', type=float, default=1000, help='初始温度')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    bounds = []
    for b in args.bounds.split(';'):
        parts = b.split(',')
        bounds.append((float(parts[0]), float(parts[1])))

    func = eval(f"lambda x: {args.func}")

    result = simulated_annealing(func, bounds, T_init=args.temp)

    print("\n=== 模拟退火结果 ===")
    print(f"最优解: {result['best_x']}")
    print(f"最优值: {result['best_f']:.6f}")

    if args.output:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        ax1.plot(result['convergence'], color=C["blue"], lw=2)
        ax1.set_xlabel("温度轮次")
        ax1.set_ylabel("最优适应度")
        ax1.set_title("收敛曲线")
        ax1.set_yscale('log')
        ax2.plot(result['temperatures'], color=C["red"], lw=2)
        ax2.set_xlabel("轮次")
        ax2.set_ylabel("温度")
        ax2.set_title("降温过程")
        ax2.set_yscale('log')
        save_fig(fig, "sa_convergence", save_dir=os.path.dirname(args.output) or '.')
