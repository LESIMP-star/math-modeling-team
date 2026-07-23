#!/usr/bin/env python3
"""
week1-review.py — 第1周复习 (Day 7)
====================================
复习题 + 代码挑战, 验证学习成果。
在 Spyder 里打开, #%% 分块跑。
"""

# %% 挑战1: 自己写一个 MIP
print("=" * 60)
print("挑战1: 自己写一个 MIP (背包问题)")
print("=" * 60)
"""
问题: 有5件物品, 重量 [2,3,4,5,9], 价值 [3,4,5,7,10],
      背包容量 12。选哪些物品价值最大？

要求: 不百度不翻代码, 自己写!
      提示: 用 x[i] = addVar(vtype=GRB.BINARY), 
            sum(重量*x) <= 容量
"""
# TODO: 在这里自己写

# %% 挑战2: 灵敏度分析
print("=" * 60)
print("挑战2: 看懂影子价格")
print("=" * 60)
"""
用 mip1.py 的问题 (max x+y+2z, x+y+2z <= 4, x+y >= 1)
在 optimize() 后加:
  for c in m.getConstrs():
      print(f"{c.ConstrName}: Pi={c.Pi}, Slack={c.Slack}")
看哪个约束是紧的? 影子价格是多少?
"""
# TODO: 自己写

# %% 挑战3: 多目标分层
print("=" * 60)
print("挑战3: 3目标分层优化")
print("=" * 60)
"""
定义3个目标:
  f1: 最大化覆盖 (优先级最高)
  f2: 最小化成本 (次优先)
  f3: 最大化公平性 (最低优先)

用 setObjectiveN() 实现, 任意数据都可以。
"""
# TODO: 自己写

print("\n✅ 如果你3个挑战都手写出来了, 第1周过关!")
print("   如果写不出来, 回头看 day1-day6 的对应文件")
