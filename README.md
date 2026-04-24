# 阶梯轴 Stepped Shaft

基于工程图纸生成的三维 CAD 模型。

## 图纸信息

- **总长度**: 158mm
- **各段直径**: Ø25 → Ø28 → Ø30 → Ø25 → Ø35 → Ø42 → Ø32 → Ø30 → Ø25
- **键槽**: 左端平键槽 + 中部半圆键槽 + 右端方键槽
- **投影法**: 第三视角

## 文件说明

| 文件 | 说明 |
|------|------|
| `stepped_shaft.FCStd` | FreeCAD 原生格式（参数化） |
| `stepped_shaft.step` | 中性交换格式 |
| `stepped_shaft.stl` | 三角网格（3D打印） |
| `stepped_shaft.scad` | OpenSCAD 源码 |
| `generate_*.py` | 生成脚本 |

## 生成方式

1. **CadQuery**: 直接运行 `python3 generate_with_cadquery.py`
2. **FreeCAD**: 在 FreeCAD GUI 中运行 `generate_fcstd.py`

## 历史

- 2026-04-24: 初始版本
