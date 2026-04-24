#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶梯轴 Stepped Shaft - FreeCAD Python 脚本
基于工程图纸生成三维模型

图纸分析：
- 总长度: 158mm
- 各段直径: Ø25, Ø28, Ø30, Ø35, Ø42, Ø32
- 键槽: 左端平键槽(8x4x50), 中部半圆键槽(R14), 右端方键槽(8x8)
"""

import FreeCAD as App
import Part
import Sketcher
import math

# 创建新文档
doc = App.newDocument("Stepped_Shaft")

# ====================
# 定义各段尺寸
# ====================
# 从左到右各段长度
segments = [
    {"length": 25, "diameter": 25},      # 第1段 Ø25
    {"length": 10, "diameter": 28},      # 第2段过渡 Ø28
    {"length": 28, "diameter": 30},      # 第3段 Ø30
    {"length": 10, "diameter": 25},      # 第4段回退
    {"length": 5, "diameter": 35},        # 第5段法兰小径
    {"length": 8, "diameter": 42},       # 第6段法兰大径
    {"length": 40, "diameter": 32},       # 第7段半圆键槽处
    {"length": 28, "diameter": 30},       # 第8段右端
    {"length": 4, "diameter": 25},        # 第9段收尾
]

# 累计长度用于定位
x = 0
for seg in segments:
    seg["x_start"] = x
    x += seg["length"]

print("各段位置:")
for i, seg in enumerate(segments):
    print(f"  段{i+1}: x={seg['x_start']}mm, L={seg['length']}mm, Ø{seg['diameter']}mm")

# ====================
# 创建阶梯轴主体
# ====================
print("\n创建阶梯轴主体...")

# 使用 Part.makeCylinder 创建各段，然后融合
shapes = []
for seg in segments:
    cyl = Part.makeCylinder(
        seg["diameter"] / 2,
        seg["length"],
        App.Vector(seg["x_start"], 0, 0),
        App.Vector(1, 0, 0)  # X轴方向
    )
    shapes.append(cyl)

# 融合所有圆柱体
shaft = shapes[0]
for s in shapes[1:]:
    shaft = shaft.fuse(s)

print(f"  主体创建完成，顶点数: {shaft.Nodes}, 面数: {shaft.Faces}")

# ====================
# 创建键槽 (简化表示)
# ====================
print("\n创建键槽...")

# 左端平键槽 (50mm长, 8mm宽, 4mm深)
keyway1_x = 25 + 10 + 14  # 第1段末尾后14mm
keyway1 = Part.makeBox(50, 8, 4, 
                       App.Vector(keyway1_x - 25, 12 - 4, 12.5 - 4))
print(f"  左端键槽: 位置x={keyway1_x-25}mm, 50x8x4mm")

# 中部半圆键槽 (Woodruff keyway R14)
# 简化为圆柱的一部分
woodruff_x = 90  # 法兰右侧
woodruff_base = 12.5  # 圆心高度(Ø25的一半)
woodruff_cyl = Part.makeCylinder(
    14, 8,
    App.Vector(woodruff_x - 4, woodruff_base, 12.5 - 14),
    App.Vector(1, 0, 0)
)
print(f"  半圆键槽: 位置x={woodruff_x-4}mm, R14x8mm")

# 右端方键槽 (28mm长, 8mm宽, 8mm深)
keyway3_x = 130
keyway3 = Part.makeBox(28, 8, 8,
                       App.Vector(keyway3_x - 14, 15 - 8, 15 - 4))
print(f"  右端键槽: 位置x={keyway3_x-14}mm, 28x8x8mm")

# 从主体中切除键槽
shaft_with_keyways = shaft
shaft_with_keyways = shaft_with_keyways.cut(keyway1)
shaft_with_keyways = shaft_with_keyways.cut(woodruff_cyl)
shaft_with_keyways = shaft_with_keyways.cut(keyway3)

print(f"  键槽创建完成，最终顶点数: {shaft_with_keyways.Nodes}")

# ====================
# 显示结果
# ====================
Part.show(shaft_with_keyways)
doc.recompute()

print("\n✅ 阶梯轴模型创建完成!")
print(f"   总长度: 158mm")
print(f"   最大直径: Ø42mm (法兰)")
print(f"   特征: 6段直径 + 3个键槽")

# 保存模型
output_file = "/home/tooyan/.openclaw/workspace_cad/stepped_shaft.fcstd"
doc.save()
print(f"   已保存: {output_file}")
