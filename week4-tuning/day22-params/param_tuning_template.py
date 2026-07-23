#!/usr/bin/env python3
"""
param_tuning_template.py — Gurobi 调参模板 (Day 22)
====================================================
对已有模型测试不同参数组合，找最快的。

结构:
  1. 基准测试 (默认参数)
  2. 单参数逐个测试
  3. 最佳组合测试

测试参数:
  - Presolve: 0, 1, 2
  - Cuts: 0, 1, 2, 3
  - Heuristics: 0, 0.1, 0.3, 0.5
  - MIPFocus: 0, 1, 2, 3
  - Threads: 1, 4, 8, 16

用法:
  python param_tuning_template.py [model_file]
  或修改下面 model_path 为你自己的 .lp/.mps 文件

练习:
  1. 先用 kkt_bilevel_complete.py 导出的 LP 文件测试
  2. 再拿一个更大的问题测试
  3. 记录哪个参数对求解时间影响最大
"""
import gurobipy as gp
from gurobipy import GRB
import time
import sys

# ============================================================
# 配置
# ============================================================
# 不指定文件时，自动用你 Day10 的 KKT 问题（内嵌）
USE_BUILTIN_MODEL = True  
MODEL_PATH = "D:/Python_Projects/gurobi-study/week2-bilevel/day10-kkt-bigm/kkt_bilevel_complete.lp"

# 如果文件不存在或用内置模型
if not USE_BUILTIN_MODEL:
    if len(sys.argv) > 1:
        MODEL_PATH = sys.argv[1]

# ============================================================
# 基准模型 (默认参数)
# ============================================================
def run_model(params=None, name="默认"):
    """运行模型并返回求解时间"""
    if USE_BUILTIN_MODEL:
        # 内置 KKT 问题
        m = gp.Model(f"tuning_{name}")
        x   = m.addVar(lb=0, ub=5, name="x")
        y1  = m.addVar(lb=0, ub=100, name="y1")
        y2  = m.addVar(lb=0, ub=100, name="y2")
        lam = m.addVar(lb=0, ub=10, name="lamda")
        s1  = m.addVar(lb=0, name="s1")
        z1  = m.addVar(vtype=GRB.BINARY, name="z1")
        z2  = m.addVar(vtype=GRB.BINARY, name="z2")
        z3  = m.addVar(vtype=GRB.BINARY, name="z3")
        M = 100
        m.addConstr(y1 + y2 >= x, name="prim_feas")
        m.addConstr(s1 == y1 + y2 - x, name="slack_def")
        m.addConstr(lam <= 1, name="sta_1")
        m.addConstr(lam <= 0.5, name="sta_2")
        m.addConstr(lam <= M * z1, name="comp_lam")
        m.addConstr(s1 <= M * (1 - z1), name="comp_sl")
        m.addConstr(1 - lam <= M * z2, name="comp_mu1")
        m.addConstr(y1 <= M * (1 - z2), name="comp_y1")
        m.addConstr(0.5 - lam <= M * z3, name="comp_mu2")
        m.addConstr(y2 <= M * (1 - z3), name="comp_y2")
        m.setObjective(x + y1, GRB.MAXIMIZE)
    else:
        m = gp.read(MODEL_PATH)
    
    # 设置参数
    if params:
        for k, v in params.items():
            m.setParam(k, v)
    
    # 超时保护 (防止调坏参数导致死循环)
    m.setParam("TimeLimit", 30)
    
    t0 = time.time()
    m.optimize()
    dt = time.time() - t0
    
    return dt, m.Status, m.ObjVal if m.Status == GRB.OPTIMAL else None

# ============================================================
# 测试
# ============================================================
print("=" * 60)
print("Gurobi 参数调优测试")
print("=" * 60)

# 基准
dt_base, status, obj = run_model(None, "基准")
print(f"\n基准 (默认参数): {dt_base:.3f}s, 状态={status}, 目标={obj}")
print("-" * 60)

# 单参数测试
params_to_test = [
    ("Presolve", [0, 1, 2]),
    ("Cuts", [0, 1, 2, 3]),
    ("Heuristics", [0.0, 0.1, 0.3, 0.5]),
    ("MIPFocus", [0, 1, 2, 3]),
    ("Threads", [1, 4, 8]),
]

results = [("基准", dt_base)]

for param_name, values in params_to_test:
    print(f"\n测试参数: {param_name}")
    for v in values:
        dt, status, obj = run_model({param_name: v}, f"{param_name}={v}")
        speedup = dt_base / dt if dt > 0 else float('inf')
        print(f"  {param_name}={v}: {dt:.3f}s (加速比={speedup:.2f}x)")
        results.append((f"{param_name}={v}", dt))

# 最佳组合
print("\n" + "-" * 60)
print("最佳组合测试: Presolve=2 + Cuts=2 + Heuristics=0.1")
best_params = {"Presolve": 2, "Cuts": 2, "Heuristics": 0.1, "MIPFocus": 2}
dt_best, status, obj = run_model(best_params, "最佳组合")
speedup = dt_base / dt_best if dt_best > 0 else float('inf')
print(f"  耗时: {dt_best:.3f}s (加速比={speedup:.2f}x)")

print("\n" + "=" * 60)
print("结果排序 (最快到最慢):")
results.sort(key=lambda x: x[1])
for i, (name, dt) in enumerate(results[:10]):
    speedup = dt_base / dt if dt > 0 else float('inf')
    print(f"  #{i+1}: {name} → {dt:.3f}s ({speedup:.2f}x)")
print("=" * 60)
