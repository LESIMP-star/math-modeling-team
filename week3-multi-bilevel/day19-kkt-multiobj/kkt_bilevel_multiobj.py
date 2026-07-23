#!/usr/bin/env python3
"""
kkt_bilevel_multiobj.py — 多目标下层的双层优化 (Day 19)
======================================================
问题:
  上层: max_x x + y1          s.t. x ∈ [0, 5]
  下层: min_{y1,y2} {w*(y1+0.5*y2) + (1-w)*(2*y1+y2)}
        s.t. y1 + y2 ≥ x, y1, y2 ≥ 0

  下层两个目标: f_low1 = y1+0.5*y2, f_low2 = 2*y1+y2
  权重 w 从 0.1 到 0.9 变化 → 得到 9 个解
  每个解对应上层的一个目标值

练习:
  1. 跑通，看 w 变化时上/下层目标怎么变
  2. 改成 ε-约束法: 固定 f_low2 ≤ ε, 最小化 f_low1
  3. 画图: w 值 × 上层目标值 的关系
"""
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 权重扫描
# ============================================================
results = []

for w in np.arange(0.1, 1.0, 0.1):  # 0.1, 0.2, ..., 0.9
    m = gp.Model(f"multiobj_bilevel_w{w:.1f}")
    
    # 变量
    x   = m.addVar(lb=0, ub=5, name="x")
    y1  = m.addVar(lb=0, ub=100, name="y1")
    y2  = m.addVar(lb=0, ub=100, name="y2")
    lam = m.addVar(lb=0, ub=10, name="lamda")
    s1  = m.addVar(lb=0, name="s1")
    z1  = m.addVar(vtype=GRB.BINARY, name="z1")
    z2  = m.addVar(vtype=GRB.BINARY, name="z2")
    z3  = m.addVar(vtype=GRB.BINARY, name="z3")
    
    M = 100
    
    # KKT 条件 (和之前一样)
    m.addConstr(y1 + y2 >= x, name="prim_feas")
    m.addConstr(s1 == y1 + y2 - x, name="slack_def")
    
    # 平稳性 — 注意下层目标变了一阶导数变了！
    # 下层: w*(y1+0.5*y2) + (1-w)*(2*y1+y2)
    #      = (w + 2-2w)*y1 + (0.5w + 1-w)*y2
    #      = (2-w)*y1 + (1-0.5w)*y2
    # ∂L/∂y1 = 2-w - λ - μ1 = 0 → λ ≤ 2-w
    # ∂L/∂y2 = 1-0.5w - λ - μ2 = 0 → λ ≤ 1-0.5w
    m.addConstr(lam <= 2 - w, name="sta_1")
    m.addConstr(lam <= 1 - 0.5*w, name="sta_2")
    
    # 互补松弛 × 3
    m.addConstr(lam <= M * z1, name="comp_lam")
    m.addConstr(s1 <= M * (1 - z1), name="comp_sl")
    m.addConstr(2 - w - lam <= M * z2, name="comp_mu1")
    m.addConstr(y1 <= M * (1 - z2), name="comp_y1")
    m.addConstr(1 - 0.5*w - lam <= M * z3, name="comp_mu2")
    m.addConstr(y2 <= M * (1 - z3), name="comp_y2")
    
    # 上层目标
    m.setObjective(x + y1, GRB.MAXIMIZE)
    
    m.setParam("OutputFlag", 0)
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        f_low1 = y1.X + 0.5*y2.X
        f_low2 = 2*y1.X + y2.X
        results.append((w, x.X, y1.X, y2.X, m.ObjVal, f_low1, f_low2))
        print(f"  w={w:.1f}: 上层={m.ObjVal:.3f}, "
              f"y1={y1.X:.3f}, y2={y2.X:.3f}, "
              f"下层1={f_low1:.3f}, 下层2={f_low2:.3f}")
    else:
        print(f"  w={w:.1f}: 无解")

# ============================================================
# 绘图
# ============================================================
print("\n" + "=" * 50)
results = np.array(results)
print(f"✅ 扫描完成, 共 {len(results)} 个有效解")

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(results[:,0], results[:,4], 'ro-', linewidth=2)
plt.xlabel("下层权重 w")
plt.ylabel("上层目标值 (x + y1)")
plt.title("权重 w 对上层目标的影响")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(results[:,5], results[:,6], 'bs-', linewidth=2)
plt.xlabel("下层目标1 (f_low1)")
plt.ylabel("下层目标2 (f_low2)")
plt.title("下层两目标的帕累托关系")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("multiobj_bilevel_result.png", dpi=150)
print("✅ 图已保存: multiobj_bilevel_result.png")
plt.show()
