# Draw.io 模板集 — 数学建模常用图表

## 1. 解题流程图模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="problem-flow" name="解题流程图">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="start" value="接收赛题" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="420" y="30" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s1" value="审题拆解&#xa;识别问题类型" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="110" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s2" value="文献检索&#xa;调研前人解法" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="200" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s3" value="模型选择&#xa;确定建模方案" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="290" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s4" value="代码求解&#xa;Python 实现" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="380" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s5" value="结果分析&#xa;图表可视化" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="470" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s6" value="论文撰写&#xa;LaTeX 排版" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="420" y="560" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="end" value="提交论文" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="420" y="650" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="e1" edge="1" source="start" target="s1" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" source="s1" target="s2" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" source="s2" target="s3" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" source="s3" target="s4" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" source="s4" target="s5" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" source="s5" target="s6" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e7" edge="1" source="s6" target="end" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 2. 算法流程图模板（以 TOPSIS 为例）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="topsis-flow" name="TOPSIS 算法流程">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="start" value="开始" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="420" y="30" width="120" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="s1" value="构建决策矩阵&#xa;X = (x_ij)m*n" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="100" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s2" value="数据标准化&#xa;z_ij = x_ij / sqrt(sum(x_ij^2))" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="180" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s3" value="确定权重&#xa;熵权法/AHP" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="260" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s4" value="加权标准化矩阵&#xa;v_ij = w_j * z_ij" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="340" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s5" value="确定正负理想解&#xa;A+ = max, A- = min" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="420" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="s6" value="计算距离&#xa;D+ = dist(v, A+)&#xa;D- = dist(v, A-)" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="500" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="s7" value="相对接近度&#xa;C_i = D- / (D+ + D-)" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="400" y="590" width="160" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="end" value="排序输出" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="420" y="670" width="120" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="e1" edge="1" source="start" target="s1" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" source="s1" target="s2" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" source="s2" target="s3" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" source="s3" target="s4" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" source="s4" target="s5" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" source="s5" target="s6" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e7" edge="1" source="s6" target="s7" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e8" edge="1" source="s7" target="end" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 3. 模型架构图模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="model-arch" name="模型架构图">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 输入层 -->
        <mxCell id="input" value="输入数据" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="80" y="60" width="120" height="50" as="geometry"/>
        </mxCell>
        <!-- 预处理 -->
        <mxCell id="preprocess" value="数据预处理&#xa;缺失值/标准化" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="280" y="60" width="140" height="50" as="geometry"/>
        </mxCell>
        <!-- 模型1 -->
        <mxCell id="model1" value="模型一&#xa;评价模型" style="whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="480" y="20" width="120" height="50" as="geometry"/>
        </mxCell>
        <!-- 模型2 -->
        <mxCell id="model2" value="模型二&#xa;预测模型" style="whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="480" y="90" width="120" height="50" as="geometry"/>
        </mxCell>
        <!-- 结果 -->
        <mxCell id="result" value="结果分析" style="whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="660" y="60" width="120" height="50" as="geometry"/>
        </mxCell>
        <!-- 论文 -->
        <mxCell id="paper" value="论文输出" style="whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="840" y="60" width="120" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="e1" edge="1" source="input" target="preprocess" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" source="preprocess" target="model1" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" source="preprocess" target="model2" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" source="model1" target="result" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" source="model2" target="result" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" source="result" target="paper" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 4. 决策判断流程图模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="decision-flow" name="模型选择决策">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="start" value="问题类型?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="380" y="30" width="160" height="100" as="geometry"/>
        </mxCell>
        <mxCell id="eval" value="评价类&#xa;TOPSIS/AHP" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="180" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="pred" value="预测类&#xa;回归/灰色预测" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="300" y="180" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="opt" value="优化类&#xa;线性规划/GA" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="500" y="180" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="cluster" value="聚类类&#xa;K-means/DBSCAN" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="700" y="180" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="e1" value="评价/排序" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="start" target="eval" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" value="趋势预测" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="start" target="pred" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" value="资源分配" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="start" target="opt" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" value="分类分组" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="start" target="cluster" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 节点颜色约定

| 颜色 | 含义 | 填充色 | 边框色 |
|------|------|--------|--------|
| 绿色 | 开始/结束 | #d5e8d4 | #82b366 |
| 蓝色 | 处理步骤 | #dae8fc | #6c8ebf |
| 黄色 | 判断/决策 | #fff2cc | #d6b656 |
| 紫色 | 数据输入/输出 | #e1d5e7 | #9673a6 |
| 红色 | 异常/终止 | #f8cecc | #b85450 |

## 使用方式

1. 将 XML 内容保存为 `.drawio` 文件
2. 用以下方式打开：
   - 在线：https://app.diagrams.net/
   - VS Code：安装 hediet.vscode-drawio 插件
   - 桌面版：https://github.com/jgraph/drawio-desktop/releases
3. 可以直接编辑、导出为 PNG/SVG/PDF
