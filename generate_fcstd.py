#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶梯轴 Stepped Shaft - FreeCAD 脚本
在 FreeCAD GUI 中运行此脚本生成 .FCStd 和 .step 文件

用法：
1. 在 5060TI 上用 FreeCAD 打开此脚本
2. 或者命令行运行：freecadcmd generate_fcstd.py
3. 在 FreeCAD Python 控制台运行：
   exec(open("generate_fcstd.py").read())
"""

import FreeCAD as App
import Part
import math
import os

# 创建新文档
doc = App.newDocument("Stepped_Shaft")

# ====================
# 定义各段尺寸
# ====================
segments = [
    {"length": 25, "diameter": 25},   # 第1段 Ø25
    {"length": 10, "diameter": 28},   # 第2段 Ø28
    {"length": 28, "diameter": 30},   # 第3段 Ø30
    {"length": 10, "diameter": 25},   # 第4段回退 Ø25
    {"length": 5, "diameter": 35},    # 第5段法兰小径 Ø35
    {"length": 8, "diameter": 42},    # 第6段法兰大径 Ø42
    {"length": 40, "diameter": 32},   # 第7段半圆键槽处 Ø32
    {"length": 28, "diameter": 30},   # 第8段右端 Ø30
    {"length": 4, "diameter": 25},    # 第9段收尾 Ø25
]

# 键槽参数
keyway_left = {"length": 50, "width": 8, "depth": 4, "x_start": 35}      # 左端平键槽
keyway_middle = {"radius": 14, "width": 8, "x_center": 126}               # 中部半圆键槽
keyway_right = {"length": 28, "width": 8, "depth": 8, "x_start": 130}     # 右端方键槽

# ====================
# 构建阶梯轴主体
# ====================
x = 0
for i, seg in enumerate(segments):
    cyl = Part.makeCylinder(
        seg["diameter"] / 2,
        seg["length"],
        App.Vector(x, 0, 0),
        App.Vector(1, 0, 0)  # X轴方向
    )
    if i == 0:
        shaft = cyl
    else:
        shaft = shaft.fuse(cyl)
    x += seg["length"]

# ====================
# 切除键槽
# ====================

# 左端平键槽
keyway1_box = Part.makeBox(
    keyway_left["length"],
    keyway_left["width"],
    keyway_left["depth"],
    App.Vector(keyway_left["x_start"], 12.5 - keyway_left["width"]/2, 12.5 - keyway_left["depth"])
)
shaft = shaft.cut(keyway1_box)

# 中部半圆键槽 (Woodruff keyway - 简化圆柱切除)
# 位于Ø32段，圆心在轴心偏下
woodruff_cyl = Part.makeCylinder(
    keyway_middle["radius"],
    keyway_middle["width"],
    App.Vector(keyway_middle["x_center"] - keyway_middle["width"]/2, 12.5 - keyway_middle["radius"], 12.5 - keyway_middle["radius"]),
    App.Vector(1, 0, 0)
)
shaft = shaft.cut(woodruff_cyl)

# 右端方键槽
keyway3_box = Part.makeBox(
    keyway_right["length"],
    keyway_right["width"],
    keyway_right["depth"],
    App.Vector(keyway_right["x_start"], 15 - keyway_right["width"]/2, 15 - keyway_right["depth"])
)
shaft = shaft.cut(keyway3_box)

# ====================
# 创建零件
# ====================
part = doc.addObject("Part::Feature", "Stepped_Shaft")
part.Shape = shaft
doc.recompute()

# ====================
# 保存文件
# ====================
output_dir = os.path.dirname(os.path.abspath(__file__))
base_name = os.path.join(output_dir, "stepped_shaft")

# 保存 .FCStd
fcstd_file = base_name + ".FCStd"
doc.saveAs(fcstd_file)
print(f"已保存: {fcstd_file}")

# 导出 .step
step_file = base_name + ".step"
import importStep
importStep.export(doc.Objects, step_file)
print(f"已导出: {step_file}")

print("\n✅ 完成！")
print(f"  总长度: {sum(s['length'] for s in segments)}mm")
print(f"  最大直径: Ø42mm")
print(f"  键槽: 左端平键槽 + 中部半圆键槽 + 右端方键槽")
