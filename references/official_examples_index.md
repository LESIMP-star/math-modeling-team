# Gurobi 官方示例分类 (E:\Ai_configs\win64\examples\python\)

## ✅ 已搬到 D 盘学习区的 (12个)
这些是学习路线需要的，已按天分好。

## ❌ 不搬的 36 个 — 按类说明

### 1️⃣ 和你的方向完全无关 (16个) — 跳过

| 文件 | 内容 | 为什么不需要 |
|------|------|------------|
| `acopf_4buses.py` | 电力系统交流潮流 | 电力专业，非建模方向 |
| `batchmode.py` | Batch 模式求解 | 运维功能，非模型 |
| `callback.py` | 回调函数自定义终止 | Gurobi 高级用法，建模用不到 |
| `dense.py` | 稠密矩阵 QP | 数值计算技巧 |
| `diet3.py` | SQLite 数据库读取 | 数据格式，非模型 |
| `diet3a.py` | MS Access ODBC 读取 | 同上 |
| `diet4.py` | Excel 数据读取 | 同上 |
| `fixanddive.py` | MIP 启发式 | 求解器算法，非建模 |
| `lpmethod.py` | Method 参数对比 | 参数调优，第4周才需接触 |
| `lpmod.py` | LP 修改重解 | 技巧性操作 |
| `mip1_remote.py` | 远程服务配置 | 网络配置无关 |
| `matrix1.py` / `matrix2.py` | 矩阵 API 写法 | 语法糖，非必须（已放 references/） |
| `multiscenario.py` | 多场景分析 | 太专业，建模初赛用不到 |
| `params.py` | 参数设置大全 | 参考文件即可（已放 references/） |
| `tune.py` | 自动参数调优 | 第4周才用到 |

### 2️⃣ 以后可能会用到 (10个) — 先放着，用到再搬

| 文件 | 内容 | 可能用到的情况 |
|------|------|--------------|
| `bilinear.py` | 双线性规划 | 下层不是 LP 时可能遇到 |
| `genconstr.py` | min/max/abs 约束 | 建模常用，但语法简单，看文档就行 |
| `genconstrnl.py` | sin/x² 非线性约束 | 非凸问题，Gurobi 支持有限 |
| `gc_pwl.py` | 分段线性约束 | 非线性转线性时有用 ⭐ |
| `gc_pwl_func.py` | PWL 函数 | 同上 |
| `piecewise.py` | 分段线性目标 | 同上（已放 references/） |
| `poolsearch.py` | 解池搜索 | 求多个可行解时用 |
| `feasopt.py` | 不可行分析 | 模型跑 infeasible 时调试用 ⭐ |
| `qcp.py` | 二次约束规划 | 下层是 QP 时用 |
| `qp.py` | 二次规划 | 投资组合等（已放 references/） |

### 3️⃣ 经典模型案例 (10个) — 和国赛建模相关 ⭐

| 文件 | 模型类型 | 国赛可能用到？ | 建议 |
|------|---------|--------------|------|
| `netflow.py` | 多商品流 | ⭐ 运输/物流题 | 等遇到再搬 |
| `mip2.py` | MIP 解池 | ⭐ 求多个方案 | 第4周调参时再学 |
| `tsp.py` | 旅行商 | ⭐ 路径优化题 | 经典但国赛不常考 |
| `sudoku.py` | 数独约束 | ❌ 娱乐题 | 跳过 |
| `workforce1.py` | 排班基础 | ⭐ 排班/调度 | 等遇到排班题再学 |
| `workforce2.py` | 排班+IIS | 同上 | 同上 |
| `workforce3.py` | 排班+迭代 | 同上 | 同上 |
| `workforce4.py` | 排班+松驰 | 同上 | 同上 |
| `workforce5.py` | 排班+多目标 | ⭐⭐ 排班+多目标 | 这个最有价值，学到多目标时可参考 |
| `workforce_batchmode.py` | 排班+batch | 跳过 | 排班+batch 高级用法 |

---

## 总结：和你的交叉方向 (双层+DC) 的关系

| 分类 | 数量 | 与你的方向 |
|------|------|-----------|
| 完全无关 | 16 个 | 电力/数据库/高级功能，跳过 |
| 以后可能用 | 10 个 | **`bilinear.py`**（双线性→DC 相关）和 **`feasopt.py`**（调试用）值得记下 |
| 经典建模 | 10 个 | **`workforce5.py`**（排班+多目标）是你第3周的直接参考 |

**目前第 1 周不需要任何额外文件**。等你学到特定模型（比如双层遇到双线性约束、排班遇到多目标），再从 E 盘原目录搬对应的文件就行。
