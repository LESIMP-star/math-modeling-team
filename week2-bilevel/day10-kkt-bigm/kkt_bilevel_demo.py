#!/usr/bin/env python3
"""
KKT单层转化最小示例
下层: min y1 + 0.5*y2   s.t. y1 + y2 >= x,  y1 >= 0, y2 >= 0
上层: max x + y1          s.t. x in [0, 5]
    
理论上: 下层最优 y1* = x, y2* = 0 (因为y1成本低)
        代入上层: max x + x = 2x, x=5时最优值=10
"""
import gurobipy as gp
from gurobipy import GRB

try:
    m = gp.Model("kkt_bilevel_demo")
    
    # ===== 变量 =====
    x  = m.addVar(lb=0, ub=5, name="x")        # 上层变量
    y1 = m.addVar(lb=0, name="y1")              # 下层变量1
    y2 = m.addVar(lb=0, name="y2")              # 下层变量2
    lam1 = m.addVar(lb=0, name="lam1")          # 对偶变量(下层约束)
    
    # 大M
    M = 1000
    z1 = m.addVar(vtype=GRB.BINARY, name="z1") # 互补松弛辅助0-1变量
    s1 = m.addVar(lb=0, name="s1")              # 松弛变量
    
    # ===== 原始可行 (下层约束) =====
    m.addConstr(y1 + y2 >= x, name="prim_feas")
    
    # ===== 对偶可行 =====
    # 下层Lagrangian: L = y1 + 0.5*y2 + lam1*(x - y1 - y2)
    # dL/dy1 = 1 - lam1 >= 0  =>  lam1 <= 1
    # dL/dy2 = 0.5 - lam1 >= 0 => lam1 <= 0.5
    m.addConstr(lam1 <= 1, name="dual_feas_1")
    m.addConstr(lam1 <= 0.5, name="dual_feas_2")
    
    # ===== 互补松弛 (大M法) =====
    # s1 = y1 + y2 - x (松弛变量, >= 0)
    m.addConstr(s1 == y1 + y2 - x, name="slack_def")
    # lam1 * s1 = 0  =>  lam1 <= M*z1, s1 <= M*(1-z1)
    m.addConstr(lam1 <= M * z1, name="comp_1")
    m.addConstr(s1  <= M * (1 - z1), name="comp_2")
    
    # ===== 上层目标 =====
    m.setObjective(x + y1, GRB.MAXIMIZE)
    
    # ===== 求解 =====
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        print(f"\n最优值 = {m.ObjVal:.4f}")
        print(f"x  = {x.X:.4f}")
        print(f"y1 = {y1.X:.4f}")
        print(f"y2 = {y2.X:.4f}")
        print(f"lam1 = {lam1.X:.4f}")
        print(f"s1  = {s1.X:.4f}")
        print(f"互补检查: lam1*s1 = {lam1.X * s1.X:.6f} (应为0)")
    else:
        print(f"求解状态: {m.Status}")
    
    m.write("kkt_bilevel_demo.lp")
    
except gp.GurobiError as e:
    print(f"Gurobi Error: {e}")
