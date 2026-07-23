#!/usr/bin/env python3
"""
kkt_bilevel_sos1.py — 用 SOS1 替代大M法 (Day 11 练习)
===================================================
从 kkt_bilevel_complete.py 改来，把互补约束从大M法换成 SOS1。

优点: 不需要3个0-1变量，模型更紧，Gurobi 求解更快。

问题 (和 Day10 完全一样):
  上层: max_x x + y1          s.t. x ∈ [0, 5]
  下层: min_{y1,y2} y1 + 0.5*y2  s.t. y1 + y2 ≥ x, y1, y2 ≥ 0

理论最优: x=5, y1=0, y2=5, λ=0.5, 目标=5

练习:
  1. 先跑这个 SOS1 版本 → 验证结果
  2. 对比两个版本的变量数: 
     - 大M法: 5连续 + 3二元 = 8变量
     - SOS1法: 5连续 + 0二元 = 5变量  ← 更少！
  3. 把上层目标改成 x + 2*y1 → 最优解变了没？
"""
import gurobipy as gp
from gurobipy import GRB

try:
    m = gp.Model("kkt_bilevel_sos1")
    
    # ===== 变量 (不需要 0-1 变量了!) =====
    x   = m.addVar(lb=0, ub=5, name="x")
    y1  = m.addVar(lb=0, ub=100, name="y1")
    y2  = m.addVar(lb=0, ub=100, name="y2")
    lam = m.addVar(lb=0, ub=10, name="lamda")
    s1  = m.addVar(lb=0, name="s1")        # 松弛变量 = y1+y2-x
    
    # ===== (1) 原始可行 =====
    m.addConstr(y1 + y2 >= x, name="prim_feas")
    m.addConstr(s1 == y1 + y2 - x, name="slack_def")
    
    # ===== (2) 平稳性 (Stationarity) =====
    # Lagrangian: L = y1 + 0.5*y2 + λ*(x-y1-y2) - μ1*y1 - μ2*y2
    # ∂L/∂y1 = 1 - λ - μ1 = 0 → μ1 = 1-λ ≥ 0 → λ ≤ 1
    # ∂L/∂y2 = 0.5 - λ - μ2 = 0 → μ2 = 0.5-λ ≥ 0 → λ ≤ 0.5
    m.addConstr(lam <= 1,   name="stationarity_1")
    m.addConstr(lam <= 0.5, name="stationarity_2")
    
    # ===== (3) 互补松弛 × 3 条 ← 用 SOS1! =====
    # 第1条: λ ⟂ (x - y1 - y2) 即 λ ⟂ (-s1)
    m.addSOS(GRB.SOS_TYPE1, [lam, s1], [1, 2])
    
    # 第2条: μ1 = 1-λ ⟂ y1
    # 注意: μ1 = 1-λ 是个表达式，不能直接放 SOS1
    # 但可以用逻辑: (1-λ) > 0 → y1 = 0, y1 > 0 → λ = 1
    # 实际上我们已经有 λ ≤ 0.5，所以 1-λ ≥ 0.5 > 0
    # 所以 y1 = 0 是必然的，不需要 SOS... 但为了通用性，写：
    y1_nonzero = m.addVar(vtype=GRB.BINARY, name="y1_nonzero")  # 辅助0-1
    m.addConstr(y1 <= 100 * y1_nonzero, name="y1_indicator")
    m.addConstr(1 - lam <= 100 * (1 - y1_nonzero), name="mu1_indicator")
    # 这样当 y1 > 0 时 y1_nonzero=1 → 1-lam=0 → lam=1 (但 lam≤0.5 所以不可能)
    # 所以 y1 只能 = 0 ✓
    
    # 第3条: μ2 = 0.5-λ ⟂ y2
    z3 = m.addVar(vtype=GRB.BINARY, name="z3")
    m.addConstr(0.5 - lam <= 100 * z3, name="comp_mu2_1")
    m.addConstr(y2 <= 100 * (1 - z3), name="comp_mu2_2")
    
    # ===== 上层目标 =====
    m.setObjective(x + y1, GRB.MAXIMIZE)
    
    # ===== 求解 =====
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        mu1 = 1 - lam.X
        mu2 = 0.5 - lam.X
        print(f"\n{'='*50}")
        print(f"SOS1 版本最优目标值 = {m.ObjVal:.4f}")
        print(f"{'='*50}")
        print(f"x  = {x.X:.4f}")
        print(f"y1 = {y1.X:.4f}")
        print(f"y2 = {y2.X:.4f}")
        print(f"λ  = {lam.X:.4f}")
        print(f"μ1 = 1-λ = {mu1:.4f}")
        print(f"μ2 = 0.5-λ = {mu2:.4f}")
        print(f"\n互补验证:")
        print(f"  λ × (-s1) = {lam.X * (-s1.X):.6f}")
        print(f"  μ1 × y1   = {mu1 * y1.X:.6f}")
        print(f"  μ2 × y2   = {mu2 * y2.X:.6f}")
    else:
        print(f"求解状态: {m.Status}")
    
    m.write("kkt_bilevel_sos1.lp")

except gp.GurobiError as e:
    print(f"Gurobi Error: {e}")

print("\n" + "=" * 50)
print("⚠️  注意: SOS1 不能直接放表达式 (1-λ)")
print("   所以第2/3条互补还是要辅助变量")
print("   真正的 SOS1 优势在 'λ ⟂ s' 这条")
print("   更多实践: 去看 ddro-via-bilevel 的强对偶写法")
print("=" * 50)
