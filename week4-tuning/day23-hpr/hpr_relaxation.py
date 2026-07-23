#!/usr/bin/env python3
"""
hpr_relaxation.py — High-Point Relaxation (Day 23)
===================================================
HPR = 去掉下层 KKT 条件，只保留上层 + 下层原始可行。

作用: 
  - 给出"理论最优上界"（双层问题的最优值不可能超过 HPR）
  - gap = (HPR - KKT解) / HPR 越小 → KKT 模型越紧越好解
  
问题 (和之前一样):
  上层: max x + y1          s.t. x ∈ [0, 5]
  下层: min y1 + 0.5*y2    s.t. y1 + y2 ≥ x, y1, y2 ≥ 0

理论: 
  KKT 解: x=5, y1=0, y2=5, obj=5
  HPR:    x=5, y1=5, y2=0, obj=10 (无下层约束)

练习:
  1. 先跑通对比 HPR vs KKT
  2. ★ 把上层目标改成 x + 2*y1 → HPR 涨多少？
  3. ★ 添加下层绑定约束 y1 ≤ 3 → HPR gap 变小了没？
"""
import gurobipy as gp
from gurobipy import GRB

print("=" * 60)
print("High-Point Relaxation (HPR) vs KKT 对比")
print("=" * 60)

# ============================================================
# 模型1: HPR (去掉KKT)
# ============================================================
m_hpr = gp.Model("HPR")
x1 = m_hpr.addVar(lb=0, ub=5, name="x")
y1 = m_hpr.addVar(lb=0, ub=100, name="y1")
y2 = m_hpr.addVar(lb=0, ub=100, name="y2")

m_hpr.addConstr(y1 + y2 >= x1, name="prim_feas")  # 只保留原始可行
# ★ 练习: 加 m_hpr.addConstr(y1 <= 3, name="upper_bound")
m_hpr.setObjective(x1 + y1, GRB.MAXIMIZE)

m_hpr.optimize()
hpr_obj = m_hpr.ObjVal
print(f"\nHPR (去KKT, 只有原始可行):")
print(f"  目标 = {hpr_obj:.4f}")
print(f"  x = {x1.X:.4f}, y1 = {y1.X:.4f}, y2 = {y2.X:.4f}")

# ============================================================
# 模型2: KKT 完整 (从 kkt_bilevel_complete.py)
# ============================================================
m_kkt = gp.Model("KKT")

x  = m_kkt.addVar(lb=0, ub=5, name="x")
ya = m_kkt.addVar(lb=0, ub=100, name="y1")
yb = m_kkt.addVar(lb=0, ub=100, name="y2")
lam = m_kkt.addVar(lb=0, ub=10, name="lamda")
s1  = m_kkt.addVar(lb=0, name="s1")
z1  = m_kkt.addVar(vtype=GRB.BINARY, name="z1")
z2  = m_kkt.addVar(vtype=GRB.BINARY, name="z2")
z3  = m_kkt.addVar(vtype=GRB.BINARY, name="z3")
M = 100

m_kkt.addConstr(ya + yb >= x, name="prim_feas")
m_kkt.addConstr(s1 == ya + yb - x, name="slack_def")
m_kkt.addConstr(lam <= 1,   name="sta_1")
m_kkt.addConstr(lam <= 0.5, name="sta_2")
m_kkt.addConstr(lam <= M * z1, name="comp_lam")
m_kkt.addConstr(s1  <= M * (1 - z1), name="comp_sl")
m_kkt.addConstr(1 - lam <= M * z2, name="comp_mu1")
m_kkt.addConstr(ya <= M * (1 - z2), name="comp_y1")
m_kkt.addConstr(0.5 - lam <= M * z3, name="comp_mu2")
m_kkt.addConstr(yb <= M * (1 - z3), name="comp_y2")
# ★ m_kkt.addConstr(ya <= 3, name="upper_bound")
m_kkt.setObjective(x + ya, GRB.MAXIMIZE)

m_kkt.optimize()
kkt_obj = m_kkt.ObjVal

print(f"\nKKT (完整单层转化):")
print(f"  目标 = {kkt_obj:.4f}")
print(f"  x = {x.X:.4f}, y1 = {ya.X:.4f}, y2 = {yb.X:.4f}")
print(f"  λ = {lam.X:.4f}")

# ============================================================
# 对比
# ============================================================
print("\n" + "=" * 60)
print("对比分析:")
print(f"  HPR 上界: {hpr_obj:.4f}")
print(f"  KKT 最优: {kkt_obj:.4f}")
if hpr_obj != 0:
    gap = (hpr_obj - kkt_obj) / hpr_obj * 100
    print(f"  Gap: {gap:.2f}%")
    if gap < 5:
        print("  ✅ KKT模型很紧！gap < 5%")
    elif gap < 20:
        print("  ⚠️  gap 适中，可以尝试加更多约束收紧")
    else:
        print("  ❌ gap 很大，KKT 模型太松了")
print("=" * 60)
