#!/usr/bin/env python3
"""
epsilon_constraint.py — ε-约束法实现帕累托前沿 (Day 17)
======================================================
问题:
  min f1 = x1 + x2
  min f2 = -x1 + 2*x2
  s.t. x1 + x2 ≤ 10
       x1 ≥ 0, x2 ≥ 0

方法: ε-约束法
  1. 先求 f1_min (单独 min f1)
  2. 再求 f2_min, f2_max (单独 min/max f2)
  3. 在 [f2_min, f2_max] 内均匀取 N 个 ε 值
  4. 每个 ε: min f1 s.t. f2 ≤ ε → 记录 (f1, f2)

练习:
  1. 先跑通，看帕累托前沿图
  2. 把 N 从 10 改成 20 → 前沿更密
  3. ★ 自己改约束: 加一个 x1 ≤ 3 → 看前沿形状变化
"""
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 数据
# ============================================================
N = 10  # 网格点数

# ============================================================
# Step 1: 求 f2 的取值范围
# ============================================================
m1 = gp.Model("get_f2_range")

x1 = m1.addVar(lb=0, name="x1")
x2 = m1.addVar(lb=0, name="x2")
m1.addConstr(x1 + x2 <= 10, name="constraint")
# ★ 加约束练习: m1.addConstr(x1 <= 3)

# min f2
m1.setObjective(-x1 + 2*x2, GRB.MINIMIZE)
m1.optimize()
f2_min = m1.ObjVal
print(f"f2 最小值 = {f2_min:.4f}")

# max f2 (GRB.MAXIMIZE)
m1.setObjective(-x1 + 2*x2, GRB.MAXIMIZE)
m1.optimize()
f2_max = m1.ObjVal
print(f"f2 最大值 = {f2_max:.4f}")

# ============================================================
# Step 2: ε-约束法循环
# ============================================================
f1_vals = []
f2_vals = []

eps_grid = np.linspace(f2_min, f2_max, N)

for eps in eps_grid:
    m = gp.Model(f"epsilon_{eps:.2f}")
    
    x1v = m.addVar(lb=0, name="x1")
    x2v = m.addVar(lb=0, name="x2")
    
    m.addConstr(x1v + x2v <= 10, name="constraint")
    # m.addConstr(x1v <= 3)  # ← 和上面同步开/关
    
    # ε-约束: f2 ≤ ε
    m.addConstr(-x1v + 2*x2v <= eps, name="epsilon_constraint")
    
    # min f1
    m.setObjective(x1v + x2v, GRB.MINIMIZE)
    m.setParam("OutputFlag", 0)  # 静默模式
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        f1_vals.append(m.ObjVal)
        f2_vals.append(eps)
    else:
        print(f"  ε={eps:.2f}: 不可行")

# ============================================================
# Step 3: 绘图
# ============================================================
plt.figure(figsize=(8, 6))
plt.plot(f1_vals, f2_vals, 'bo-', linewidth=2, markersize=6)
plt.xlabel("f1 = x1 + x2 (最小化)")
plt.ylabel("f2 = -x1 + 2*x2 (ε约束)")
plt.title("ε-约束法: 帕累托前沿")
plt.grid(True, alpha=0.3)

# 标注每个点
for i, (f1, f2) in enumerate(zip(f1_vals, f2_vals)):
    plt.annotate(f"ε={f2:.1f}", (f1, f2), 
                textcoords="offset points", xytext=(5, 5),
                fontsize=8)

plt.tight_layout()
plt.savefig("pareto_frontier.png", dpi=150)
print(f"\n✅ 帕累托前沿图已保存: pareto_frontier.png")
plt.show()
