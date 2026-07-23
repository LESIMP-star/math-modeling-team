"""
绘图工具模块：Nature风格作图、跨平台中文字体检测
提供统一的配色方案和保存函数
"""
import os, sys, warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 跨平台中文字体检测
_CANDIDATES = {
    'Windows' : ['Microsoft YaHei', 'SimHei', 'SimSun', 'FangSong'],
    'Darwin'  : ['PingFang SC', 'Heiti SC', 'STHeiti', 'Apple LiGothic'],
    'Linux'   : ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Droid Sans Fallback'],
}
_chinese_font = None
for family in _CANDIDATES.get(sys.platform, []) + ['Microsoft YaHei', 'PingFang SC', 'WenQuanYi Micro Hei']:
    try:
        fm.findfont(family, fallback_to_default=False)
        _chinese_font = family
        break
    except:
        continue

if not _chinese_font:
    for f in fm.fontManager.ttflist:
        if any(kw in f.name for kw in ['YaHei', 'Hei', 'SimHei', 'FangSong', 'PingFang', 'WenQuanYi', 'Noto Sans CJK', 'Droid Sans Fallback']):
            _chinese_font = f.name
            break

_has_chinese = _chinese_font is not None

# Nature 风格 rcParams
plt.rcParams['font.family'] = 'sans-serif'
if _has_chinese:
    plt.rcParams['font.sans-serif'] = [_chinese_font, 'Arial', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['font.size'] = 15
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2.5
plt.rcParams['legend.frameon'] = False

# Nature 配色
C = {
    "blue":   "#0F4D92",
    "blue2":  "#3775BA",
    "green":  "#8BCF8B",
    "green2": "#AADCA9",
    "green3": "#DDF3DE",
    "red":    "#B64342",
    "red2":   "#E9A6A1",
    "red3":   "#F6CFCB",
    "gray":   "#CFCECE",
    "gray2":  "#767676",
    "gray3":  "#4D4D4D",
    "black":  "#272727",
    "gold":   "#FFD700",
    "teal":   "#42949E",
    "violet": "#9A4D8E",
    "pink":   "#EA84DD",
}
COLORS = [C["blue"], C["green"], C["red"], C["teal"], C["violet"], C["gold"], C["blue2"], C["pink"]]


def save_fig(fig, name, save_dir='./output/figures', fmts=('png',), dpi=600):
    """保存图形到指定目录"""
    os.makedirs(save_dir, exist_ok=True)
    for fmt in fmts:
        p = os.path.join(save_dir, f"{name}.{fmt}")
        fig.savefig(p, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    print(f"图表已保存: {save_dir}/{name}")
