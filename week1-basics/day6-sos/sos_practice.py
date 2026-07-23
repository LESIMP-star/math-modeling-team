#!/usr/bin/env python3
"""
sos_practice.py — SOS1 互补约束练习 (Day 6)
=========================================
用 SOS1 替代大M法实现互补条件。

问题:
  max x + y
  s.t. x * y = 0  (二者至少一为0)
       x ≤ 3, y ≤ 5
       x, y ≥ 0

两种写法对比:
  方法A: 大M法 (用 0-1 变量)
  方法B: SOS1 (更简洁)

练习:
  1. 先跑方法A → 观察结果
  2. 再跑方法B → 对比结果是否一致
  3. 把 x 上界从 3 改成 10 → 解变多少？
"""
import gurobipy as gp
from gurobipy import GRB

# ============================================================
# 方法A: 大M法
# ============================================================
print("=" * 50)
print("方法A: 大M法实现互补")
print("=" * 50)

mA = gp.Model("complementarity_bigm")

x = mA.addVar(lb=0, ub=3, name="x")
y = mA.addVar(lb=0, ub=5, name="y")
z = mA.addVar(vtype=GRB.BINARY, name="z")  # 辅助0-1
M = 100  # 大M

# 互补: x*y = 0 → 用大M表达
mA.addConstr(x <= M * z, name="comp_x")
mA.addConstr(y <= M * (1 - z), name="comp_y")

mA.setObjective(x + y, GRB.MAXIMIZE)
mA.optimize()

if mA.Status == GRB.OPTIMAL:
    print(f"  x = {x.X:.4f}, y = {y.X:.4f}")
    print(f"  检查 x*y = {x.X * y.X:.6f} (应为0)")
    print(f"  目标 = {mA.ObjVal:.4f}")

# ============================================================
# 方法B: SOS1
# ============================================================
print("\n" + "=" * 50)
print("方法B: SOS1 实现互补 (更简洁)")
print("=" * 50)

mB = gp.Model("complementarity_sos1")

x2 = mB.addVar(lb=0, ub=3, name="x")
y2 = mB.addVar(lb=0, ub=5, name="y")

# SOS1: x 和 y 不能同时非零
mB.addSOS(GRB.SOS_TYPE1, [x2, y2], [1, 2])

mB.setObjective(x2 + y2, GRB.MAXIMIZE)
mB.optimize()

if mB.Status == GRB.OPTIMAL:
    print(f"  x = {x2.X:.4f}, y = {y2.X:.4f}")
    print(f"  检查 x*y = {x2.X * y2.X:.6f} (应为0)")
    print(f"  目标 = {mB.ObjVal:.4f}")

# ============================================================
# ★ 练习: 改成 x ≤ 10, y ≤ 10
#    用 SOS1 写法再做一遍
# ============================================================
print("\n" + "=" * 50)
print("✅ 总结: SOS1 不需要大M + 0-1变量, 模型更紧")
print("=" * 50)
