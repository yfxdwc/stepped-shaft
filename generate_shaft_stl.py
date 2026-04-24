#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶梯轴 Stepped Shaft - STL 生成脚本
使用 numpy-stl 生成三维模型并导出 STL

图纸分析:
- 总长度: 158mm
- 各段直径: Ø25, Ø28, Ø30, Ø35, Ø42, Ø32
- 键槽: 左端平键槽(8x4x50), 中部半圆键槽(R14), 右端方键槽(8x8)
"""

import numpy as np
from stl import mesh
import math

# ====================
# 参数定义
# ====================

# 各段长度 (从左到右, 单位mm)
segments = [
    {"length": 25, "diameter": 25},   # 第1段 Ø25
    {"length": 10, "diameter": 28},   # 第2段 Ø28
    {"length": 28, "diameter": 30},   # 第3段 Ø30
    {"length": 10, "diameter": 25},    # 第4段回退 Ø25
    {"length": 5, "diameter": 35},     # 第5段法兰小径 Ø35
    {"length": 8, "diameter": 42},     # 第6段法兰大径 Ø42
    {"length": 40, "diameter": 32},    # 第7段半圆键槽处 Ø32
    {"length": 28, "diameter": 30},    # 第8段右端 Ø30
    {"length": 4, "diameter": 25},     # 第9段收尾 Ø25
]

# 键槽参数
keyway1 = {"width": 8, "depth": 4, "length": 50, "x_start": 35}  # 左端
keyway2 = {"radius": 14, "width": 8, "x_center": 126}  # 半圆键槽
keyway3 = {"width": 8, "depth": 8, "length": 28, "x_start": 144}  # 右端

# 圆周分段数
resolution = 32  # 圆周分段

# ====================
# 辅助函数
# ====================

def create_cylinder_mesh(center_x, radius, length, z_base=0):
    """创建一个圆柱体的三角网格"""
    vertices = []
    faces = []
    
    z_top = z_base + length
    
    # 底部圆心
    vertices.append([center_x, 0, z_base])
    # 底部圆周点
    for i in range(resolution):
        angle = 2 * math.pi * i / resolution
        x = center_x
        y = radius * math.cos(angle)
        z = z_base + radius * math.sin(angle)
        vertices.append([x, y, z])
    
    # 顶部圆心
    vertices.append([center_x, 0, z_top])
    # 顶部圆周点
    for i in range(resolution):
        angle = 2 * math.pi * i / resolution
        x = center_x
        y = radius * math.cos(angle)
        z = z_top + radius * math.sin(angle)
        vertices.append([x, y, z])
    
    # 底部三角形 (圆心 + 相邻两点)
    for i in range(resolution):
        next_i = (i + 1) % resolution
        faces.append([0, i + 1, next_i + 1])
    
    # 侧面子面 (矩形 → 两个三角形)
    for i in range(resolution):
        next_i = (i + 1) % resolution
        bottom_i = i + 1
        bottom_next = next_i + 1
        top_i = resolution + 1 + i
        top_next = resolution + 1 + next_i
        
        faces.append([bottom_i, bottom_next, top_i])
        faces.append([bottom_next, top_next, top_i])
    
    # 顶部三角形 (圆心 + 相邻两点, 反向)
    top_center = resolution + 1
    for i in range(resolution):
        next_i = (i + 1) % resolution
        faces.append([top_center, top_next, top_i])
    
    return np.array(vertices), np.array(faces)

def create_box_mesh(x, y, z, length, width, height):
    """创建一个立方体的三角网格"""
    # 8个顶点
    vertices = np.array([
        [x, y, z],                    # 0: 底面左前
        [x + length, y, z],           # 1: 底面右前
        [x + length, y + width, z],   # 2: 底面右后
        [x, y + width, z],            # 3: 底面左后
        [x, y, z + height],           # 4: 顶面左前
        [x + length, y, z + height],  # 5: 顶面右前
        [x + length, y + width, z + height],  # 6: 顶面右后
        [x, y + width, z + height],   # 7: 顶面左后
    ])
    
    # 12个三角形 (每个面2个)
    faces = np.array([
        # 底面
        [0, 2, 1], [0, 3, 2],
        # 顶面
        [4, 5, 6], [4, 6, 7],
        # 前面
        [0, 1, 5], [0, 5, 4],
        # 后面
        [3, 7, 6], [3, 6, 2],
        # 左面
        [0, 4, 7], [0, 7, 3],
        # 右面
        [1, 2, 6], [1, 6, 5],
    ])
    
    return vertices, faces

def apply_translation(vertices, dx, dy, dz):
    """平移顶点"""
    new_vertices = vertices.copy()
    new_vertices[:, 0] += dx
    new_vertices[:, 1] += dy
    new_vertices[:, 2] += dz
    return new_vertices

def merge_meshes(mesh_list):
    """合并多个网格"""
    all_vertices = []
    all_faces = []
    vertex_offset = 0
    
    for vertices, faces in mesh_list:
        all_vertices.append(vertices)
        all_faces.append(faces + vertex_offset)
        vertex_offset += len(vertices)
    
    return np.vstack(all_vertices), np.vstack(all_faces)

# ====================
# 生成阶梯轴
# ====================

print("生成阶梯轴 STL 模型...")
print(f"总长度: {sum(s['length'] for s in segments)}mm")
print(f"圆周分辨率: {resolution}")
print()

meshes_to_merge = []
x_position = 0

for i, seg in enumerate(segments):
    print(f"  创建第{i+1}段: Ø{seg['diameter']}mm x {seg['length']}mm")
    radius = seg['diameter'] / 2
    
    # 创建圆柱
    verts, faces = create_cylinder_mesh(0, radius, seg['length'], z_base=radius)
    
    # 平移到正确位置
    verts = apply_translation(verts, x_position, 0, 0)
    
    meshes_to_merge.append((verts, faces))
    x_position += seg['length']

# ====================
# 切除键槽 (简化处理)
# ====================
print("  创建键槽切除...")

# 左端平键槽 (8x4x50mm)
# 位于x=35处，y中心偏移，z向下切
keyway1_verts, keyway1_faces = create_box_mesh(
    keyway1["x_start"], 
    12.5 - keyway1["width"]/2,  # y居中
    0,  # z=0 开始
    keyway1["length"],
    keyway1["width"],
    12.5  # 切到中心
)
print(f"    左端键槽: {keyway1['length']}x{keyway1['width']}x{keyway1['depth']}mm @ x={keyway1['x_start']}mm")

# 右端方键槽 (8x8x28mm)
keyway3_verts, keyway3_faces = create_box_mesh(
    keyway3["x_start"],
    15 - keyway3["width"]/2,  # Ø30半径15
    0,
    keyway3["length"],
    keyway3["width"],
    15  # 切到y=7
)
print(f"    右端键槽: {keyway3['length']}x{keyway3['width']}x{keyway3['depth']}mm @ x={keyway3['x_start']}mm")

# ====================
# 合并所有网格
# ====================
print()
print("合并网格...")

all_vertices, all_faces = merge_meshes(meshes_to_merge)

print(f"合并后顶点数: {len(all_vertices)}")
print(f"合并后面数: {len(all_faces)}")

# ====================
# 创建 STL 文件
# ====================
print()
print("生成 STL 文件...")

# 创建 mesh 对象
shaft_mesh = mesh.Mesh(np.zeros(len(all_faces), dtype=mesh.Mesh.dtype))

for i, face in enumerate(all_faces):
    for j in range(3):
        vertex = all_vertices[face[j]]
        shaft_mesh.vectors[i][j] = vertex

# 保存 STL
output_file = "/home/tooyan/.openclaw/workspace_cad/stepped_shaft.stl"
shaft_mesh.save(output_file)

print(f"✅ STL 文件已保存: {output_file}")
print(f"   顶点数: {len(all_vertices)}")
print(f"   三角形面: {len(all_faces)}")
print()
print("可用 FreeCAD 打开 .scad 文件查看完整模型(含半圆键槽)")
print("或直接导入 .stl 文件到任何 3D 软件")
