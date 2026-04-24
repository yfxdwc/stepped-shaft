#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶梯轴 Stepped Shaft - 根据工程图纸（David Butterworth）重新生成

正确尺寸（从左到右）：
- 总长度: 158mm
- Ø25 × 50mm  (左端键槽段)
- Ø28 × 20mm  (过渡段)
- Ø30 × 20mm  (基准A左侧)
- Ø35 × 25mm  (法兰下方)
- Ø42 × 5mm   (法兰宽度)
- Ø32 × 28mm  (圆弧槽段)
- Ø30 × 10mm  (右端段)

键槽：
- 左端平键槽: 50×8×4mm
- 右侧半圆槽: R14, 8mm宽, 8mm深
"""

import cadquery as cq
from cadquery import exporters

# ====================
# 定义各段尺寸（直径, 长度）
# ====================
segments = [
    (25, 50),   # 左端键槽段
    (28, 20),   # 过渡段
    (30, 20),   # 基准A左侧段
    (35, 25),   # 法兰下方段
    (42, 5),    # 法兰宽度
    (32, 28),   # 圆弧槽段
    (30, 10),   # 右端段
]

# 验证总长度
total = sum(s[1] for s in segments)
print(f"总长度: {total}mm (应为158mm)")

# ====================
# 构建阶梯轴
# ====================

# 第1段: Ø25 × 50mm (起点)
shaft = (cq.Workplane("XY")
         .circle(25/2)
         .extrude(50))

current_length = 50

# 第2段: Ø28 × 20mm (过渡)
shaft = (shaft
         .faces(">Z").workplane()
         .circle(28/2).workplane(offset=3).circle(25/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(28/2).extrude(17))
current_length += 20

# 第3段: Ø30 × 20mm
shaft = (shaft
         .faces(">Z").workplane()
         .circle(30/2).workplane(offset=2).circle(28/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(30/2).extrude(18))
current_length += 20

# 第4段: Ø35 × 25mm
shaft = (shaft
         .faces(">Z").workplane()
         .circle(35/2).workplane(offset=3).circle(30/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(35/2).extrude(22))
current_length += 25

# 第5段: Ø42(法兰) × 5mm
shaft = (shaft
         .faces(">Z").workplane()
         .circle(42/2).workplane(offset=3).circle(35/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(42/2).extrude(2))
current_length += 5

# 第6段: Ø32 × 28mm
shaft = (shaft
         .faces(">Z").workplane()
         .circle(32/2).workplane(offset=3).circle(42/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(32/2).extrude(25))
current_length += 28

# 第7段: Ø30 × 10mm (右端)
shaft = (shaft
         .faces(">Z").workplane()
         .circle(30/2).workplane(offset=2).circle(32/2).loft())
shaft = (shaft.faces(">Z").workplane().circle(30/2).extrude(8))
current_length += 10

print(f"构建完成，总长度: {current_length}mm")

# ====================
# 左端平键槽 (50×8×4mm)
# ====================
# 键槽在轴顶面，中心线通过轴心
# 轴顶面Y = 25/2 = 12.5mm
# 键槽深度4mm，所以键槽底部Y = 12.5 - 4 = 8.5mm
keyway_left = (cq.Workplane("XY")
               .center(25, 0)  # 键槽在轴上方
               .rect(50, 8)    # 长50mm，宽8mm
               .extrude(4)     # 深4mm
               .translate((-25, 0, 25 - 4)))  # 移动到轴顶面

shaft = shaft.cut(keyway_left)
print("左端平键槽(50×8×4mm)已切除")

# ====================
# 右侧半圆槽 (R14, 8宽, 8深)
# ====================
# 法兰位置: 50+20+20+25 = 115mm
# 槽从法兰右侧5mm开始: x = 115 + 5 = 120mm
# 圆柱部分半径14mm，宽度8mm

# 法兰中心 x = 115 + 2.5 = 117.5mm
# 圆弧中心 x = 120 + 14 = 134mm

# 创建半圆槽（Ø32轴上方）
groove_center_x = 120 + 14  # 134mm
groove_radius = 14
groove_depth = 8

# 圆柱
cylinder = (cq.Workplane("XY")
            .center(groove_center_x, 0)
            .circle(groove_radius)
            .extrude(groove_depth))

# 切掉下半圆（留下上半圆作为槽）
cut_box = (cq.Workplane("XY")
           .center(groove_center_x, 0)
           .rect(28, 14)
           .extrude(groove_depth)
           .translate((0, 7, 0)))

half_groove = cylinder.cut(cut_box)
# 移动到轴顶面上方 (Ø32轴，顶面Y = 16mm)
half_groove = half_groove.translate((0, 0, 32 - 8))

shaft = shaft.cut(half_groove)
print("右侧半圆槽(R14, 8×8mm)已切除")

# ====================
# 导出
# ====================
output_dir = "/home/tooyan/CAD/2026-04-24_stepped_shaft"

step_path = f"{output_dir}/stepped_shaft_correct.step"
exporters.export(shaft, step_path)
print(f"STEP: {step_path}")

stl_path = f"{output_dir}/stepped_shaft_correct.stl"
exporters.export(shaft, stl_path)
print(f"STL: {stl_path}")

scad_path = f"{output_dir}/stepped_shaft_correct.scad"
exporters.export(shaft, scad_path)
print(f"SCAD: {scad_path}")

print("\n✅ 正确模型生成完成")
print(f"   总长度: {current_length}mm")
print(f"   直径段数: {len(segments)}段")
print(f"   特征: 7段直径 + 2个键槽")
