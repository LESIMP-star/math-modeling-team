"""
熵权法
用于客观确定指标权重
用法: python entropy_weight.py --input data.csv --types +,+,-,+
"""
import argparse
import numpy as np
import pandas as pd


def entropy_weight(data, types):
    """
    熵权法计算权重

    参数:
        data: DataFrame, 评价指标数据
        types: list, 各指标类型（'+'正向，'-'负向）

    返回:
        dict, 各指标权重
    """
    # 1. 标准化处理
    norm_data = data.values.copy().astype(float)
    for i, t in enumerate(types):
        col = norm_data[:, i]
        if t == '+':
            # 正向指标
            min_val = col.min()
            max_val = col.max()
            norm_data[:, i] = (col - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        else:
            # 负向指标
            min_val = col.min()
            max_val = col.max()
            norm_data[:, i] = (max_val - col) / (max_val - min_val) if max_val != min_val else 0.5

    # 避免0值导致log计算问题
    norm_data = norm_data + 1e-10

    # 2. 计算比重
    col_sums = norm_data.sum(axis=0)
    P = norm_data / col_sums

    # 3. 计算信息熵
    n = len(data)
    k = 1.0 / np.log(n)
    E = -k * (P * np.log(P)).sum(axis=0)

    # 4. 计算差异系数
    D = 1 - E

    # 5. 计算权重
    W = D / D.sum()

    result = dict(zip(data.columns, W))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='熵权法')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件 (CSV)')
    parser.add_argument('--types', type=str, required=True, help='指标类型，逗号分隔（+正向，-负向）')
    parser.add_argument('--output', type=str, default=None, help='输出结果文件')

    args = parser.parse_args()

    # 读取数据
    data = pd.read_csv(args.input)
    types = [t.strip() for t in args.types.split(',')]

    # 检查
    assert len(types) == data.shape[1], f"类型数量({len(types)})与指标数量({data.shape[1]})不匹配"

    # 计算
    weights = entropy_weight(data, types)

    # 输出
    print("\n=== 熵权法计算结果 ===")
    total = 0
    for name, w in weights.items():
        print(f"  {name}: {w:.4f}")
        total += w
    print(f"  权重之和: {total:.4f}")

    if args.output:
        df = pd.DataFrame([weights])
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {args.output}")
