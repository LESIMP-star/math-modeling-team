#!/usr/bin/env python3
"""
project_design.py — 综合项目设计 (Day 25-26)
=============================================
你自己定义一个双层+多目标问题，基于 KKT 框架实现。

结构:
  [1] 数学公式 → 先写在注释里
  [2] 变量定义
  [3] KKT 条件
  [4] 多目标处理 (权重法)
  [5] 参数调优
  [6] 结果分析

模板: 改 ==TODO== 标记的地方
"""

import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import numpy as np
import time

# ============================================================
# [1] 数学公式 — 先写清楚你的问题
# ============================================================
"""
问题描述: (TODO: 在这里写你的问题)
  上层: max/min F(x, y) = ________________________________
        s.t. x ∈ [___, ___]
        
  下层: min f(x, y) = _____________________________________
        s.t. g_i(x, y) ≤ 0, i=1,...,m
             y ≥ 0

变量说明:
  x: _________________________________________
  y1: ________________________________________
  y2: ________________________________________
"""

# ============================================================
# [2] 参数配置
# ============================================================
# TODO: 改这里的参数
USE_EPSILON_CONSTRAINT = False  # True=ε-约束, False=权重法
W = 0.5  # 权重法用的权重 (0~1)
N_GRID = 10  # ε-约束法的网格点数

# ============================================================
# [3] 模型构建
# ============================================================
def build_bilevel_model(weight=0.5, param_overrides=None):
    """
    构建双层→KKT→单层模型
    Args:
        weight: 下层两目标的权重 (w)
        param_overrides: dict of Gurobi 参数覆盖
    """
    m = gp.Model("my_bilevel_project")
    
    # ===== 变量 =====
    # TODO: 根据你的问题改变量
    x  = m.addVar(lb=0, ub=10, name="x")           # 上层变量
    y1 = m.addVar(lb=0, ub=100, name="y1")          # 下层变量1
    y2 = m.addVar(lb=0, ub=100, name="y2")          # 下层变量2
    
    # 对偶变量 + 互补辅助
    lam1 = m.addVar(lb=0, ub=100, name="lam1")
    lam2 = m.addVar(lb=0, ub=100, name="lam2")
    s1 = m.addVar(lb=0, name="s1")
    s2 = m.addVar(lb=0, name="s2")
    z = {}  # 0-1 变量 for 大M
    for i in range(6):
        z[i] = m.addVar(vtype=GRB.BINARY, name=f"z{i}")
    
    M = 1000
    
    # ===== 原始可行 (下层约束) =====
    # TODO: 根据你的下层约束改
    m.addConstr(y1 + y2 >= x, name="g1")            # TODO: g1(x,y) ≤ 0
    m.addConstr(2*y1 + y2 <= 15, name="g2")         # TODO: g2(x,y) ≤ 0
    
    # 松弛变量
    m.addConstr(s1 == y1 + y2 - x, name="s1_def")
    m.addConstr(s2 == 15 - 2*y1 - y2, name="s2_def")
    
    # ===== 平稳性 =====
    # TODO: 根据你下层的 Lagrangian 推导
    # ∂L/∂y1 = ... = 0
    # ∂L/∂y2 = ... = 0
    m.addConstr(lam1 <= 1, name="sta_1")
    m.addConstr(lam2 + lam1 <= 2, name="sta_2")
    
    # ===== 互补松弛 =====
    # λ_i × s_i = 0
    m.addConstr(lam1 <= M * z[0], name="comp_lam1")
    m.addConstr(s1 <= M * (1 - z[0]), name="comp_s1")
    m.addConstr(lam2 <= M * z[1], name="comp_lam2")
    m.addConstr(s2 <= M * (1 - z[1]), name="comp_s2")
    
    # μ_j × y_j = 0
    m.addConstr(1 - lam1 <= M * z[2], name="comp_mu1")
    m.addConstr(y1 <= M * (1 - z[2]), name="comp_y1")
    m.addConstr(2 - lam2 - lam1 <= M * z[3], name="comp_mu2")
    m.addConstr(y2 <= M * (1 - z[3]), name="comp_y2")
    
    # ===== 目标 (上层) =====
    # TODO: 改你的上层目标
    upper_obj = x + y1
    m.setObjective(upper_obj, GRB.MAXIMIZE)
    
    # ===== 参数覆盖 =====
    if param_overrides:
        for k, v in param_overrides.items():
            m.setParam(k, v)
    
    return m, (x, y1, y2, lam1, lam2)

# ============================================================
# [4] 求解 + 结果
# ============================================================
m, (x, y1, y2, lam1, lam2) = build_bilevel_model(W)
m.setParam("OutputFlag", 0)
m.optimize()

if m.Status == GRB.OPTIMAL:
    print(f"\n{'='*50}")
    print(f"✅ 求解成功!")
    print(f"{'='*50}")
    print(f"上层目标 = {m.ObjVal:.4f}")
    print(f"  x  = {x.X:.4f}")
    print(f"下層变量:")
    print(f"  y1 = {y1.X:.4f}")
    print(f"  y2 = {y2.X:.4f}")
    print(f"对偶变量:")
    print(f"  λ1 = {lam1.X:.4f}")
    print(f"  λ2 = {lam2.X:.4f}")
else:
    print(f"❌ 求解失败, 状态码={m.Status}")

print(f"\n💡 提示: 现在可以修改 ==TODO== 标记的地方")
print(f"   用你自己的问题替换模板内容")
