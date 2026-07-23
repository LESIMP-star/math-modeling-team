"""
遗传算法 (Genetic Algorithm)
适用于组合优化、函数优化、参数寻优
用法: python genetic_algorithm.py --func "x**2 + y**2" --bounds "-5,5;-5,5" --pop 100 --gen 200
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotting.utils import C, save_fig


def genetic_algorithm(func, bounds, pop_size=100, n_gen=200,
                      crossover_rate=0.8, mutation_rate=0.1, seed=42):
    """
    遗传算法求解函数最小值

    参数:
        func: callable, 目标函数 f(x) -> float, x为numpy数组
        bounds: list of tuples, 各维度上下界 [(lb, ub), ...]
        pop_size: int, 种群大小
        n_gen: int, 迭代代数
        crossover_rate: float, 交叉概率
        mutation_rate: float, 变异概率
        seed: int, 随机种子

    返回:
        dict, 最优解、最优值、收敛曲线
    """
    np.random.seed(seed)
    n_dim = len(bounds)
    lb = np.array([b[0] for b in bounds])
    ub = np.array([b[1] for b in bounds])

    # 初始化种群
    pop = lb + (ub - lb) * np.random.rand(pop_size, n_dim)
    fitness = np.array([func(ind) for ind in pop])

    best_history = []
    best_idx = np.argmin(fitness)
    best_x = pop[best_idx].copy()
    best_f = fitness[best_idx]

    for gen in range(n_gen):
        # 选择（锦标赛选择）
        new_pop = np.zeros_like(pop)
        for i in range(pop_size):
            candidates = np.random.choice(pop_size, 3, replace=False)
            winner = candidates[np.argmin(fitness[candidates])]
            new_pop[i] = pop[winner]

        # 交叉（模拟二进制交叉 SBX）
        for i in range(0, pop_size - 1, 2):
            if np.random.rand() < crossover_rate:
                alpha = np.random.rand(n_dim)
                p1, p2 = new_pop[i], new_pop[i + 1]
                new_pop[i] = alpha * p1 + (1 - alpha) * p2
                new_pop[i + 1] = alpha * p2 + (1 - alpha) * p1

        # 多项式变异
        for i in range(pop_size):
            if np.random.rand() < mutation_rate:
                idx = np.random.randint(n_dim)
                new_pop[i, idx] += np.random.randn() * (ub[idx] - lb[idx]) * 0.1
                new_pop[i, idx] = np.clip(new_pop[i, idx], lb[idx], ub[idx])

        pop = new_pop
        fitness = np.array([func(ind) for ind in pop])

        best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_f:
            best_f = fitness[best_idx]
            best_x = pop[best_idx].copy()

        best_history.append(best_f)

    return {
        'best_x': best_x,
        'best_f': best_f,
        'convergence': best_history,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='遗传算法')
    parser.add_argument('--func', type=str, required=True, help='目标函数（如 "x[0]**2 + x[1]**2"）')
    parser.add_argument('--bounds', type=str, required=True, help='边界（如 "-5,5;-5,5"）')
    parser.add_argument('--pop', type=int, default=100, help='种群大小')
    parser.add_argument('--gen', type=int, default=200, help='迭代代数')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')

    args = parser.parse_args()

    bounds = []
    for b in args.bounds.split(';'):
        parts = b.split(',')
        bounds.append((float(parts[0]), float(parts[1])))

    func = eval(f"lambda x: {args.func}")

    result = genetic_algorithm(func, bounds, pop_size=args.pop, n_gen=args.gen)

    print("\n=== 遗传算法结果 ===")
    print(f"最优解: {result['best_x']}")
    print(f"最优值: {result['best_f']:.6f}")

    if args.output:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(result['convergence'], color=C["blue"], lw=2)
        ax.set_xlabel("迭代代数", fontsize=14)
        ax.set_ylabel("最优适应度", fontsize=14)
        ax.set_title("遗传算法收敛曲线", fontsize=16, fontweight='bold')
        ax.set_yscale('log')
        save_fig(fig, "ga_convergence", save_dir=os.path.dirname(args.output) or '.')
