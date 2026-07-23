# 🗺️ Gurobi 进阶学习计划（日级细化版）

> 环境：Spyder + `D:/Anaconda3/python.exe`  
> 示例：`E:/Ai_configs/win64/examples/python/`  
> Gurobi 13.0.0，License 2841306（~2027-07）  
> 用户：NCU 金融数学大一，弱代码强数学，导师彭振华（WHU，双层+DC方向）  
> 主编辑器：Spyder（`#%%` 分块跑）

---

## 第 1 周：Gurobi 基础 → 多目标 API

> 目标：跑通官方 5 个示例，理解 `setObjectiveN()` 多目标语法

### Day 1 — 第一个 MIP（0-1 规划入门）

**文件**: `mip1.py`
```
1 | Spyder → File → Open → E:/Ai_configs/win64/examples/python/mip1.py
2 | 整段跑通 → 输出 "Obj: 3"
3 | 思考：x=1, y=0, z=1 → 1+0+2*1=3 是怎么来的？
4 | 动手改1：把 x 的 vtype 从 BINARY 改成 CONTINUOUS → 目标值变吗？
5 | 动手改2：把约束 x+y >= 1 改成 x+y >= 2 → 报错？说明什么？
6 | 加 m.write("mip1.lp") → 用记事本打开 mip1.lp 看数学表达
```
✅ **验证**：能解释 "Obj: 3" 怎么算出来的

### Day 2 — 线性规划 + 影子价格

**文件**: `lp.py`（连续变量 LP）
```
1 | 打开 lp.py，跑通
2 | 在 optimize() 后加：
   for c in m.getConstrs():
       print(f"{c.ConstrName}: Pi={c.Pi}, Slack={c.Slack}")
3 | 看Pi（影子价格）：哪个约束紧（Slack=0），Pi就非零
4 | 观察：把约束右端项+1，目标值变化量 ≈ Pi 值
```
✅ **验证**：能说清"Pi=0 代表该约束是松弛的，对当前解无影响"

### Day 3 — 营养配餐（完整建模流程）

**文件**: `diet.py`
```
1 | 跑通，看最优值的餐食组合
2 | 改数据1：caloriesMin 从 2000 → 2500，成本涨多少？
3 | 改数据2：牛肉价格 ×3，看食谱怎么重新选
4 | 写 diet.lp 打开 — 这是最清晰的"数学公式 → 代码"对照
5 | 扩展挑战：加第8种食物（数据复制一份+改 range）
```
✅ **验证**：能独立给 diet 加一种新食物

### Day 4 — 设施选址（0-1 规划经典）

**文件**: `facility.py`
```
1 | 理解两个变量集：open[i]（建厂）和 assign[i,j]（分配客户）
2 | 跑通后改 FixedCost ×3 → 工厂数量变少了吗？
3 | 画示意图："开了几个厂？每个厂服务谁？"
4 | 把 addConstrs 抄到纸上对应数学公式
```
✅ **验证**：画出最优选址方案图（厂位置+客户分配）

### Day 5 — 多目标分层法 🔑

**文件**: `multiobj.py`
```
1 | 跑通，看输出了几个解（PoolSolutions=100 搜集了N个解）
2 | 关键 API：setObjectiveN(obj, index=i, priority=p, weight=w)
3 | 改 priority: [3,2,2,1] → [1,1,1,1]（平级）看结果变化
4 | 改 weight: 全部 = 1，看权重法效果
5 | 保存一个 2 目标简化版：删掉两个 Subset，只留 priority=3 和 priority=1
```
✅ **验证**：能写一个 3 目标的分层优化问题（自己的数据）

### Day 6 — SOS1 约束（KKT 互补松弛的关键）

**文件**: `sos.py`
```
1 | 跑通，理解 SOS_TYPE1 → 一组变量中最多一个非零
2 | 新建文件，写问题：
   max x + y
   s.t. x*y = 0 (x,y ≥ 0)  →  用 SOS1 替代
   x ≤ 3, y ≤ 5
3 | 对比：m.addConstr(x*y <= 0) 和 SOS1 写法的区别
```
✅ **验证**：能用 SOS1 写出互补约束 `x⊥y`

### Day 7 — 周复习 + 跑通 Optimization 101

**任务**:
```
1 | 下 gurobi-modeling-examples 的 Optimization 101 Notebook
   → https://github.com/lx249/gurobi-modeling-examples
2 | 找到 setObjectiveN() 的多目标完整例子
3 | 整理一份你自己版本的"单目标→多目标"迁移笔记
```
✅ **里程碑**：能写出 3 目标分层/加权优化问题

---

## 第 2 周：KKT / 强对偶单层转化

> 目标：理解 KKT 条件怎么写成 Gurobi 约束，跑通自己的双层最小例子

### Day 8 — 双层规划数学标准形式

**纸上数学，不写代码**
```
1 | 抄标准形式：
   min_{x∈X, y∈S(x)} F(x,y)
   S(x) = argmin_{y} {f(x,y) : g(x,y) ≤ 0}
2 | 标出：上层变量 x，下层变量 y，下层约束 g，上层约束 G
3 | 翻出导师给的论文 → 把变量一一对号入座
```
✅ **验证**：随便找一篇双层优化论文，能指出 x/y/F/f/g 分别是什么

### Day 9 — KKT 条件数学回顾

**纸上数学**
```
1 | 写下：下层 min c^T y  s.t. Ay ≤ b - Bx
2 | Lagrangian: L = c^T y + λ^T(Ay - b + Bx) - μ^T y
3 | KKT 三条：
   ① 原始可行: Ay ≤ b - Bx, y ≥ 0
   ② 对偶可行: A^T λ + μ = c, λ ≥ 0, μ ≥ 0
   ③ 互补松弛: λ_i·(Ay - b + Bx)_i = 0, μ_i·y_i = 0
4 | 把 ③ 写成 "二者之一为 0" 的形式
```
✅ **验证**：能写出 3 个变量的下层问题的全部 KKT 条件

### Day 10 — 大M法实现 KKT 转化（本地有文件！）

**文件**: `E:/Ai_configs/win64/examples/python/kkt_bilevel_complete.py`（我刚才写好的）

```
1 | 在 Spyder 打开 → `#%%` 切分 → 逐段跑通
2 | 理解每条互补约束都有 2 条辅助约束 + 1 个 0-1 变量
3 | 动手改1：把 M = 100 改成 M = 10，还能跑对吗？
4 | 动手改2：把上层目标从 x+y1 改成 x + 2*y1，最优解变多少？
5 | 动手改3：把 x 上界从 5 改成 10，结果变多少？
```
✅ **验证**：把 M 改到刚好可行（比如 M=6），观察结果变化

### Day 11 — SOS1 替代大M法（更紧的模型）

**文件**: `kkt_bilevel_sos1.py`（从 Day 10 复制改）
```
1 | 复制 kkt_bilevel_complete.py → 新文件
2 | 把互补约束的 大M+z 写法 替换为 SOS1：
   m.addSOS(GRB.SOS_TYPE1, [lam, s1], [1, 2])
   m.addSOS(GRB.SOS_TYPE1, [1-lam, y1], [1, 2])  ← 注意 μ1=1-λ
   m.addSOS(GRB.SOS_TYPE1, [0.5-lam, y2], [1, 2])
3 | 去掉 z1/z2/z3 三个0-1变量
4 | 对比大M法和SOS1法的求解时间（gurobi log 里看）
```
✅ **验证**：SOS1 版本的结果与大M法一致

### Day 12 — 强对偶转化（替代 KKT，更快）

**概念理解日**
```
KKT 问题的根源：
- 互补约束 λ·s = 0 是非凸的
- 大M法让模型变松（relaxation gap 大）
- 节点数暴涨

强对偶路线的核心思想：
- 下层是 LP → 强对偶成立 c^T y = (b-Bx)^T λ
- 用这个等式替代互补松弛条件
- 模型是线性的，没有 0-1 变量，纯 LP！

文件：下 ddro-via-bilevel 的代码，找 strong_duality 关键词
```
✅ **验证**：能写出强对偶等式 $c^T y = (b-Bx)^T \lambda$

### Day 13 — 下 ddro-via-bilevel 并跑通

```
1 | mkdir -p D:/Python_Projects/bilevel_practice
2 | cd D:/Python_Projects/bilevel_practice
3 | git clone https://github.com/simstevens/ddro-via-bilevel.git
4 | 找 shortest_path 文件夹 → 看 model.py
5 | 能跑通就算成功，不要求看完
```
✅ **验证**：ddro-via-bilevel 能在本地跑出结果

### Day 14 — 周复习

```
1 | 对比 KKT(大M法) vs KKT(SOS1) vs 强对偶 的优劣势
2 | 填下表：

| 方法 | 变量类型 | 0-1变量数 | 线性/非线性 | 求解速度 |
|------|---------|----------|------------|---------|
| KKT+大M | MIP | 多 | 线性 | 慢 |
| KKT+SOS1 | MIP | 少 | 线性+SOS | 中 |
| 强对偶 | LP | 0 | 线性 | 最快 |

3 | 结论：下层是 LP 时，永远优先用强对偶转化
```
✅ **里程碑**：吃透双层→单层转化的三种方法

---

## 第 3 周：多目标 × 双层（ε-约束法 + 帕累托前沿）

> 目标：把多目标嵌进双层框架，理解 ε-约束法和 AUGMECON

### Day 15 — 多目标双层的数学形式

```
1 | 写下"下层是多目标"的双层问题：
   Upper: min F(x, y)
   Lower: min {f1(x,y), f2(x,y)}  s.t. y ∈ Y(x)
2 | 两种处理方式：
   A) 下层用权重法合为一个目标 → KKT转化
   B) 下层用ε-约束法 → 把其中一个目标变成约束
3 | 标出：你导师论文里用的是哪种？
```
✅ **验证**：论文里看明白导师是怎么处理多目标下层的

### Day 16 — ε-约束法原理（纯数学）

```
1 | 对于多目标 min {f1, f2}:
   min f1  s.t. f2 ≤ ε
2 | 循环改变 ε: ε = ε_min + k·Δε, k=0,1,...,K
3 | 每次跑一个单目标问题 → 得到一组帕累托解
4 | 优点：能找到非凸前沿上的点（权重法不能）
```
✅ **验证**：手算一个 2 目标问题，用 ε-约束法画出 5 个帕累托点

### Day 17 — Gurobi 实现 ε-约束法

**文件**: 新建 `epsilon_constraint_demo.py`
```
1 | 定义 2 目标问题: min f1 = x1 + x2,  min f2 = -x1 + 2*x2
   s.t. x1 + x2 ≤ 10, x1 ≥ 0, x2 ≥ 0
2 | 先做单目标: min f1 → 记录 f2 的值 → f2_min
3 | 再做: min f2 → 记录 f1 的值 → f2_max
4 | 在 [f2_min, f2_max] 内划分 10 个 ε
5 | 循环: for eps in f2_grid: 
       m.addConstr(f2 <= eps) → m.optimize() → 记录(f1, f2)
6 | 绘图: plt.scatter(f1_list, f2_list)
```
✅ **验证**：画出的帕累托前沿呈递减趋势

### Day 18 — pyaugmecon 入门

```
1 | pip install pyaugmecon (在 D:/Anaconda3 下)
2 | 阅读文档: https://github.com/wouterbles/pyaugmecon
3 | 跑通其 examples 里的最短代码
4 | 对比：自己手写 ε-约束法 vs pyaugmecon 的代码量
```
✅ **验证**：pyaugmecon 能跑出和你手写一致的帕累托前沿

### Day 19 — 多目标下层的 KKT 转化（核心难点）

```
1 | 下层是 min_{y∈Y} {f1(y), f2(y)} 
2 | 权重法: min θ·f1 + (1-θ)·f2 → 变单目标 → 标准 KKT
3 | ε-约束法: min f1, s.t. f2 ≤ ε → 单目标 → KKT 不变
4 | 关键理解：多目标并不改变 KKT 结构，只是下层目标变了
```
✅ **验证**：能写出"下层是加权和"的双层→单层 KKT 约束

### Day 20 — 完整案例：双层+多目标 Gurobi 实现

```
1 | 把之前 kkt_bilevel_complete.py 的下层目标改成多目标
   - 权重法: f_lower = w*f1 + (1-w)*f2
   - 循环 w = 0.1, 0.3, 0.5, 0.7, 0.9
2 | 每次记录上层目标值
3 | 画图：帕累托前沿（上层目标 vs 下层两目标的权衡）
```
✅ **验证**：得到 5 组不同权重对应的最优解

### Day 21 — 周复习

```
1 | 整理：多目标双层优化的 3 条路径
   a) 权重法(下层加权) + KKT → 最易实现
   b) ε-约束法 + KKT → 更全面的前沿
   c) 强对偶(下层是LP) → 最快但下层必须是LP
2 | 评估：你导师论文的路线上哪种最适合？
```
✅ **里程碑**：能写"下层多目标+KKT转化"的完整代码

---

## 第 4 周：参数调优 + 切割平面 + 综合项目

> 目标：学习 Gurobi 调参技巧，跑通完整的大规模双层案例

### Day 22 — Gurobi 调参基础

**本地测试文件**
```
1 | 回到 kkt_bilevel_complete.py → 先跑一次记录求解时间
2 | 加参数逐个试：
   m.setParam("Presolve", 2)      # 更强预求解
   m.setParam("Cuts", 2)          # 更强切割平面
   m.setParam("Heuristics", 0.1)  # 降低启发式
   m.setParam("MIPFocus", 2)      # 聚焦最优解证明
   m.setParam("Threads", 8)       # 并行
3 | 每条参数单测：记录节点数和求解时间的变化
4 | 找出你的 kkt_bilevel 问题的最佳参数组合
```
✅ **验证**：参数调优后求解时间至少下降 20%

### Day 23 — High-Point Relaxation (HPR)

```
1 | HPR = 去掉下层KKT条件，只保留上层+下层原始可行
2 | 从 kkt_bilevel_complete.py 复制 → 删掉所有互补约束和0-1变量
3 | 跑 HPR → 这是"理论上界"
4 | 与 KKT 完整模型的解对比 → 差距有多大？
5 | 差距越小 = KKT 模型越紧越好解
```
✅ **验证**：得到 HPR 上界和 KKT 解，计算 gap%

### Day 24 — 读 ddro-via-bilevel 的代码结构

**文件**: `D:/Python_Projects/bilevel_practice/ddro-via-bilevel/`
```
1 | 看目录结构：shortest_path/portfolio/ 等文件夹
2 | 打开 shortest_path/model.py → 找 strong_duality 关键词
3 | 截取核心片段（强对偶转换的Gurobi代码）
4 | 与你的 kkt_bilevel_complete.py 对比结构异同
5 | 笔记：记录别人代码里你觉得值得学的写法
```
✅ **验证**：能说出 ddro-via-bilevel 与你写法的 3 个不同点

### Day 25 — 综合项目设计（自己定义问题）

**定题**
```
1 | 基于 kkt_bilevel_complete.py 的框架
2 | 定义你自己的小问题，满足：
   - 1 个上层变量，2 个下层变量
   - 下层有 2-3 个约束
   - 下层是 2 目标：权重法转换
3 | 写出完整数学形式
4 | 翻译成 Gurobi 代码
```
✅ **验证**：自定问题的代码能跑出合理结果

### Day 26 — 综合项目：双层+多目标+调参

```
1 | 在 Day 25 的代码上加：
   - 多目标下层（ε-约束法或权重法）
   - 最优参数组合（Day 22 的结果）
   - 写 LP 文件检查模型
2 | 做灵敏度分析：参数变化时解的变化
3 | 如果有时间：对比大M法 vs SOS1法的求解器 log
```
✅ **验证**：完成一个完整的"双层+多目标+Gurobi调参"案例

### Day 27 — 读导师论文 + 映射到 Gurobi 代码

```
1 | 拿出导师彭振华的论文
2 | 把论文中的数学模型 → 标出：
   - 哪些是上层/下层变量
   - 目标函数是什么（单目标/多目标/DC结构?）
   - 下层约束条件
3 | 评估：现有代码框架能否覆盖？需要新增什么？
4 | 列出"从教程到论文"的差距清单
```
✅ **验证**：有一份论文→代码的映射表

### Day 28 — 总结复盘 + 后续计划

```
1 | 整理 4 周学到的核心模板：
   - 单层LP/MIP模板
   - KKT转化模板（大M + SOS1）
   - 强对偶转化模板
   - 多目标模板（ε-约束 + 权重法 + 分层法）
   - Gurobi调参模板
2 | 评估当前水平：
   - 能独立写简单的双层问题
   - 能读懂 ddro-via-bilevel 的核心代码
   - 能调参提升求解速度
3 | 方向建议：
   - 下一步：啃 DC 算法（你导师方向）
   - 再下一步：iP-DCA 迭代分解
```
✅ **里程碑**：有 5 个可复用的 Gurobi 代码模板 + 论文映射表

---

## 附录：快速启动命令

```bash
# 打开 Spyder
start "" "D:\Anaconda3\Scripts\spyder.exe"

# 在终端快速测试 Gurobi
D:/Anaconda3/python.exe -c "import gurobipy; print('OK')"

# Python 使用 Anaconda 的
D:/Anaconda3/python.exe your_script.py

# 写 LP 文件检查
m.write("model.lp")  # 记事本打开
```

## 附录：本地已有文件速查

| 文件 | 用途 | 周次 |
|------|------|------|
| `mip1.py` | 最简单0-1规划 | W1-D1 |
| `lp.py` | 连续变量LP | W1-D2 |
| `diet.py` | 配餐问题(完整建模) | W1-D3 |
| `facility.py` | 选址问题(0-1规划经典) | W1-D4 |
| `multiobj.py` | 多目标分层法 ⭐ | W1-D5 |
| `sos.py` | SOS1约束示例 | W1-D6 |
| `sensitivity.py` | 灵敏度分析 | W1-D2 |
| `kkt_bilevel_complete.py` | KKT单层转化完整版 ⭐⭐ | W2-D10 |
| `portfolio.py` | 投资组合(QP) | 选做 |
| `piecewise.py` | 分段线性化 | 选做 |
