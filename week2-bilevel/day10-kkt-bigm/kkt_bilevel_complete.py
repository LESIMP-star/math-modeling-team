#!/usr/bin/env python3
"""
KKT单层转化 - 完整版（含所有互补约束）
=====================================
问题:
  上层: max_x x + y1          s.t. x ∈ [0, 5]
  下层: min_{y1,y2} y1 + 0.5*y2  s.t. y1 + y2 ≥ x,  y1, y2 ≥ 0

KKT条件（完整的4条）:
  1) 原始可行: y1 + y2 ≥ x, y1 ≥ 0, y2 ≥ 0
  2) 对偶可行: λ ≥ 0, μ1 ≥ 0, μ2 ≥ 0 
  3) 平稳性:  1 - λ - μ1 = 0, 0.5 - λ - μ2 = 0 → μ1 = 1-λ, μ2 = 0.5-λ
  4) 互补松弛(3条): λ·(x - y1 - y2) = 0, μ1·y1 = 0, μ2·y2 = 0

理论最优: x=5, y1=0, y2=5, λ=0.5, 目标值=5
"""
import gurobipy as gp
from gurobipy import GRB

try:
    m = gp.Model("kkt_bilevel_complete")
    
    # ===== 变量 =====
    x  = m.addVar(lb=0, ub=5, name="x")         # 上层变量
    y1 = m.addVar(lb=0, ub=100, name="y1")       # 下层变量1 (给一个上界帮助数值)
    y2 = m.addVar(lb=0, ub=100, name="y2")       # 下层变量2
    lam = m.addVar(lb=0, ub=10, name="lamda")    # 对偶变量 λ (原约束)
    
    # 大M法辅助变量 (用于3条互补松弛)
    M = 100
    z1 = m.addVar(vtype=GRB.BINARY, name="z1")   # λ × (x-y1-y2) = 0
    z2 = m.addVar(vtype=GRB.BINARY, name="z2")   # μ1 × y1 = 0
    z3 = m.addVar(vtype=GRB.BINARY, name="z3")   # μ2 × y2 = 0
    s1 = m.addVar(lb=0, name="s1")                # 松弛变量 = y1 + y2 - x
    
    # ===== (1) 原始可行 =====
    m.addConstr(y1 + y2 >= x, name="prim_feas")
    
    # ===== (2)+(3) 平稳性 =====
    # 从 Lagrangian: L = y1 + 0.5*y2 + λ*(x - y1 - y2) - μ1*y1 - μ2*y2
    # ∂L/∂y1 = 1 - λ - μ1 = 0  → μ1 = 1 - λ (μ1 ≥ 0 → λ ≤ 1)
    # ∂L/∂y2 = 0.5 - λ - μ2 = 0 → μ2 = 0.5 - λ (μ2 ≥ 0 → λ ≤ 0.5)
    m.addConstr(lam <= 1,   name="stationarity_1")   # 隐含 μ1 = 1-λ ≥ 0
    m.addConstr(lam <= 0.5, name="stationarity_2")   # 隐含 μ2 = 0.5-λ ≥ 0
    
    # ===== (4) 互补松弛 × 3 条 =====
    # 第1条: λ × (x - y1 - y2) = 0  (用松弛变量 s1 = y1 + y2 - x)
    m.addConstr(s1 == y1 + y2 - x, name="slack_def")
    m.addConstr(lam <= M * z1, name="comp_lam")       # λ > 0 ⇒ z1=1 ⇒ s1=0
    m.addConstr(s1  <= M * (1 - z1), name="comp_sl")  # s1 > 0 ⇒ z1=0 ⇒ λ=0
    
    # 第2条: μ1 × y1 = 0, 其中 μ1 = 1 - λ
    # μ1 = 1 - λ ≥ 0, μ1 × y1 = 0 ⇒ (1-λ) × y1 = 0
    m.addConstr(1 - lam <= M * z2, name="comp_mu1_1")  # 1-λ > 0 ⇒ z2=1 ⇒ y1=0
    m.addConstr(y1 <= M * (1 - z2), name="comp_mu1_2") # y1 > 0 ⇒ z2=0 ⇒ 1-λ=0
    
    # 第3条: μ2 × y2 = 0, 其中 μ2 = 0.5 - λ
    # μ2 = 0.5 - λ ≥ 0, μ2 × y2 = 0 ⇒ (0.5-λ) × y2 = 0
    m.addConstr(0.5 - lam <= M * z3, name="comp_mu2_1")  # 0.5-λ > 0 ⇒ z3=1 ⇒ y2=0
    m.addConstr(y2 <= M * (1 - z3), name="comp_mu2_2")   # y2 > 0 ⇒ z3=0 ⇒ 0.5-λ=0
    
    # ===== 上层目标 =====
    m.setObjective(x + y1, GRB.MAXIMIZE)
    
    # ===== 求解 =====
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        print(f"\n{'='*50}")
        print(f"最优目标值 = {m.ObjVal:.4f}")
        print(f"{'='*50}")
        print(f"上层变量 x    = {x.X:.4f}")
        print(f"下层变量 y1   = {y1.X:.4f}")
        print(f"下层变量 y2   = {y2.X:.4f}")
        print(f"对偶变量 λ    = {lam.X:.4f}")
        print(f"μ1 = 1-λ     = {1 - lam.X:.4f}")
        print(f"μ2 = 0.5-λ   = {0.5 - lam.X:.4f}")
        print(f"松弛 slk = y1+y2-x = {s1.X:.4f}")
        
        # 验证互补条件
        mu1 = 1 - lam.X
        mu2 = 0.5 - lam.X
        print(f"\n{'='*50}")
        print("互补条件验证 (应为0):")
        print(f"  λ × (x-y1-y2) = {lam.X * (-s1.X):.6f}")
        print(f"  μ1 × y1       = {mu1 * y1.X:.6f}")
        print(f"  μ2 × y2       = {mu2 * y2.X:.6f}")
        print(f"{'='*50}")
    else:
        print(f"求解状态: {m.Status}")
    
    m.write("kkt_bilevel_complete.lp")
    
except gp.GurobiError as e:
    print(f"Gurobi Error: {e}")
