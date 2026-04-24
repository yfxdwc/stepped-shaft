#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶梯轴 Stepped Shaft - CadQuery 脚本
生成 .step 和 .FCStd 文件
"""
import cadquery as cq
from cadquery import exporters

# ====================
# 定义各段尺寸
# ====================
segments = [
    {"length": 25, "diameter": 25},
    {"length": 10, "diameter": 28},
    {"length": 28, "diameter": 30},
    {"length": 10, "diameter": 25},
    {"length": 5, "diameter": 35},
    {"length": 8, "diameter": 42},
    {"length": 40, "diameter": 32},
    {"length": 28, "diameter": 30},
    {"length": 4, "diameter": 25},
]

# ====================
# 构建阶梯轴主体
# ====================
print("构建阶梯轴...")

# 创建第一个圆柱
result = (cq.Workplane("XY")
    .transformed(rotate=(0, 0, 0), offset=(segments[0]["length"]/2, 0, 0))
    .cylinder(segments[0]["length"], segments[0]["diameter"]/2, centered=(True, False, False))
)

x = segments[0]["length"]
for seg in segments[1:]:
    x += seg["length"]/2
    result = (result
        .union(
            cq.Workplane("XY")
            .transformed(rotate=(0, 0, 0), offset=(x, 0, 0))
            .cylinder(seg["length"], seg["diameter"]/2, centered=(True, False, False))
        )
    )
    x += seg["length"]/2

print(f"  主体构建完成")

# ====================
# 切除键槽
# ====================
print("切除键槽...")

# 左端平键槽 (简化)
keyway_left = cq.Workplane("XY") \
    .transformed(offset=(35 + 25, 12.5 - 4, 0)) \
    .box(50, 4, 8, centered=(True, True, False))
result = result.cut(keyway_left)
print(f"  左端键槽已切除")

# 中部半圆键槽 (简化)
keyway_middle = cq.Workplane("XY") \
    .transformed(offset=(126, 12.5 - 14, 12.5 - 14)) \
    .cylinder(14, 8, centered=(True, True, True))  # 简化为圆柱
result = result.cut(keyway_middle)
print(f"  中部键槽已切除")

# 右端方键槽
keyway_right = cq.Workplane("XY") \
    .transformed(offset=(130 + 14, 15 - 4, 0)) \
    .box(28, 8, 8, centered=(True, True, False))
result = result.cut(keyway_right)
print(f"  右端键槽已切除")

# ====================
# 导出文件
# ====================
output_dir = "/home/tooyan/CAD/2026-04-24_stepped_shaft"

# 导出 .step
step_file = f"{output_dir}/stepped_shaft.step"
exporters.export(result, step_file)
print(f"\n已导出 .step: {step_file}")

# 导出 .stl
stl_file = f"{output_dir}/stepped_shaft.stl"
exporters.export(result, stl_file)
print(f"已导出 .stl: {stl_file}")

print(f"\n✅ 完成！")
print(f"  总长度: {sum(s['length'] for s in segments)}mm")
print(f"  最大直径: Ø42mm")
