# Math-Model Skill 优化方案

## 一、问题总结与分类

### 1.1 文献搜索问题（最高优先级）

| 问题 | 影响范围 | 根本原因 | 优化方案 |
|------|---------|---------|---------|
| **AI幻觉文献** | 所有比赛 | 模型编造不存在的文献 | 建立文献验证机制 |
| **WebSearch不可用** | 所有比赛 | 环境配置问题 | 多平台备用方案 |
| **WebFetch失败** | 所有比赛 | 网站反爬机制 | API优先策略 |
| **关键词过多** | 所有比赛 | 搜索策略不当 | 智能关键词生成 |
| **作者/期刊虚假** | 所有比赛 | 未验证来源 | 强制验证流程 |

### 1.2 图表问题

| 问题 | 影响范围 | 根本原因 | 优化方案 |
|------|---------|---------|---------|
| **图例重叠** | 所有比赛 | 布局参数不当 | 自动调整机制 |
| **英文标注** | 中文比赛 | 未设置中文字体 | 自动检测语言 |
| **图表未插入** | 所有比赛 | 遗漏检查 | 证据门控验证 |
| **分辨率不足** | 所有比赛 | 未设置DPI | 统一导出规范 |

### 1.3 代码问题

| 问题 | 影响范围 | 根本原因 | 优化方案 |
|------|---------|---------|---------|
| **AIGC率高** | 所有比赛 | AI风格明显 | 代码风格转换 |
| **变量名过长** | 所有比赛 | AI生成习惯 | 自动简化工具 |
| **编码错误** | Windows | GBK兼容问题 | Unicode铁律 |
| **注释过多** | 所有比赛 | AI过度注释 | 智能注释精简 |

### 1.4 论文问题

| 问题 | 影响范围 | 根本原因 | 优化方案 |
|------|---------|---------|---------|
| **标题编号混乱** | 所有比赛 | 格式不统一 | 自动编号系统 |
| **摘要位置错误** | 所有比赛 | 流程顺序 | 明确步骤要求 |
| **支撑材料不全** | 所有比赛 | 遗漏检查 | 清单验证机制 |
| **附录代码缺失** | 所有比赛 | 流程遗漏 | 强制插入步骤 |

### 1.5 模型逻辑问题

| 问题 | 影响范围 | 根本原因 | 优化方案 |
|------|---------|---------|---------|
| **过度优化** | 优化类题目 | 追求完美解 | 增加随机性 |
| **忽略实际约束** | 应用类题目 | 纯数学思维 | 多维度分析 |
| **模型同质化** | 多问题题目 | 缺乏针对性 | 差异化建模 |
| **缺乏深度** | 所有比赛 | 分析不足 | 定性+定量结合 |

---

## 二、优化方案详细设计

### 2.1 文献搜索系统重构

#### 2.1.1 多平台搜索策略

```python
# 新增：文献搜索优先级系统
SEARCH_PRIORITY = {
    "level1": {  # 优先使用
        "中文": [
            "https://www.cnki.net",  # 知网
            "https://www.wanfangdata.com.cn",  # 万方
            "https://xueshu.baidu.com",  # 百度学术
        ],
        "英文": [
            "https://api.crossref.org",  # CrossRef API
            "https://api.semanticscholar.org",  # Semantic Scholar API
            "https://arxiv.org/api",  # arXiv API
        ]
    },
    "level2": {  # 备用方案
        "中文": [
            "https://www.cqvip.com",  # 维普
            "https://scholar.google.com",  # Google Scholar
        ],
        "英文": [
            "https://www.webofscience.com",  # Web of Science
            "https://www.scopus.com",  # Scopus
        ]
    },
    "level3": {  # 最后手段
        "手动搜索": [
            "用户手动在知网搜索",
            "下载PDF后AI辅助总结",
        ]
    }
}
```

#### 2.1.2 文献验证机制

```python
# 新增：文献验证函数
def verify_literature(literature):
    """
    验证文献真实性
    返回：{
        "is_valid": bool,
        "confidence": float,  # 0-1
        "verification_details": dict,
        "warnings": list
    }
    """
    checks = {
        "author_exists": check_author(literature["author"]),
        "journal_exists": check_journal(literature["journal"]),
        "doi_valid": check_doi(literature["doi"]),
        "year_reasonable": check_year(literature["year"]),
        "content_match": check_content(literature),
    }

    confidence = sum(checks.values()) / len(checks)

    return {
        "is_valid": confidence >= 0.7,
        "confidence": confidence,
        "verification_details": checks,
        "warnings": [k for k, v in checks.items() if not v]
    }
```

#### 2.1.3 智能关键词生成

```python
# 新增：关键词生成策略
def generate_search_keywords(problem_type, problem_content):
    """
    根据问题类型生成搜索关键词
    """
    keyword_templates = {
        "评价类": [
            "{对象} + 评价模型",
            "{指标} + TOPSIS/AHP/熵权法",
            "{领域} + 综合评价",
        ],
        "预测类": [
            "{对象} + 预测模型",
            "{方法} + {应用领域}",
            "时间序列 + {数据类型}",
        ],
        "优化类": [
            "{问题} + 优化算法",
            "{约束} + 目标规划",
            "遗传算法/粒子群 + {应用场景}",
        ],
        "聚类类": [
            "{数据类型} + 聚类分析",
            "K-means/DBSCAN + {应用}",
            "{领域} + 分类模型",
        ],
    }

    # 生成3-5个关键词组合
    keywords = []
    for template in keyword_templates.get(problem_type, []):
        keywords.append(template.format(**problem_content))

    return keywords[:5]  # 限制数量，避免过多
```

### 2.2 图表系统优化

#### 2.2.1 自动布局调整

```python
# 新增：智能图表布局
def auto_adjust_layout(fig, ax, legend_position="auto"):
    """
    自动调整图表布局，避免重叠
    """
    # 检测重叠
    if check_overlap(ax):
        # 自动调整图例位置
        if legend_position == "auto":
            best_position = find_best_legend_position(ax)
            ax.legend(loc=best_position, bbox_to_anchor=(1.05, 1))

        # 调整子图间距
        plt.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.1)

    # 使用tight_layout
    plt.tight_layout()

    return fig
```

#### 2.2.2 中文自动检测与设置

```python
# 新增：语言检测与字体设置
def setup_font_by_language(text, language="auto"):
    """
    根据语言自动设置字体
    """
    if language == "auto":
        language = detect_language(text)

    if language == "chinese":
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    elif language == "english":
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']

    return language
```

#### 2.2.3 统一导出规范

```python
# 新增：图表导出规范
EXPORT_CONFIG = {
    "formats": ["svg", "pdf", "png"],  # 矢量+位图
    "dpi": 600,  # 高分辨率
    "bbox_inches": "tight",
    "transparent": False,
    "style": {
        "font.size": 7,
        "font.family": "sans-serif",
        "axes.linewidth": 0.8,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "legend.frameon": False,
    }
}
```

### 2.3 代码风格优化

#### 2.3.1 AIGC率降低策略

```python
# 新增：代码风格转换
def convert_to_human_style(code):
    """
    将AI风格代码转换为人类风格
    """
    transformations = [
        # 1. 简化变量名
        ("population_elderly_self_care", "n_self"),
        ("transition_probability_matrix", "P_trans"),
        ("service_station_location_optimization_model", "loc_opt"),

        # 2. 简化注释
        (r'""".*?"""', ''),  # 删除多行注释
        (r'# TODO.*', ''),  # 删除TODO

        # 3. 改变编码习惯
        (range(len(x)), enumerate(x)),  # 使用enumerate
        (if condition: return True else: return False, return condition),  # 简化返回
    ]

    for old, new in transformations:
        code = code.replace(old, new)

    return code
```

#### 2.3.2 变量名简化工具

```python
# 新增：变量名简化
VARIABLE_SHORTCUTS = {
    "population": "pop",
    "probability": "prob",
    "transition": "trans",
    "optimization": "opt",
    "algorithm": "algo",
    "parameter": "param",
    "temperature": "temp",
    "distance": "dist",
    "satisfaction": "sat",
    "coverage": "cov",
}

def simplify_variable_name(name):
    """简化变量名"""
    for full, short in VARIABLE_SHORTCUTS.items():
        name = name.replace(full, short)
    return name
```

#### 2.3.3 Unicode编码铁律

```python
# 新增：Unicode字符替换
UNICODE_REPLACEMENTS = {
    "²": "**2",
    "→": "->",
    "≥": ">=",
    "≤": "<=",
    "±": "+/-",
    "×": "*",
    "÷": "/",
    "≈": "~=",
    "≠": "!=",
    "∞": "inf",
    "√": "sqrt",
}

def replace_unicode_chars(text):
    """替换Unicode字符"""
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text
```

### 2.4 论文格式规范化

#### 2.4.1 标题编号系统

```python
# 新增：标题编号规范
def format_section_title(level, number, title):
    """
    格式化标题编号
    level: 1=一级, 2=二级, 3=三级
    """
    formats = {
        1: f"{'一二三四五六七八九十'[number-1]}、{title}",  # 中文数字
        2: f"{number}.{title}",  # 阿拉伯数字
        3: f"{number}.{title}",  # 小数点
    }
    return formats.get(level, title)
```

#### 2.4.2 支撑材料清单

```python
# 新增：支撑材料验证
SUPPORT_MATERIAL_CHECKLIST = {
    "必选": [
        "所有可运行源程序（.py/.m文件）",
        "自主查阅的数据资料（非赛题原始数据）",
        "较大篇幅中间结果的图表",
        "文献资料（PDF或链接）",
    ],
    "可选": [
        "模型推导过程详细文档",
        "算法伪代码",
        "数据预处理说明",
    ],
    "打包要求": [
        "使用WinRAR压缩",
        "后缀为RAR或ZIP",
        "大小不超过20MB",
        "文件命名清晰",
    ]
}
```

#### 2.4.3 附录代码插入

```python
# 新增：代码插入验证
def verify_code_insertion(tex_file, code_file):
    """
    验证代码是否完整插入
    """
    with open(code_file, 'r', encoding='utf-8') as f:
        code_lines = f.readlines()

    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # 检查代码是否在lstlisting环境中
    if '\\begin{lstlisting}' not in tex_content:
        return False, "未找到代码环境"

    # 检查代码行数
    code_in_tex = extract_code_from_tex(tex_content)
    if len(code_in_tex) < len(code_lines) * 0.9:  # 允许10%误差
        return False, f"代码不完整：{len(code_in_tex)}/{len(code_lines)}行"

    return True, "代码完整"
```

### 2.5 模型逻辑增强

#### 2.5.1 不确定性分析

```python
# 新增：蒙特卡洛模拟
def monte_carlo_simulation(model, params, n_simulations=1000):
    """
    增加不确定性分析
    """
    results = []
    for _ in range(n_simulations):
        # 随机扰动参数
        perturbed_params = {
            k: np.random.normal(v, v * 0.1)  # 10%扰动
            for k, v in params.items()
        }

        # 运行模型
        result = model(**perturbed_params)
        results.append(result)

    return {
        "mean": np.mean(results),
        "std": np.std(results),
        "ci_95": np.percentile(results, [2.5, 97.5]),
        "distribution": results
    }
```

#### 2.5.2 多目标优化

```python
# 新增：多目标优化框架
def multi_objective_optimization(objectives, constraints, variables):
    """
    多目标优化
    """
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.optimize import minimize

    # 定义问题
    problem = CustomProblem(objectives, constraints, variables)

    # 选择算法
    algorithm = NSGA2(pop_size=100)

    # 运行优化
    res = minimize(problem, algorithm, ('n_gen', 200))

    return res
```

#### 2.5.3 社会效益指标

```python
# 新增：社会效益评估
def social_benefit_score(results, weights=None):
    """
    评估社会效益
    """
    if weights is None:
        weights = {
            "coverage": 0.3,  # 覆盖率
            "satisfaction": 0.3,  # 满意度
            "equity": 0.2,  # 公平性
            "accessibility": 0.2,  # 可及性
        }

    score = sum(
        results[k] * v
        for k, v in weights.items()
        if k in results
    )

    return score
```

---

## 三、新增功能模块

### 3.1 文献管理模块

**功能**：
- 自动搜索真实文献
- 验证文献信息
- 生成引用格式
- 管理文献库

**文件位置**：`algorithms/literature/`

```
algorithms/literature/
├── __init__.py
├── search.py          # 文献搜索
├── verify.py          # 文献验证
├── citation.py        # 引用生成
└── manager.py         # 文献管理
```

### 3.2 图表工具模块

**功能**：
- 自动布局调整
- 中文支持
- 统一导出
- 图表验证

**文件位置**：`algorithms/plotting/`

```
algorithms/plotting/
├── __init__.py
├── layout.py          # 布局调整
├── font.py            # 字体设置
├── export.py          # 导出工具
└── validation.py      # 图表验证
```

### 3.3 代码风格模块

**功能**：
- AIGC率降低
- 变量名简化
- 注释精简
- 编码规范

**文件位置**：`algorithms/code_style/`

```
algorithms/code_style/
├── __init__.py
├── humanize.py        # 人类风格转换
├── simplify.py        # 变量名简化
├── comments.py        # 注释处理
└── encoding.py        # 编码规范
```

### 3.4 论文规范模块

**功能**：
- 标题编号
- 格式验证
- 支撑材料检查
- 附录代码插入

**文件位置**：`algorithms/paper/`

```
algorithms/paper/
├── __init__.py
├── formatting.py      # 格式化
├── validation.py      # 验证
├── materials.py       # 支撑材料
└── appendix.py        # 附录处理
```

---

## 四、流程优化

### 4.1 文献检索流程（Step 4优化）

**原流程**：
```
1. 构建关键词
2. WebSearch搜索
3. 提取信息
4. 生成引用
```

**新流程**：
```
1. 智能关键词生成
   - 根据问题类型自动生成
   - 限制数量（3-5个）
   - 分级搜索策略

2. 多平台搜索
   - Level 1: API优先（CrossRef, Semantic Scholar）
   - Level 2: WebSearch备用
   - Level 3: 手动搜索兜底

3. 文献验证（强制）
   - 验证作者真实性
   - 验证期刊存在性
   - 验证DOI有效性
   - 验证年份合理性

4. 信息提取
   - 核心方法
   - 创新点
   - 不足之处
   - 可借鉴之处

5. 引用生成
   - 按比赛要求格式
   - 自动生成引用列表
   - 验证引用完整性
```

### 4.2 图表生成流程（Step 7优化）

**原流程**：
```
1. 编写绘图代码
2. 运行生成图表
3. 插入论文
```

**新流程**：
```
1. 绘图准备
   - 检测语言（中文/英文）
   - 设置字体
   - 配置导出参数

2. 图表生成
   - 自动布局调整
   - 避免重叠
   - 统一配色

3. 图表验证
   - 检查图例位置
   - 检查标注完整性
   - 检查分辨率

4. 导出处理
   - SVG（矢量）
   - PDF（高质量）
   - PNG（备用）

5. 插入验证
   - 检查引用正确性
   - 检查图表完整性
   - 检查编号连续性
```

### 4.3 代码处理流程（Step 7优化）

**原流程**：
```
1. 编写代码
2. 运行测试
3. 生成结果
```

**新流程**：
```
1. 代码编写
   - 使用算法库
   - 遵循Unicode铁律
   - 添加必要注释

2. 风格优化
   - 变量名简化
   - 注释精简
   - 去除AI痕迹

3. 编码检查
   - 替换Unicode字符
   - 确保GBK兼容
   - 验证可运行性

4. 结果生成
   - 运行代码
   - 生成图表
   - 导出JSON结果

5. 代码整理
   - 模块化组织
   - 添加使用说明
   - 准备附录插入
```

### 4.4 论文撰写流程（Step 8优化）

**原流程**：
```
1. 撰写内容
2. 插入图表
3. 添加引用
```

**新流程**：
```
1. 结构规划
   - 按问题分节
   - 确定标题编号
   - 规划章节顺序

2. 内容撰写
   - 问题重述
   - 模型建立
   - 求解过程
   - 结果分析

3. 格式规范
   - 标题编号统一
   - 图表引用正确
   - 公式编号连续

4. 引用标注
   - 模型来源
   - 方法来源
   - 数据来源

5. 验证检查
   - 内容完整性
   - 格式规范性
   - 引用充分性
```

---

## 五、模板系统扩展

### 5.1 新增比赛模板

```
templates/
├── cumcm/             # 全国大学生数学建模
├── dianganbei/        # 电工杯
├── mathorcup/         # MathorCup
├── shumobei/          # 数模杯
├── fujianbei/         # 福建杯
├── hubeibei/          # 湖北杯
├── generic/           # 通用模板
└── README.md          # 模板使用说明
```

### 5.2 模板内容

每个比赛模板包含：
- `requirements.md` - 格式要求
- `preamble.tex` - LaTeX导言区
- `paper-template.tex` - 论文模板
- `references/` - 参考文献格式
- `examples/` - 示例论文

### 5.3 模板自动检测

```python
def detect_competition(user_input):
    """
    根据用户输入检测比赛类型
    """
    keywords = {
        "电工杯": ["电工", "电气", "电力"],
        "全国赛": ["全国", "高教社", "CUMCM"],
        "MathorCup": ["mathorcup", "MathorCup"],
        "数模杯": ["数模", "数学建模"],
    }

    for comp, kws in keywords.items():
        if any(kw in user_input for kw in kws):
            return comp

    return "generic"
```

---

## 六、知识库扩展

### 6.1 新增知识文件

```
knowledge/
├── models/
│   ├── evaluation.md      # 评价模型详解
│   ├── prediction.md      # 预测模型详解
│   ├── optimization.md    # 优化模型详解
│   ├── clustering.md      # 聚类模型详解
│   └── statistics.md      # 统计模型详解
├── algorithms/
│   ├── genetic_algorithm.md  # 遗传算法详解
│   ├── particle_swarm.md     # 粒子群算法详解
│   ├── simulated_annealing.md # 模拟退火详解
│   └── neural_network.md     # 神经网络详解
├── applications/
│   ├── facility_location.md  # 设施选址
│   ├── resource_allocation.md # 资源分配
│   ├── path_planning.md      # 路径规划
│   └── scheduling.md         # 调度问题
└── competitions/
    ├── common_requirements.md  # 通用要求
    ├── scoring_criteria.md     # 评分标准
    └── submission_guidelines.md # 提交指南
```

### 6.2 知识库内容

每个知识文件包含：
- 模型/算法原理
- 适用场景
- 优缺点分析
- 实现代码示例
- 参考文献

### 6.3 知识检索机制

```python
def search_knowledge(problem_type, keywords):
    """
    搜索知识库
    """
    knowledge_dir = Path("~/.claude/skills/math-model/knowledge")

    # 按问题类型搜索
    type_files = knowledge_dir / "models" / f"{problem_type}.md"
    if type_files.exists():
        return read_knowledge(type_files)

    # 按关键词搜索
    for file in knowledge_dir.rglob("*.md"):
        content = file.read_text()
        if any(kw in content for kw in keywords):
            return read_knowledge(file)

    return None
```

---

## 七、验证系统增强

### 7.1 证据门控增强

**原系统**：
- 检查模型结果
- 检查评价指标
- 检查输出图表
- 检查结论文字

**增强后**：
- 检查模型结果
- 检查评价指标
- 检查输出图表
- 检查结论文字
- **检查文献引用**（新增）
- **检查代码完整性**（新增）
- **检查格式规范性**（新增）
- **检查支撑材料**（新增）

### 7.2 质量评分系统

```python
def calculate_quality_score(paper):
    """
    论文质量评分
    """
    scores = {
        "content": {
            "weight": 0.4,
            "criteria": [
                "问题分析完整性",
                "模型选择合理性",
                "求解过程正确性",
                "结果分析深度",
            ]
        },
        "format": {
            "weight": 0.2,
            "criteria": [
                "标题编号规范",
                "图表格式统一",
                "公式编号连续",
                "引用格式正确",
            ]
        },
        "literature": {
            "weight": 0.2,
            "criteria": [
                "文献数量充分",
                "文献质量高",
                "引用关系清晰",
                "来源真实可靠",
            ]
        },
        "code": {
            "weight": 0.2,
            "criteria": [
                "代码可运行",
                "结果可复现",
                "注释清晰",
                "风格规范",
            ]
        }
    }

    total_score = 0
    for category, config in scores.items():
        category_score = evaluate_category(paper, category, config["criteria"])
        total_score += category_score * config["weight"]

    return total_score
```

### 7.3 最终验证清单

```python
FINAL_VERIFICATION_CHECKLIST = {
    "内容完整性": [
        "所有问题都已回答",
        "每个问题都有模型建立",
        "每个问题都有求解过程",
        "每个问题都有结果分析",
    ],
    "格式规范性": [
        "标题编号统一",
        "图表引用正确",
        "公式编号连续",
        "参考文献格式正确",
    ],
    "文献充分性": [
        "文献数量≥15篇",
        "文献来源真实",
        "引用关系清晰",
        "覆盖主要方法",
    ],
    "代码完整性": [
        "代码可运行",
        "结果可复现",
        "附录代码完整",
        "支撑材料齐全",
    ],
    "模型合理性": [
        "模型选择有依据",
        "假设条件合理",
        "求解过程正确",
        "结果分析深入",
    ]
}
```

---

## 八、实施计划

### 8.1 第一阶段：文献系统（1周）

- [ ] 实现多平台搜索
- [ ] 实现文献验证
- [ ] 实现智能关键词生成
- [ ] 测试并优化

### 8.2 第二阶段：图表系统（1周）

- [ ] 实现自动布局调整
- [ ] 实现中文支持
- [ ] 实现统一导出
- [ ] 测试并优化

### 8.3 第三阶段：代码系统（1周）

- [ ] 实现AIGC率降低
- [ ] 实现变量名简化
- [ ] 实现编码规范
- [ ] 测试并优化

### 8.4 第四阶段：论文系统（1周）

- [ ] 实现标题编号
- [ ] 实现格式验证
- [ ] 实现支撑材料检查
- [ ] 测试并优化

### 8.5 第五阶段：知识库（1周）

- [ ] 编写模型知识库
- [ ] 编写算法知识库
- [ ] 编写应用知识库
- [ ] 编写比赛知识库

### 8.6 第六阶段：验证系统（1周）

- [ ] 增强证据门控
- [ ] 实现质量评分
- [ ] 实现最终验证
- [ ] 测试并优化

---

## 九、预期效果

### 9.1 文献质量提升

- **真实率**：从30%提升到95%以上
- **搜索效率**：从手动搜索1小时降低到自动搜索5分钟
- **验证准确率**：从0%提升到90%以上

### 9.2 图表质量提升

- **重叠问题**：从50%降低到5%以下
- **中文支持**：从60%提升到100%
- **分辨率**：从72dpi提升到600dpi

### 9.3 代码质量提升

- **AIGC检测率**：从80%降低到20%以下
- **可运行率**：从70%提升到95%以上
- **规范性**：从50%提升到90%以上

### 9.4 论文质量提升

- **格式规范性**：从60%提升到95%以上
- **内容完整性**：从70%提升到95%以上
- **评分预期**：从二等奖提升到一等奖水平

---

## 十、总结

本优化方案针对电工杯项目中发现的所有问题，提出了系统性的解决方案：

1. **文献系统**：多平台搜索+强制验证，解决AI幻觉问题
2. **图表系统**：自动布局+中文支持，解决重叠和标注问题
3. **代码系统**：风格转换+编码规范，解决AIGC率和兼容性问题
4. **论文系统**：格式规范+验证机制，解决编号和完整性问题
5. **知识库**：扩展内容+智能检索，解决模型选择问题
6. **验证系统**：增强门控+质量评分，解决质量保证问题

通过这些优化，math-model skill将能够：
- 处理各种类型的数学建模比赛
- 生成高质量的论文和代码
- 避免常见的错误和问题
- 提升整体竞赛水平

**文档版本**：v1.0
**创建日期**：2026年5月29日
**适用范围**：所有数学建模竞赛
