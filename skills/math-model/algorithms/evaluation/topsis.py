"""
TOPSIS 综合评价算法
适用于多指标决策、方案排序
用法: python topsis.py --input data.csv --weights 0.3,0.3,0.2,0.2 --types +,+,-,+
"""
import argparse
import numpy as np
import pandas as pd


def topsis(data, weights, types):
    """
    TOPSIS 综合评价

    参数:
        data: DataFrame, 评价指标数据（每行一个方案，每列一个指标）
        weights: list, 各指标权重（和为1）
        types: list, 各指标类型（'+'为正向指标，'-'为负向指标）

    返回:
        DataFrame, 包含综合得分和排名
    """
    # 1. 标准化处理（向量归一化）
    norm_data = data.values / np.sqrt((data.values ** 2).sum(axis=0))

    # 2. 加权标准化
    weighted_data = norm_data * weights

    # 3. 确定正理想解和负理想解
    ideal_best = []
    ideal_worst = []
    for i, t in enumerate(types):
        if t == '+':
            ideal_best.append(weighted_data[:, i].max())
            ideal_worst.append(weighted_data[:, i].min())
        else:
            ideal_best.append(weighted_data[:, i].min())
            ideal_worst.append(weighted_data[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # 4. 计算距离
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # 5. 计算综合得分
    scores = dist_worst / (dist_best + dist_worst)

    # 6. 排名
    result = data.copy()
    result['综合得分'] = scores
    result['排名'] = scores.argsort()[::-1].argsort() + 1
    result = result.sort_values('排名')

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TOPSIS 综合评价算法')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--weights', type=str, required=True, help='权重，逗号分隔（如 0.3,0.3,0.2,0.2）')
    parser.add_argument('--types', type=str, required=True, help='指标类型，逗号分隔（+正向，-负向，如 +,+,-,+）')
    parser.add_argument('--output', type=str, default=None, help='输出结果文件 (CSV)')

    args = parser.parse_args()

    # 读取数据
    data = pd.read_csv(args.input)
    weights = np.array([float(w) for w in args.weights.split(',')])
    types = [t.strip() for t in args.types.split(',')]

    # 检查
    assert len(weights) == data.shape[1], f"权重数量({len(weights)})与指标数量({data.shape[1]})不匹配"
    assert len(types) == data.shape[1], f"类型数量({len(types)})与指标数量({data.shape[1]})不匹配"
    assert abs(sum(weights) - 1.0) < 0.01, f"权重之和应为1，当前为{sum(weights)}"

    # 计算
    result = topsis(data, weights, types)

    # 输出
    print("\n=== TOPSIS 评价结果 ===")
    print(result.to_string())

    if args.output:
        result.to_csv(args.output, index=True, encoding='utf-8-sig')
        print(f"\n结果已保存: {args.output}")
