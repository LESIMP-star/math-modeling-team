# 🚀 Gurobi 数学建模工具库

**给队友的：** 这是咱们队共享的 Gurobi 学习 + 比赛代码库。直接 clone 下来就能跑。

```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
# 用 D:/Anaconda3/python.exe 跑任意 .py 文件
```

**关于我：** NCU 金融数学，方向双层优化+DC算法（导师彭振华）。  
**目标：** 2026 国赛前掌握 Gurobi 求解大规模双层/多目标优化。

---

## 📁 目录

```
├── week1-basics/       ← 从零学 Gurobi（每天一个可跑示例）
├── week2-bilevel/      ← ⭐ 双层→KKT 单层转化（核心）
├── week3-multi-bilevel/ ← 多目标×双层
├── week4-tuning/       ← Gurobi 调参 + 综合项目
├── week5-competition/  ← 国赛模拟
├── week6-final-sprint/ ← 最后冲刺
│
├── competition/        ← 【国赛时用】三人协作区
│   ├── model/          ← Gurobi 求解代码
│   ├── data/           ← 赛题数据
│   └── figs/           ← 结果图
│
├── skills/             ← 数模全流程工作流（选题→建模→写论文）
│   └── math-model/     ← 含 agent 定义、算法库、论文模板
│
├── courses/            ← 课程资料（最优化、运筹学等）
│   └── 最优化课程/      ← 彭老师课件
│
├── references/         ← 资料索引
│   ├── latex/          ← LaTeX教程PDF
│   └── official_examples_index.md
│
├── my-practice/        ← 你自己的练习
└── github-repos/       ← 推荐的外部项目
```

## 🔧 怎么用

| 阶段 | 做什么 |
|------|--------|
| **赛前** | 各人 clone 仓库，跟着 week1→6 自学 Gurobi |
| **赛中** | 在 `competition/` 下建文件夹，各写各的，`git push` 同步 |
| **赛后** | 优秀解法整理进 `references/`，下次复用 |

## 🖥 运行环境

- Gurobi 13.0.0（License 2841306，有效期至 2027-07）
- Python：`D:/Anaconda3/python.exe`
- 编辑器：Spyder（推荐 `#%%` 分块跑）
- 论文：Overleaf（实时协作，不放在 GitHub 里）

---

## 📚 数学建模学习（给队友）

这个仓库同时记录数模学习过程。你们可以：

- 跟着 `week1→6` 自学 Gurobi
- 每周跑通一个示例，在 **微信群** 打卡
- 有好的资料直接往 `references/` 里加
- 国赛时在 `competition/` 下协作

> 不会 Git 操作没关系，直接往文件夹里放文件也行，我统一提交。

---

## 📅 42 天学习路线

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

---

## 📎 推荐资源

| 资源 | 说明 |
|------|------|
| [最优化课程 - 彭振华](https://zhenhuapeng.github.io/coursematerials/) | 导师的最优化课程，和 Gurobi 学习同步进行 |
| [ddro-via-bilevel](https://github.com/simstevens/ddro-via-bilevel) | ⭐ KKT/强对偶单层转化—最短路径/背包/投资组合案例 |
| [gurobi-modeling-examples](https://github.com/lx249/gurobi-modeling-examples) | Gurobi 官方建模示例合辑（Notebook） |
| [gurobi-modeling-examples (中文)](https://github.com/zhuqiu8/Guroi_modeling-examples) | 同上，带中文注释 |
| [pyaugmecon](https://github.com/wouterbles/pyaugmecon) | 增强 ε-约束法，Python + Gurobi，自动帕累托前沿 |
| [Multi-Objective-Optimization-Using-Gurobi](https://github.com/Dr-BAli/Multi-Objective-Optimization-Using-Gurobi) | 权重法 + 帕累托前沿 + Gurobi `setObjectiveN` |
| [benchmark_bilevel](https://github.com/benchopt/benchmark_bilevel) | 双层优化基准测试框架 |
| [Solver-for-MIQP-QP-Bilevel-Problems](https://github.com/AndreasHorlaender/Solver-for-MIQP-QP-Bilevel-Problems) | 高松弛（HPR）vs KKT，切割平面 |
| [VF-iDCA](https://github.com/SUSTech-Optimization) | iDCA 迭代分解（超参数选择）|

---

> 祝国赛顺利！有任何卡点直接 @ 我。
