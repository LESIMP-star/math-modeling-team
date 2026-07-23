"""
灰色预测 GM(1,1) 模型
适用于小样本、短期预测
用法: python grey_prediction.py --input data.csv --col target --predict 5
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def gm11(data, predict_n=5):
    """
    GM(1,1) 灰色预测

    参数:
        data: array-like, 原始时间序列数据
        predict_n: int, 预测期数

    返回:
        dict, 包含拟合值、预测值、精度指标
    """
    x0 = np.array(data, dtype=float)
    n = len(x0)

    # 1. 累加生成序列 (AGO)
    x1 = np.cumsum(x0)

    # 2. 紧邻均值生成序列
    z1 = 0.5 * (x1[:-1] + x1[1:])

    # 3. 构建数据矩阵 B 和 Y
    B = np.column_stack((-z1, np.ones(n - 1)))
    Y = x0[1:].reshape(-1, 1)

    # 4. 最小二乘法求参数
    params = np.linalg.inv(B.T @ B) @ B.T @ Y
    a = params[0, 0]  # 发展系数
    b = params[1, 0]  # 灰色作用量

    # 5. 预测模型
    def x1_hat(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    # 6. 拟合值（还原）
    x1_hat_vals = np.array([x1_hat(k) for k in range(n + predict_n)])
    x0_hat = np.diff(x1_hat_vals)
    x0_hat = np.insert(x0_hat, 0, x0[0])

    # 7. 拟合精度
    fitted = x0_hat[:n]
    residuals = x0 - fitted
    relative_errors = np.abs(residuals) / x0 * 100

    # 后验差比检验
    s1 = np.std(x0, ddof=1)
    s2 = np.std(residuals, ddof=1)
    C = s2 / s1  # 后验差比值

    # 小误差概率
    P = np.mean(np.abs(residuals - residuals.mean()) < 0.6745 * s1)

    # 8. 预测值
    predicted = x0_hat[n:n + predict_n]

    return {
        'fitted': fitted,
        'predicted': predicted,
        'residuals': residuals,
        'relative_errors': relative_errors,
        'mean_error': relative_errors.mean(),
        'C': C,
        'P': P,
        'a': a,
        'b': b,
        'x0_hat': x0_hat
    }


def evaluate_model(C, P):
    """模型精度等级"""
    if C < 0.35 and P > 0.95:
        return "好"
    elif C < 0.50 and P > 0.80:
        return "合格"
    elif C < 0.65 and P > 0.70:
        return "勉强合格"
    else:
        return "不合格"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='灰色预测 GM(1,1)')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--col', type=str, required=True, help='目标列名')
    parser.add_argument('--predict', type=int, default=5, help='预测期数')
    parser.add_argument('--output', type=str, default=None, help='输出图片路径')
    parser.add_argument('--result', type=str, default=None, help='输出结果文件')

    args = parser.parse_args()

    # 读取数据
    data = pd.read_csv(args.input)
    series = data[args.col].values

    # 预测
    result = gm11(series, args.predict)

    # 输出
    print("\n=== 灰色预测 GM(1,1) 结果 ===")
    print(f"发展系数 a = {result['a']:.6f}")
    print(f"灰色作用量 b = {result['b']:.6f}")
    print(f"平均相对误差 = {result['mean_error']:.2f}%")
    print(f"后验差比值 C = {result['C']:.4f}")
    print(f"小误差概率 P = {result['P']:.4f}")
    print(f"模型精度: {evaluate_model(result['C'], result['P'])}")
    print(f"\n预测未来 {args.predict} 期:")
    for i, v in enumerate(result['predicted']):
        print(f"  第 {len(series) + i + 1} 期: {v:.4f}")

    # 绘图
    fig, ax = plt.subplots(figsize=(10, 6))
    x_orig = range(1, len(series) + 1)
    x_all = range(1, len(series) + args.predict + 1)
    ax.plot(x_orig, series, 'bo-', label='原始数据', markersize=6)
    ax.plot(x_all, result['x0_hat'][:len(series) + args.predict], 'r--', label='拟合/预测', linewidth=2)
    ax.axvline(x=len(series), color='gray', linestyle=':', alpha=0.7, label='预测起点')
    ax.set_title('灰色预测 GM(1,1)', fontsize=14, fontweight='bold')
    ax.set_xlabel('期数', fontsize=12)
    ax.set_ylabel('数值', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if args.output:
        fig.savefig(args.output, bbox_inches='tight')
        print(f"\n图表已保存: {args.output}")
    plt.close(fig)

    if args.result:
        pd.DataFrame({
            '期数': range(1, len(series) + args.predict + 1),
            '原始值': list(series) + [np.nan] * args.predict,
            '拟合/预测值': result['x0_hat'][:len(series) + args.predict]
        }).to_csv(args.result, index=False, encoding='utf-8-sig')
        print(f"结果已保存: {args.result}")
