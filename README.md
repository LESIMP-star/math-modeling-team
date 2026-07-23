# 🚀 Gurobi 进阶学习工作区

> 目标：2026 年 9 月国赛前掌握 Gurobi 双层/多目标优化  
> 用户：NCU 金融数学大一，导师彭振华（WHU，双层+DC方向）  
> 环境：Gurobi 13.0.0 + D:/Anaconda3/python.exe + Spyder  
> 开始日期：2026-07-24 → 国赛约 2026-09-04（**倒计时 42 天**）

---

## 📁 目录结构

```
gurobi-study/
├── week1-basics/          # 第1周: Gurobi 基础 + 多目标 API
│   ├── day1-mip1/         # 第一个 MIP (mip1.py)
│   ├── day2-lp/           # LP + 影子价格 (lp.py, sensitivity.py)
│   ├── day3-diet/         # 营养配餐 (diet.py 完整建模)
│   ├── day4-facility/     # 设施选址 (facility.py 0-1规划经典)
│   ├── day5-multiobj/     # 多目标分层法 (multiobj.py + 简化版)
│   ├── day6-sos/          # SOS1 互补约束 (sos.py + 练习)
│   └── day7-review/       # 复习挑战 (week1_review.py)
│
├── week2-bilevel/         # 第2周: KKT / 强对偶单层转化
│   ├── day8-math-form/    # 双层标准形式 (数学推导)
│   ├── day9-kkt-deriva/   # KKT 条件回顾 (纸上推导)
│   ├── day10-kkt-bigm/    # ⭐ KKT + 大M法 (完整实例)
│   ├── day11-kkt-sos1/    # KKT + SOS1 (对比大M)
│   ├── day12-strong-dual/ # 强对偶转化 (理论+代码)
│   ├── day13-repo-read/   # 读 ddro-via-bilevel 代码
│   └── day14-review/      # 复习挑战 (week2_review.py)
│
├── week3-multi-bilevel/   # 第3周: 多目标 × 双层
│   ├── day15-math-form/   # 多目标双层数学形式
│   ├── day16-epsilon-pri/ # ε-约束法原理
│   ├── day17-epsilon-cod/ # ⭐ ε-约束法代码实现
│   ├── day18-pyaugmecon/  # pyaugmecon 库
│   ├── day19-kkt-multi/   # ⭐ 多目标下层+KKT
│   ├── day20-full-case/   # 完整案例
│   └── day21-review/
│
├── week4-tuning/          # 第4周: Gurobi 调参 + 综合项目
│   ├── day22-params/      # ⭐ 参数调优模板
│   ├── day23-hpr/         # ⭐ High-Point Relaxation
│   ├── day24-ddroad/      # 读 ddro-via-bilevel 结构
│   ├── day25-project/     # 综合项目设计 (模板)
│   ├── day26-project-goal/# 项目完成
│   ├── day27-paper-map/   # 论文→代码映射
│   └── day28-review/
│
├── week5-competition/     # 第5周: 国赛实战模拟
│   ├── day29-30/          # 模拟赛题1
│   ├── day31-32/          # 模拟赛题2
│   ├── day33-34/          # 模拟赛题3
│   └── day35-review/
│
├── week6-final-sprint/    # 第6周: 最后冲刺
│   ├── day36-37/          # 知识复盘
│   ├── day38-39/          # 国赛策略
│   ├── day40-41/          # 模板整理
│   └── day42-review/      # 考前准备
│
├── references/            # 参考资料
│   ├── gurobi_study_plan_detailed.md  # 完整28天计划
│   ├── math-to-code-translation.md    # 公式→代码对照
│   └── (额外Gurobi官方示例)
│
├── github-repos/          # GitHub 下载的仓库
│   └── README.md          # 各仓库说明+链接
│
└── my-practice/           # 你自己的练习代码
```

## 📅 42天学习冲刺计划

### 第 1 周：Gurobi 基础 (7/24 - 7/30)
**每天 1 小时，在 Spyder 里跑通官方示例**

| 天 | 内容 | 核心文件 | 验证标准 |
|----|------|---------|---------|
| 1 | 第一个 MIP | `day1/mip1.py` | 输出 Obj=3 + 改参数 |
| 2 | LP + 影子价格 | `day2/lp.py` | 看懂 Pi/Slack |
| 3 | 营养配餐 | `day3/diet.py` | 改数据后重新跑 |
| 4 | 设施选址 | `day4/facility.py` | 画分配图 |
| 5 | ⭐ 多目标分层 | `day5/multiobj_simple.py` | 改 priority/weight |
| 6 | SOS1 约束 | `day6/sos_practice.py` | 两种写法对比 |
| 7 | 复习 | `day7/week1_review.py` | 3个挑战全过 |

### 第 2 周：双层→KKT 转化 (7/31 - 8/6) 🔥 **核心**
**每天 1.5 小时，理解和跑通 KKT 代码**

| 天 | 内容 | 核心文件 | 验证标准 |
|----|------|---------|---------|
| 8 | 双层数学形式 | 纸上推导 | 论文变量对上号 |
| 9 | KKT 条件回顾 | 纸上推导 | 写出3条KKT |
| 10 | ⭐ KKT+大M | `day10/kkt_bilevel_complete.py` | 互补条件=0 |
| 11 | KKT+SOS1 | `day11/kkt_bilevel_sos1.py` | 对比大M版本 |
| 12 | 强对偶转化 | 看 ddro 代码 | 理解为啥更快 |
| 13 | 读 ddro 代码 | `github-repos/ddro-via-bilevel/` | 跑通一个案例 |
| 14 | 复习 | `day14/week2_review.py` | 4个挑战全过 |

### 第 3 周：多目标 × 双层 (8/7 - 8/13)
**每天 1.5 小时**

| 天 | 内容 | 核心文件 | 验证标准 |
|----|------|---------|---------|
| 15 | 多目标双层形式 | 纸上 | 写出形式 |
| 16 | ε-约束原理 | 纸上 | 手算5个点 |
| 17 | ⭐ ε-约束代码 | `day17/epsilon_constraint.py` | 画帕累托图 |
| 18 | pyaugmecon | 跑通示例 | 对比手写 |
| 19 | ⭐ 多目标下层KKT | `day19/kkt_bilevel_multiobj.py` | 权重法扫描 |
| 20 | 完整案例 | 从 day19 改 | 改约束后跑通 |
| 21 | 复习 | 整理笔记 | 3条路径 |

### 第 4 周：调参 + 综合项目 (8/14 - 8/20)
**每天 1.5 小时**

| 天 | 内容 | 核心文件 | 验证标准 |
|----|------|---------|---------|
| 22 | ⭐ 参数调优 | `day22/param_tuning_template.py` | 加速≥20% |
| 23 | ⭐ HPR | `day23/hpr_relaxation.py` | 算 gap% |
| 24 | 读 ddro 结构 | 看代码 | 对比自己写法 |
| 25 | 项目设计 | `day25/project_design.py` | 填 TODO |
| 26 | 项目完成 | 调参+结果 | 完整案例 |
| 27 | 论文→代码映射 | `day27/paper_mapping.py` | 填论文公式 |
| 28 | 复习 | 整理5个模板 | 汇总 |

### 第 5 周：国赛模拟 (8/21 - 8/27)
**每天 2 小时，模拟比赛节奏**

| 天 | 内容 | 做什么 |
|----|------|--------|
| 29-30 | 模拟赛题1 | 找往年A题，用Gurobi写完整建模 |
| 31-32 | 模拟赛题2 | 找往年B题，做灵敏度分析 |
| 33-34 | 模拟赛题3 | 找往年C题，大数据+优化 |
| 35 | 复盘 | 总结卡点 |

### 第 6 周：最后冲刺 (8/28 - 9/3)
**以复习和策略为主**

| 天 | 内容 | 做什么 |
|----|------|--------|
| 36-37 | 知识复盘 | 重跑 5 个核心模板 |
| 38-39 | 国赛策略 | 读优秀论文+排版 |
| 40-41 | 模板整理 | 打包成自己的工具库 |
| 42 | 考前准备 | 环境检查+心态 |

---

## 🎯 核心文件索引（⭐ 最重要）

| 文件 | 重要性 | 完成状态 | 说明 |
|------|--------|---------|------|
| `day10-kkt-bigm/kkt_bilevel_complete.py` | ⭐⭐⭐ | ✅ 已跑通 | KKT完整版(含3条互补) |
| `day11-kkt-sos1/kkt_bilevel_sos1.py` | ⭐⭐ | ✅ 已生成 | SOS1替代大M |
| `day17-epsilon-code/epsilon_constraint.py` | ⭐⭐⭐ | ✅ 已生成 | ε-约束法+绘图 |
| `day19-kkt-multiobj/kkt_bilevel_multiobj.py` | ⭐⭐⭐ | ✅ 已生成 | 多目标下层KKT |
| `day22-params/param_tuning_template.py` | ⭐⭐ | ✅ 已生成 | Gurobi调参测试 |
| `day23-hpr/hpr_relaxation.py` | ⭐⭐ | ✅ 已生成 | HPR vs KKT |
| `day25-project/project_design.py` | ⭐⭐ | ✅ 已生成 | 综合项目模板 |

---

## 📦 GitHub 仓库索引

这些是原计划提到的仓库，网络允许时克隆到 `github-repos/`：

```bash
# ⭐ 最关键 (W2用): KKT/强对偶
git clone --depth 1 https://github.com/simstevens/ddro-via-bilevel.git

# 官方示例 (W1参考)
git clone --depth 1 https://github.com/lx249/gurobi-modeling-examples.git

# 中文注释版 (选)
git clone --depth 1 https://github.com/zhuqiu8/Guroi_modeling-examples.git

# AUGMECON (W3用): ε-约束法
git clone --depth 1 https://github.com/wouterbles/pyaugmecon.git

# 多目标Gurobi (W3参考)
git clone --depth 1 https://github.com/Dr-BAli/Multi-Objective-Optimization-Using-Gurobi.git

# 双层基准测试 (W4参考)
git clone --depth 1 https://github.com/benchopt/benchmark_bilevel.git
```

各仓库用途：
| 仓库 | 周次 | 主要价值 |
|------|------|---------|
| `ddro-via-bilevel` | W2-W3 | KKT/强对偶转化代码 ⭐ |
| `gurobi-modeling-examples` | W1 | Optimization 101 多目标 |
| `pyaugmecon` | W3 | 增强ε-约束法实现 |
| `Multi-Objective-Optimization-Using-Gurobi` | W3 | 权重法+帕累托 |
| `benchmark_bilevel` | W4 | 算法选型参考 |

---

## 💡 每日学习流程

```
1. 打开 Spyder
2. cd D:/Python_Projects/gurobi-study
3. 找到今天的 day 文件夹
4. 打开 .py 文件 → #%% 分块跑
5. 改 ==TODO== 或 ★ 标记的参数
6. 观察输出是否与预期一致
7. 不一致 → 看文件里的注释提示
8. ✅ 验证条件通过 → 明天继续
```

## 🔧 快速命令

```bash
# 运行任何练习文件
D:/Anaconda3/python.exe day10-kkt-bigm/kkt_bilevel_complete.py

# 写 LP 文件检查
# 在代码末尾加:  m.write("check.lp")
# 然后用记事本打开

# Spyder 打开方式
# start "" "D:\Anaconda3\Scripts\spyder.exe"
```

---

## 📐 学习原则

1. **先跑通，再理解** — 不要试图一次性看懂全部代码
2. **每次只改 1 个参数** — 观察变化，理解因果关系
3. **#%% 分块跑** — Spyder 的 Cell 模式，一段段验证
4. **纸上公式→代码** — 先写数学形式再翻译成 Gurobi
5. **每周必须复习** — 复习日的 3-4 个挑战必须自己手写
6. **跑不通就问** — 把错误信息和代码发给我

---

## 📎 推荐 GitHub 项目

| 项目 | 说明 | 适用 |
|------|------|------|
| [ddro-via-bilevel](https://github.com/simstevens/ddro-via-bilevel) | ⭐ KKT/强对偶单层转化，含最短路径/背包/投资组合案例 | W2 核心参考 |
| [gurobi-modeling-examples](https://github.com/lx249/gurobi-modeling-examples) | Gurobi 官方建模示例合辑（Notebook） | W1 入门参考 |
| [gurobi-modeling-examples (中文)](https://github.com/zhuqiu8/Guroi_modeling-examples) | 同上，带中文注释 | W1 中文友好 |
| [pyaugmecon](https://github.com/wouterbles/pyaugmecon) | 增强 ε-约束法，Python + Gurobi，自动帕累托前沿 | W3 ε-约束法 |
| [Multi-Objective-Optimization-Using-Gurobi](https://github.com/Dr-BAli/Multi-Objective-Optimization-Using-Gurobi) | 权重法 + 帕累托前沿 + Gurobi `setObjectiveN` | W3 多目标参考 |
| [Bilevel-Optimization-Emissions](https://github.com/ainiusheng/Bilevel-Optimization-Emissions) | 双层 + 多目标（利润/排放/成本），电力定价场景 | W2-W3 双层+多目标 |
| [benchmark_bilevel](https://github.com/benchopt/benchmark_bilevel) | 双层优化基准测试框架，多求解器对比 | W4 算法选型 |
| [DeepRL-BiobjectiveKP](https://github.com/Multi-Objective-Optimization-Laboratory/DeepRL-BiobjectiveKP) | AUGMECON + Gurobi，双目标背包问题 | W3 ε-约束法 |
| [TETREES](https://github.com/SoftwareImpacts/SIMPAC-2025-349) | 精确 ε-约束法，Python + Gurobi，服务-资源分配 | W3 ε-约束法 |
| [Solver-for-MIQP-QP-Bilevel-Problems](https://github.com/AndreasHorlaender/Solver-for-MIQP-QP-Bilevel-Problems) | 高松弛（HPR）vs KKT，变量松弛+切割平面 | W4 加速技巧 |
| [VF-iDCA](https://github.com/SUSTech-Optimization) | iDCA 迭代分解（超参数选择），SUSTech 系列 | 进阶参考（iP-DCA） |

---

> 祝国赛顺利！有任何卡点直接 @ 我。
