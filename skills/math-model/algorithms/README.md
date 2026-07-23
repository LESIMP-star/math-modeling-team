# Math-Model 算法库

本目录包含数学建模竞赛所需的各类算法和工具模块。

## 目录结构

```
algorithms/
├── __init__.py
├── README.md                    # 本文件
├── evaluation/                  # 评价类算法
│   ├── __init__.py
│   ├── topsis.py               # TOPSIS评价法
│   ├── entropy_weight.py       # 熵权法
│   └── lasso_feature_selection.py  # LASSO特征选择
├── prediction/                  # 预测类算法
│   ├── __init__.py
│   ├── grey_prediction.py      # 灰色预测
│   ├── huber_regression.py     # Huber回归
│   └── breakpoint_detection.py # 断点检测
├── optimization/                # 优化类算法
│   ├── __init__.py
│   ├── genetic_algorithm.py    # 遗传算法
│   ├── simulated_annealing.py  # 模拟退火
│   └── particle_swarm.py       # 粒子群算法
├── clustering/                  # 聚类类算法
│   ├── __init__.py
│   ├── kmeans.py               # K-means聚类
│   └── dbscan.py               # DBSCAN聚类
├── plotting/                    # 绘图工具
│   ├── __init__.py
│   ├── basic_plots.py          # 基础图表
│   ├── correlation.py          # 相关性图表
│   ├── sensitivity.py          # 灵敏度分析
│   ├── utils.py                # 绘图工具
│   └── layout.py               # 布局调整（新增）
├── literature/                  # 文献管理（新增）
│   ├── __init__.py
│   ├── search.py               # 文献搜索
│   ├── verify.py               # 文献验证
│   └── citation.py             # 引用生成
├── code_style/                  # 代码风格（新增）
│   ├── __init__.py
│   ├── humanize.py             # 风格转换
│   ├── simplify.py             # 变量名简化
│   └── encoding.py             # 编码处理
└── paper/                       # 论文格式（新增）
    ├── __init__.py
    ├── formatting.py            # 格式化
    ├── validation.py            # 验证
    ├── materials.py             # 支撑材料
    └── appendix.py              # 附录处理
```

## 模块说明

### 1. 评价类算法 (evaluation/)

用于多指标评价和决策分析。

- **TOPSIS**: 逼近理想解排序法，适用于多指标综合评价
- **熵权法**: 客观赋权方法，基于信息熵确定指标权重
- **LASSO**: 特征选择方法，用于降维和变量筛选

### 2. 预测类算法 (prediction/)

用于时间序列预测和趋势分析。

- **灰色预测**: 小样本预测方法，适用于数据量较少的情况
- **Huber回归**: 鲁棒回归方法，对异常值不敏感
- **断点检测**: 时间序列突变点检测

### 3. 优化类算法 (optimization/)

用于组合优化和参数优化。

- **遗传算法**: 启发式优化算法，适用于复杂优化问题
- **模拟退火**: 全局优化算法，避免陷入局部最优
- **粒子群算法**: 群智能优化算法，收敛速度快

### 4. 聚类类算法 (clustering/)

用于数据分类和模式识别。

- **K-means**: 划分聚类算法，简单高效
- **DBSCAN**: 密度聚类算法，能发现任意形状的簇

### 5. 绘图工具 (plotting/)

用于生成各类图表。

- **基础图表**: 折线图、柱状图、散点图等
- **相关性图**: 热力图、散点矩阵等
- **灵敏度图**: 灵敏度分析图表
- **布局调整**: 自动调整图表布局，避免重叠（新增）

### 6. 文献管理 (literature/) - 新增

用于文献搜索、验证和引用。

- **文献搜索**: 多平台搜索策略
- **文献验证**: 验证文献真实性，解决AI幻觉问题
- **引用生成**: 自动生成标准引用格式

### 7. 代码风格 (code_style/) - 新增

用于优化代码风格，降低AIGC检测率。

- **风格转换**: 将AI风格代码转换为人类风格
- **变量名简化**: 自动简化长变量名
- **编码处理**: 处理Unicode字符，确保Windows兼容

### 8. 论文格式 (paper/) - 新增

用于论文格式验证和规范化。

- **格式化**: 标题编号、格式规范
- **验证**: 格式验证、引用检查
- **支撑材料**: 材料完整性验证
- **附录**: 代码插入验证

## 使用方法

### 1. 直接调用

```python
from algorithms.evaluation.topsis import topsis
from algorithms.plotting.layout import auto_adjust_layout
from algorithms.literature.verify import verify_literature
```

### 2. 命令行调用

```bash
python algorithms/evaluation/topsis.py --input data.csv --output result.png
python algorithms/plotting/layout.py --input figure.svg --output figure_adjusted.svg
```

### 3. 在 math-model skill 中调用

SKILL.md 中已配置自动调用这些算法，无需手动调用。

## 更新日志

### v2.0 (2026-05-29)

**新增模块**:
- 文献管理模块 (literature/)
- 代码风格模块 (code_style/)
- 论文格式模块 (paper/)
- 图表布局调整 (plotting/layout.py)

**优化内容**:
- 解决AI幻觉文献问题
- 解决图表重叠问题
- 解决AIGC检测率问题
- 解决论文格式规范问题

**适用范围**:
- 所有类型的数学建模竞赛
- 支持中英文论文
- 支持多种比赛模板

## 注意事项

1. **编码兼容**: 所有代码确保Windows GBK兼容
2. **字体设置**: 根据语言自动设置中英文字体
3. **文献验证**: 所有文献必须通过真实性验证
4. **图表规范**: 图表必须无重叠、中文标注、高分辨率
5. **代码风格**: 代码必须优化风格，降低AIGC检测率

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目路径: `~/.claude/skills/math-model/`
- 文档路径: `~/.claude/skills/math-model/SKILL.md`

---

**最后更新**: 2026年5月29日
**版本**: v2.0
**适用范围**: 所有数学建模竞赛
