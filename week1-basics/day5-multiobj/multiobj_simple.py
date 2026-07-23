#!/usr/bin/env python3
"""
multiobj_simple.py — 多目标分层法简化版 (Day 5 练习)
=================================================
问题: 从20个元素中选出≤12个，最大化4个集合的覆盖，
      但4个集合优先级不同。

修改练习 (在 Spyder 用 #%% 分块跑):
  1. 把 SetObjPriority 改成 [1,1,1,1] → 观察解的变化
  2. 把 Budget 从 12 改成 8 → 覆盖变差多少？
  3. 只保留前2个目标 → 删掉 Subsets[2] 和 Subsets[3]
  
关键 API:
  m.setObjectiveN(obj, index=i, priority=p, weight=w, name=...)
  — index=0 是最高优先级 (priority 值最大)
"""
import gurobipy as gp
from gurobipy import GRB

try:
    # ============================================================
    # 数据
    # ============================================================
    Groundset = range(20)         # 20个候选元素
    Budget = 12                   # 最多选12个
    Set = [                       # 4个集合的覆盖关系
        [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],  # Set0: 前10个
        [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],  # Set1: 位置5-9,15-19
        [0,0,0,1,1,0,1,1,0,0,0,0,0,1,1,0,1,1,0,0],  # Set2
        [0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0],  # Set3
    ]
    
    # ★ 改这里：调整优先级和权重
    SetObjPriority = [3, 2, 2, 1]  # Set0最优先, Set3最次
    SetObjWeight   = [1.0, 0.25, 1.25, 1.0]  # 同级内的权重
    
    # ============================================================
    # 建模
    # ============================================================
    m = gp.Model("multiobj_demo")
    
    # 变量: x[e] = 1 选元素e
    x = m.addVars(Groundset, vtype=GRB.BINARY, name="El")
    
    # 约束: 最多选 Budget 个
    m.addConstr(x.sum() <= Budget, name="Budget")
    
    m.ModelSense = GRB.MAXIMIZE
    
    # 设置多目标
    for i in range(4):
        obj = gp.quicksum(Set[i][k] * x[k] for k in Groundset)
        m.setObjectiveN(obj, index=i, 
                       priority=SetObjPriority[i], 
                       weight=SetObjWeight[i],
                       name=f"Set{i}")
    
    # ============================================================
    # 求解 + 输出
    # ============================================================
    m.optimize()
    
    if m.Status == GRB.OPTIMAL:
        selected = [e for e in Groundset if x[e].X > 0.9]
        print(f"\n选中元素 ({len(selected)}个): {selected}")
        print(f"各目标值:")
        for i in range(4):
            val = sum(Set[i][k] * x[k].X for k in Groundset)
            print(f"  Set{i}: {val} (priority={SetObjPriority[i]})")
    
    m.write("multiobj_demo.lp")
    print("\n✅ 已保存 multiobj_demo.lp — 用记事本打开看数学表达")

except gp.GurobiError as e:
    print(f"Gurobi Error: {e}")
