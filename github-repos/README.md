# GitHub 仓库索引

网络允许时，在 `D:\Python_Projects\gurobi-study\github-repos\` 下执行：

## ⭐ 核心仓库 (按优先级)

### 1. ddro-via-bilevel (W2-W3 最重要)
```bash
git clone --depth 1 https://github.com/simstevens/ddro-via-bilevel.git
```
- **用途**: KKT/强对偶转化代码
- **关键文件**: `shortest_path/model.py` (找 strong_duality)
- **参考**: 作者说强对偶比KKT更快

### 2. gurobi-modeling-examples (W1 入门)
```bash
git clone --depth 1 https://github.com/lx249/gurobi-modeling-examples.git
```
- **用途**: Gurobi官方建模示例
- **关键文件**: `Optimization 101` Notebook

### 3. pyaugmecon (W3 ε-约束法)
```bash
git clone --depth 1 https://github.com/wouterbles/pyaugmecon.git
```
- **用途**: 增强ε-约束法
- **安装**: `pip install pyaugmecon`

### 4. Multi-Objective-Optimization-Using-Gurobi (W3)
```bash
git clone --depth 1 https://github.com/Dr-BAli/Multi-Objective-Optimization-Using-Gurobi.git
```
- **用途**: 权重法+帕累托前沿

### 5. benchmark_bilevel (W4)
```bash
git clone --depth 1 https://github.com/benchopt/benchmark_bilevel.git
```
- **用途**: 双层优化基准测试

## 辅助仓库

### 6. Guroi_modeling-examples (中文版)
```bash
git clone --depth 1 https://github.com/zhuqiu8/Guroi_modeling-examples.git
```

### 7. Bilevel-Optimization-Emissions
```bash
git clone --depth 1 https://github.com/ainiusheng/Bilevel-Optimization-Emissions.git
```
- 双层+多目标(利润/排放/成本)

### 8. DeepRL-BiobjectiveKP
```bash
git clone --depth 1 https://github.com/Multi-Objective-Optimization-Laboratory/DeepRL-BiobjectiveKP.git
```

### 9. SIMPAC-2025-349 (TETREES)
```bash
git clone --depth 1 https://github.com/SoftwareImpacts/SIMPAC-2025-349.git
```

### 10. Solver-for-MIQP-QP-Bilevel-Problems
```bash
git clone --depth 1 https://github.com/AndreasHorlaender/Solver-for-MIQP-QP-Bilevel-Problems.git
```
- 高松弛(HPR)+切割平面

---

## 📝 说明

- 所有仓库均使用 `--depth 1`（只取最新版本，不下载历史）
- 每个仓库 < 50MB，正常网络下 2-5 分钟完成全部
- 克隆后自然融入对应 week/day 的学习任务
