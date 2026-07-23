---
name: math-model
description: 数学建模竞赛全流程工作流。当用户要求数模解题、分析赛题、生成数模论文、调用 /math-model 时使用。自动执行：审题→文献检索→选模型→写代码→写论文→润色，每步暂停等用户确认。
---

# 数学建模竞赛全流程 Agent

## 概述

本 skill 实现数学建模竞赛的全流程辅助解题。每一步完成后暂停，展示结果，等用户确认后再进入下一步。用户可随时说"回到第X步"重新调整。

## Agent 架构

本工作流采用 **编排器 + 独立 Agent** 架构，避免上下文污染：

```
编排器（本文件）
  ├── Step 0-3, 6, 8, 8.5: 编排器自身处理
  └── Step 4, 5, 7, 7.2, 10, 11: 调用独立 Agent
        ├── literature-searcher  ← 文献检索（含 CNKI/arXiv）
        ├── brainstormer         ← 创新探索
        ├── coder                ← 代码求解 + 绘图 + draw.io 流程图
        ├── polisher             ← 学术润色
        └── verifier             ← 最终验证
```

每个 Agent 有独立的上下文窗口，内嵌完整规则，不会污染编排器。

## Agent 调用协议

### Schema 验证

每个 Agent 的输入输出都有 JSON Schema 约束，定义在 `schemas/` 目录：

| Agent | 输入 Schema | 输出 Schema |
|-------|------------|------------|
| literature-searcher | `schemas/literature-input.json` | `schemas/literature-output.json` |
| brainstormer | `schemas/brainstorm-input.json` | `schemas/brainstorm-output.json` |
| coder | `schemas/coder-input.json` | `schemas/coder-output.json` |
| polisher | `schemas/polisher-input.json` | `schemas/polisher-output.json` |
| verifier | `schemas/verifier-input.json` | `schemas/verifier-output.json` |

**调用流程**：
1. 构造输入 JSON
2. **验证输入符合 input schema**（检查 required 字段和类型）
3. 调用 Agent
4. 接收返回 JSON
5. **验证返回符合 output schema**（检查 required 字段和类型）
6. 不符合 → 要求 Agent 重新返回（最多 2 次）
7. 符合 → 继续

### 错误重试机制

```
Agent 调用流程：
  第 1 次调用
    ↓ 失败/返回格式错误
  等 3 秒，第 2 次调用
    ↓ 失败
  展示错误信息给用户，让用户选择：
    A. 重试
    B. 跳过这步（手动提供结果）
    C. 退出
```

**具体错误处理**：

| 错误类型 | 处理方式 |
|---------|---------|
| Agent 返回格式错误 | 要求重新生成（提示 schema 要求） |
| Agent 超时 | 重试 1 次，还不行 → 暂停等用户 |
| Edge 浏览器断开 | 提示用户重新启动 Edge 并登录 |
| CNKI 搜索无结果 | 降级到 WebSearch / 手动搜索 |
| 代码运行报错 | Agent 自动调试（最多 3 次） |

### 文件所有权

```
编排器拥有:  output/paper.tex, output/preamble.tex
coder 拥有:  output/code.py, output/figures/, output/diagrams/
polisher:    读取 paper.tex → 润色 → 输出 paper_polished.tex（不直接改原文件）
verifier:    只读验证，不修改任何文件
```

**polisher 文件处理**：
1. polisher 读取 `output/paper.tex`
2. 润色后输出到 `output/paper_polished.tex`
3. 编排器展示差异对比
4. 用户确认后才覆盖原文件
5. 原文件备份为 `output/paper_before_polish.tex`

## 工作流总览

```
Step 0:   接收比赛信息与论文格式要求          [编排器]
Step 1:   生成 LaTeX 模板框架                 [编排器]
Step 2:   接收赛题                            [编排器]
Step 3:   审题拆解                            [编排器]
Step 4:   文献检索（前人解法调研）            [literature-searcher agent]
Step 5:   创新探索与模型设计                  [brainstormer agent]
Step 6:   撰写模型大纲                        [编排器]
Step 7:   代码求解                            [coder agent]
Step 7.2: 生成流程图（draw.io）               [coder agent]
Step 7.5: 证据门控                            [编排器验证]
Step 8:   论文撰写                            [编排器]
Step 8.5: 插入附录代码                        [编排器]
Step 9:   文献标注                            [编排器]
Step 10:  学术润色                            [polisher agent]
Step 11:  收尾输出                            [verifier agent]
```

---

## 确认机制

每步完成后：
1. 展示该步的输出结果
2. 询问："以上是本步结果，确认无误进入下一步？还是需要修改？"
3. 用户确认后进入下一步；用户提出修改则调整后重新展示
4. 用户可随时说"回到第X步"跳转

## LaTeX 编译策略（重要）

只在以下节点编译 LaTeX，其余步骤只修改源码不编译：

| 步骤 | 是否编译 | 原因 |
|------|---------|------|
| Step 1（模板框架） | ✅ 编译 | 检查排版布局和章节大纲结构 |
| Step 6（模型大纲） | ✅ 编译 | 检查公式排版是否正确 |
| Step 7.5（证据门控） | ❌ 不编译 | 验证结果文件，不涉及 .tex |
| Step 8（论文撰写） | ✅ 编译 | 插完图后检查图表渲染效果 |
| Step 8.5（附录代码） | ❌ 不编译 | 纯文本插入，无排版风险 |
| Step 9（文献标注） | ❌ 不编译 | 纯文字修改，无排版风险 |
| Step 10（学术润色） | ❌ 不编译 | 纯文字修改，无排版风险 |
| Step 11（收尾输出） | ✅ 编译 | 最终正式编译（两次 xelatex） |

每次编译只需 `xelatex paper.tex` 一次（除 Step 11 需两次以生成目录/交叉引用）。

---

## Step 0: 接收比赛信息与论文格式要求

**目标**：确定比赛类型，获取并解析论文格式要求。

**执行**：
1. 询问用户参加哪个比赛
2. 检查 `E:/Ai_configs/.claude/skills/math-model/templates/` 目录下是否有对应预存模板：
   - 有 → 读取 `requirements.md`，展示格式要求，用户确认即可
   - 没有 → 进入第3步
3. **接收用户提供的论文格式要求**（以下任一方式）：
   - Word 文件（.docx）：用 python-docx 提取
   - PDF 文件：用 Read 工具读取
   - 文本粘贴：直接在对话中提供
4. **解析格式要求**，提取关键信息：
   - 语言（中文/英文）
   - 页数限制
   - 字体字号要求（正文、标题、摘要）
   - 论文结构要求（必须包含哪些章节）
   - 图表格式要求（编号方式、标题位置）
   - 引用格式要求（GB/T 7714、APA、IEEE 等）
   - 提交格式（PDF/Word）
   - 其他特殊要求（查重率、代码要求等）
5. **自动建档**：将解析结果保存为 `E:/Ai_configs/.claude/skills/math-model/templates/{比赛名}/requirements.md`，下次直接复用
6. **确定引用格式**（不同比赛要求不同）：
   - 默认使用 `gbt7714` 国标格式（大多数比赛通用）
   - 如比赛有特殊格式要求，按要求调整

**输出**：确认比赛名称、关键格式要求（页数、字体、提交格式等）、引用格式。

---

## Step 1: 生成 LaTeX 模板框架

**目标**：根据 Step 0 的格式要求，生成完整的 .tex 骨架文件。

**执行**：
1. 检查 `E:/Ai_configs/.claude/skills/math-model/templates/{比赛名}/` 是否有预存的 `preamble.tex` 和 `paper-template.tex`：
   - **有预存模板**：读取并使用
   - **无预存模板**：根据 Step 0 解析的格式要求**从零生成**：
     - `preamble.tex`：根据语言/字体/引用格式生成导言区
     - `paper-template.tex`：根据章节结构要求生成论文骨架
     - **保存到** `E:/Ai_configs/.claude/skills/math-model/templates/{比赛名}/` 目录，供以后复用
2. 在当前工作目录创建 `output/` 文件夹
3. 将模板复制到 `output/paper.tex` 和 `output/preamble.tex`
4. 根据比赛要求预填标题页格式（题目留空待填）
5. 确保所有章节结构完整
6. **编译验证**：`cd output && xelatex paper.tex`，检查排版布局

**输出**：
- `output/paper.tex` — 完整的 LaTeX 骨架
- `output/preamble.tex` — 导言区
- 展示论文结构大纲供用户确认

---

## Step 2: 接收赛题

**目标**：获取并理解赛题内容。

**执行**：
1. 用户提供赛题（文本、Word (.docx)、PDF 文件、或图片）
2. **Word 文档读取**：
   - 使用 python-docx 提取
   - **保留原始表格结构**：赛题中的数据表格必须完整提取
   - 如果 docx 中有图片，提取到 `output/problem_images/` 目录
3. **PDF 文档读取**：
   - 用 Read 工具逐段提取原文
   - 确保表格、公式、图片完整保留
4. 如果是纯文本或图片，使用 Read 工具读取或识别图片文字
5. 完整保存赛题原文，**特别标注所有数据表格和约束条件**

**输出**：展示赛题原文（含表格），确认读取无误。

---

## Step 3: 审题拆解

**目标**：分析赛题，识别问题数量、类型和核心考点。

**执行**：
1. 仔细阅读赛题，识别：
   - 题目背景和约束条件
   - 需要解决的子问题数量
   - 每个子问题的类型（评价/预测/优化/分类/统计/图论/微分方程/博弈）
   - 核心考点和难点
   - 提供的数据类型和规模
2. 分析各子问题之间的关联
3. 生成解题路线图

**输出**：
```
## 审题分析

### 题目背景
{背景概述}

### 子问题拆解
1. **问题一**：{描述} — 类型：{评价/预测/优化/...}
2. **问题二**：{描述} — 类型：{评价/预测/优化/...}

### 核心考点
- {考点1}
- {考点2}

### 解题路线图
1. 数据预处理 → 2. 问题一求解 → 3. 问题二求解 → ...

### 评分对齐表
| 子问题 | 预期得分点 | 对应论文章节 | 需要的证据 |
|--------|-----------|-------------|-----------|
| 问题一 | 模型选择合理 | 3.1 模型建立 | 前人对比分析 |
| 问题一 | 求解结果正确 | 3.3 求解与结果 | 数值结果+图表 |
```

---

## Step 4: 文献检索（前人解法调研）

**目标**：检索前人在类似问题上用了什么模型、效果如何，为 Step 5 的创新探索提供基础。

**调用 Agent**：

```
调用 literature-searcher agent
传入 JSON:
{
  "problem_analysis": {Step 3 的审题分析结果},
  "competition_name": "比赛名称",
  "citation_format": "gbt7714"
}

接收 JSON:
{
  "papers": [...],
  "summary": {...},
  "common_approaches": [...],
  "references_bibtex": "..."
}
```

**Agent 自动执行**：
1. 通过 Edge 浏览器 + 学校图书馆搜索 CNKI 中文文献
2. 通过 arXiv API 搜索英文文献
3. 通过 CrossRef/Semantic Scholar 补充 DOI 和摘要
4. 验证每篇文献的真实性
5. 扫描知识库 `E:\Studydata\07-数学建模\knowledge\`
6. 返回结构化结果

**前置条件**（需要用户操作）：
1. 运行 `E:/Ai_configs/edge-browser/start_edge_debug.bat` 启动 Edge
2. 在 Edge 中登录学校图书馆 https://ncu.metaersp.cn/personalIndex

**Schema 验证**：接收结果后验证是否符合 `schemas/literature-output.json`，不符合则要求重新返回。

**输出**：展示前人解法调研结果（含验证状态），用户确认后进入下一步。

---

## Step 5: 创新探索与模型设计

**目标**：基于 Step 4 的前人解法，brainstorm 创新方向，确定最终模型方案。

**调用 Agent**：

```
调用 brainstormer agent
传入 JSON:
{
  "problem_analysis": {Step 3 的审题分析},
  "literature": {Step 4 的文献调研结果}
}

接收 JSON:
{
  "recommended_plan": {...},
  "alternative_plans": [...],
  "innovation_check": {...}
}
```

**Agent 自动执行**：
1. 分析前人方法的核心缺陷
2. 提出 2-3 个创新方案
3. 每个方案说明数学依据
4. 创新深度检查（至少 1 个算法层面改进）
5. 给出推荐理由

**Schema 验证**：接收结果后验证是否符合 `schemas/brainstorm-output.json`，不符合则要求重新返回。

**输出**：展示创新方案对比，用户选择后确定最终方案。

---

## Step 6: 撰写模型大纲

**目标**：编写数学模型的详细推导和公式逻辑，填入 LaTeX 框架。

**执行**：
1. 对每个子问题的模型，编写：
   - 模型的数学定义
   - 目标函数和约束条件
   - 公式推导过程
   - 求解思路
2. 将公式用 LaTeX 格式写入 `output/paper.tex` 的对应章节
3. 确保公式编号连续、符号一致
4. **完成后编译一次**：`cd output && xelatex paper.tex`，检查公式排版

**LaTeX 公式规范**：
- 行内公式：`$...$`
- 行间公式：`\begin{equation}...\end{equation}`
- 向量用粗体：`\vect{x}`
- 矩阵用粗体：`\mat{A}`
- 微分d用正体：`\diff`

**输出**：更新后的 `output/paper.tex`（模型建立章节已填入公式）。

---

## Step 7: 代码求解

**目标**：编写并运行 Python 代码，求解模型并生成图表。

**调用 Agent**：

```
调用 coder agent
传入 JSON:
{
  "sub_problems": [
    {
      "id": 1,
      "model": "模型名",
      "parameters": {},
      "data_path": "数据文件路径",
      "expected_output": "预期结果描述"
    }
  ],
  "algorithm_library_path": "E:/Ai_configs/.claude/skills/math-model/algorithms/",
  "output_dir": "output/"
}

接收 JSON:
{
  "results": [
    {
      "problem_id": 1,
      "model": "模型名",
      "metrics": {"RMSE": 0.03, "R2": 0.97},
      "figures": ["output/figures/fig_q1_pred.png"],
      "conclusion": "一句话结论",
      "code_path": "output/code.py"
    }
  ],
  "code_quality": {...},
  "figure_quality": {...}
}
```

**Agent 自动执行**：
1. 根据模型大纲编写 Python 代码
2. 调用 `E:/Ai_configs/.claude/skills/math-model/algorithms/` 下的已有工具
3. 运行代码，生成图表（SVG + PDF + PNG，600dpi）
4. 代码报错时自动调试（四阶段流程）
5. 生成 `output/results_summary.json`

**Schema 验证**：接收结果后验证是否符合 `schemas/coder-output.json`，不符合则要求重新返回。

**输出**：代码运行结果、图表预览、质量检查报告。

---

## Step 7.2: 生成流程图（draw.io）

**目标**：生成解题流程图和算法流程图，用于论文和答辩。

**调用 Agent**：

```
调用 coder agent（复用，不需要额外调用）
传入 JSON:
{
  "task": "generate_diagrams",
  "problem_analysis": {Step 3 的审题分析},
  "model_plan": {Step 5 的创新方案},
  "output_dir": "output/diagrams/"
}
```

**Agent 自动生成**：
1. `output/diagrams/problem_flow.drawio` — 解题流程图
2. `output/diagrams/algorithm_flow.drawio` — 算法流程图
3. `output/diagrams/data_flow.drawio` — 数据处理流程
4. `output/diagrams/model_architecture.drawio` — 模型架构图

**使用方式**：
- VS Code：安装 `hediet.vscode-drawio` 插件，双击 .drawio 文件打开
- 网页版：https://app.diagrams.net/ 打开
- 桌面版：https://github.com/jgraph/drawio-desktop/releases

**输出**：展示流程图预览，用户确认后继续。

---

## Step 7.5: 证据门控（Evidence Gate）

**目标**：强制验证每个子问题的求解证据齐全，未通过则不允许进入论文写作。

**执行**：
1. 读取 `output/results_summary.json`
2. 对每个子问题逐项检查：
   - [ ] 有真实的模型结果（非占位符）
   - [ ] 有至少一个评价指标（RMSE / R² / 准确率等）
   - [ ] 有至少一张输出图表（`output/figures/` 下存在对应文件）
   - [ ] 有明确的结论文字
   - [ ] 图表质量检查（无重叠、中文正确、≥600dpi、格式齐全）
   - [ ] 代码质量检查（可运行、无Unicode、变量名已简化）
3. 如果任一子问题未通过：
   - 列出具体缺失项
   - **阻断流程**，要求返回 Step 7 补充求解
4. 全部通过后，展示验证结果表

**输出**：证据门控验证结果表。

---

## Step 8: 论文撰写

**目标**：将模型、代码、图表填入 LaTeX 框架，撰写完整论文。

**执行**：
1. **标题编号规范**：
   - 一级标题：中文数字 + 顿号（一、二、三、）
   - 二级标题：阿拉伯数字 + 小数点（1.1, 1.2）
   - 三级标题：阿拉伯数字 + 小数点（1.1.1, 1.1.2）
   - 禁止混用

2. 按照论文固定结构，逐章节撰写：
   - 问题重述与分析
   - 模型假设与符号说明
   - 问题一：模型建立与求解（一问一答自成一体）
   - 问题二：模型建立与求解
   - ...
   - 模型优缺点与推广
   - 结论
   - 参考文献
   - 附录（留空，Step 8.5 插入）

   **⚠️ 论文结构铁律**：每问独立一节，禁止按内容类型分章。

3. 所有内容写入 `output/paper.tex`
4. **完成后编译一次**：`cd output && xelatex paper.tex`

**输出**：完整的 `output/paper.tex`（附录除外）。

---

## Step 8.5: 插入附录代码与支撑材料

**目标**：将求解代码完整插入论文附录。

**执行**：
1. 读取 `output/code.py` 的完整内容
2. 在 `output/paper.tex` 的 `\section{附录}` 章节中插入代码
3. 验证插入的代码完整性（行数一致、不截断）
4. 准备支撑材料目录结构
5. **此步不编译 LaTeX**

**输出**：更新后的 `output/paper.tex`（附录已插入完整代码）。

---

## Step 9: 文献标注

**目标**：标注每处引用的来源文献。确保引用数量 ≥ 15 条。

**执行**：
1. 检查论文中所有引用位置
2. 对每处需要引用的段落，补充 `\cite{ref}` 格式标注
3. 在参考文献列表中补充完整的文献信息
4. **引用数量检查**：统计参考文献总数，必须 ≥ 15 条
5. **引用格式按 Step 0 确定的格式执行**（默认 gbt7714）
6. **此步不编译 LaTeX**

**输出**：更新后的参考文献列表（≥ 15 条）。

---

## Step 10: 学术润色

**目标**：对全文进行学术化润色。**润色 ≠ 换词，润色 = 用专业学术语言详尽扩充**。

**调用 Agent**：

```
调用 polisher agent
传入 JSON:
{
  "paper_path": "output/paper.tex",
  "sections_to_polish": [
    {
      "section": "3.1 问题一模型建立",
      "content": "当前内容",
      "needs_expansion": true
    }
  ],
  "language": "chinese",
  "competition_style": "cumcm"
}

接收 JSON:
{
  "polished_paper_path": "output/paper.tex",
  "changes": [...],
  "quality_check": {...}
}
```

**Agent 自动执行**：
1. 读取 `output/paper.tex` 全文
2. 按写作策略润色（沙漏结构、claim-evidence-boundary）
3. 扩充模型推导、算法原理、结果分析
4. 去口语化、去 AI 痕迹
5. 每节篇幅增加 30%-50%
6. **输出到 `output/paper_polished.tex`**（不直接改原文件）
7. **此步不编译 LaTeX**

**编排器处理**：
1. 备份原文件：`cp output/paper.tex output/paper_before_polish.tex`
2. 展示润色前后对比（关键章节）
3. 用户确认后覆盖：`cp output/paper_polished.tex output/paper.tex`
4. 如果用户不满意，可以要求重新润色或手动修改

**输出**：润色后的论文，展示修改对比供用户审阅。

---

## Step 11: 收尾输出

**目标**：生成摘要，输出最终文件，进行最终验证。

**调用 Agent**：

```
调用 verifier agent
传入 JSON:
{
  "paper_path": "output/paper.tex",
  "code_path": "output/code.py",
  "figures_dir": "output/figures/",
  "results_summary": {},
  "references_count": 15
}

接收 JSON:
{
  "checks": {...},
  "scores": {...},
  "paper_stats": {...},
  "blocking_issues": [],
  "warnings": [...]
}
```

**Agent 自动执行**：
1. 逐项验证所有检查项
2. 实际运行验证命令（不信任 "应该没问题"）
3. 生成质量评分报告
4. 列出阻断问题和警告

**Schema 验证**：接收结果后验证是否符合 `schemas/verifier-output.json`，不符合则要求重新返回。

**编排器执行**：
1. **生成摘要**（最后写）：
   - 问题概述（1-2句）
   - 使用的方法和模型（2-3句）
   - 主要结果和结论（2-3句）
   - 写入论文标题页
2. **最终编译**：`cd output && xelatex paper.tex && xelatex paper.tex`（两次）
3. **展示汇总**：论文结构、页数、图表数量、代码行数

**输出**：
```
## 输出完成

### 文件清单
- output/paper.tex — 论文主文件
- output/preamble.tex — 导言区
- output/code.py — 求解代码
- output/figures/ — 图表文件夹
- output/diagrams/ — 流程图文件夹（.drawio）
- output/支撑材料_{参赛编号}/ — 支撑材料目录

### 编译方法
cd output && xelatex paper.tex && xelatex paper.tex

### 最终验证结果
{verifier agent 返回的质量报告}

### 论文统计
{页数、图表数、公式数、参考文献数、代码行数}
```

---

## 内置知识库

当 `E:/Ai_configs/.claude/skills/math-model/knowledge/` 目录为空或匹配度低时，使用以下内置知识：

### 经典模型速查

| 问题类型 | 常用模型 | 适用场景 |
|---------|---------|---------|
| 评价类 | TOPSIS、熵权法、层次分析法、灰色关联、模糊综合评价 | 多指标排序、方案评价 |
| 预测类 | 灰色预测、回归分析、ARIMA、神经网络、马尔可夫 | 趋势预测、数据拟合 |
| 优化类 | 线性规划、整数规划、遗传算法、模拟退火、粒子群 | 资源分配、路径规划 |
| 聚类类 | K-means、DBSCAN、层次聚类、高斯混合 | 数据分类、模式识别 |
| 统计类 | 因子分析、主成分分析、回归分析、方差分析 | 数据降维、因素分析 |
| 图论类 | Dijkstra、Floyd、最小生成树、网络流 | 路径规划、网络优化 |
| 微分方程 | 常微分方程、偏微分方程、差分方程 | 动态系统建模 |
| 博弈类 | 纳什均衡、博弈树、演化博弈 | 竞争决策分析 |

### 算法库目录

扫描 `E:/Ai_configs/.claude/skills/math-model/algorithms/` 获取可用工具：
- `evaluation/` — 评价类算法 .py
- `prediction/` — 预测类算法 .py
- `optimization/` — 优化类算法 .py
- `clustering/` — 聚类类算法 .py
- `plotting/` — 绘图工具 .py
