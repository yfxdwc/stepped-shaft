// 阶梯轴 Stepped Shaft - OpenSCAD 代码
// 基于工程图纸生成三维模型
//
// 图纸分析:
// - 总长度: 158mm
// - 各段直径: Ø25, Ø28, Ø30, Ø35, Ø42, Ø32
// - 键槽: 左端平键槽(8x4x50), 中部半圆键槽(R14), 右端方键槽(8x8)
// - 投影法: 第三视角

// ====================
// 参数定义
// ====================

// 各段长度 (从左到右)
segment1_len = 25;   // Ø25
segment2_len = 10;   // Ø28
segment3_len = 28;   // Ø30
segment4_len = 10;   // Ø25 (回退)
segment5_len = 5;    // Ø35 法兰
segment6_len = 8;    // Ø42 法兰
segment7_len = 40;   // Ø32 半圆键槽处
segment8_len = 28;   // Ø30
segment9_len = 4;    // Ø25 收尾

// 各段直径
d1 = 25;
d2 = 28;
d3 = 30;
d4 = 25;
d5 = 35;
d6 = 42;
d7 = 32;
d8 = 30;
d9 = 25;

// 键槽参数
keyway1_width = 8;   // 左端平键槽
keyway1_depth = 4;
keyway1_length = 50;

keyway2_radius = 14; // 半圆键槽半径
keyway2_width = 8;

keyway3_width = 8;   // 右端方键槽
keyway3_depth = 8;
keyway3_length = 28;

// ====================
// 模块定义
// ====================

// 圆柱段模块
module cylinder_segment(diameter, length) {
    cylinder(h=length, d=diameter, center=false);
}

// 键槽切除模块
module keyway_cut(width, depth, length, height_offset) {
    translate([0, -width/2, height_offset])
        cube([length, width, depth]);
}

// ====================
// 生成模型
// ====================

// 总长度
total_length = segment1_len + segment2_len + segment3_len + segment4_len + 
               segment5_len + segment6_len + segment7_len + segment8_len + segment9_len;

echo("总长度 = ", total_length, "mm");

// 构建阶梯轴主体
union() {
    // 第1段 Ø25
    translate([0, 0, 0])
        cylinder_segment(d1, segment1_len);
    
    // 第2段 Ø28
    translate([segment1_len, 0, 0])
        cylinder_segment(d2, segment2_len);
    
    // 第3段 Ø30
    translate([segment1_len + segment2_len, 0, 0])
        cylinder_segment(d3, segment3_len);
    
    // 第4段回退 Ø25
    translate([segment1_len + segment2_len + segment3_len, 0, 0])
        cylinder_segment(d4, segment4_len);
    
    // 第5段法兰小径 Ø35
    translate([segment1_len + segment2_len + segment3_len + segment4_len, 0, 0])
        cylinder_segment(d5, segment5_len);
    
    // 第6段法兰大径 Ø42
    translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len, 0, 0])
        cylinder_segment(d6, segment6_len);
    
    // 第7段半圆键槽处 Ø32
    translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len, 0, 0])
        cylinder_segment(d7, segment7_len);
    
    // 第8段右端 Ø30
    translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + segment7_len, 0, 0])
        cylinder_segment(d8, segment8_len);
    
    // 第9段收尾 Ø25
    translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + segment7_len + segment8_len, 0, 0])
        cylinder_segment(d9, segment9_len);
}

// 切除键槽
difference() {
    // 整体向上偏移，使轴心在 z=0
    translate([0, 0, 12.5])
    union() {
        // 第1段 Ø25
        translate([0, 0, 0])
            cylinder_segment(d1, segment1_len);
        
        // 第2段 Ø28
        translate([segment1_len, 0, 0])
            cylinder_segment(d2, segment2_len);
        
        // 第3段 Ø30
        translate([segment1_len + segment2_len, 0, 0])
            cylinder_segment(d3, segment3_len);
        
        // 第4段回退 Ø25
        translate([segment1_len + segment2_len + segment3_len, 0, 0])
            cylinder_segment(d4, segment4_len);
        
        // 第5段法兰小径 Ø35
        translate([segment1_len + segment2_len + segment3_len + segment4_len, 0, 0])
            cylinder_segment(d5, segment5_len);
        
        // 第6段法兰大径 Ø42
        translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len, 0, 0])
            cylinder_segment(d6, segment6_len);
        
        // 第7段半圆键槽处 Ø32
        translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len, 0, 0])
            cylinder_segment(d7, segment7_len);
        
        // 第8段右端 Ø30
        translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + segment7_len, 0, 0])
            cylinder_segment(d8, segment8_len);
        
        // 第9段收尾 Ø25
        translate([segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + segment7_len + segment8_len, 0, 0])
            cylinder_segment(d9, segment9_len);
    }
    
    // 左端平键槽切除 (位于第1段末端)
    // 位置: 从左端25+10=35mm处开始
    keyway1_x = segment1_len + 10;
    translate([keyway1_x - keyway1_length/2, -keyway1_width/2, 12.5 - keyway1_depth])
        cube([keyway1_length, keyway1_width, keyway1_depth]);
    
    // 中部半圆键槽 (Woodruff keyway R14)
    // 位于法兰右侧的Ø32段
    keyway2_x = segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + 16;
    translate([keyway2_x - keyway2_width/2, 12.5 - keyway2_radius, 12.5 - keyway2_radius])
        cylinder(h=keyway2_width, r=keyway2_radius);
    
    // 右端方键槽
    // 位于右端Ø30段
    keyway3_x = segment1_len + segment2_len + segment3_len + segment4_len + segment5_len + segment6_len + segment7_len + 14;
    translate([keyway3_x - keyway3_length/2, -keyway3_width/2, 15 - keyway3_depth])
        cube([keyway3_length, keyway3_width, keyway3_depth]);
}

// ====================
// 渲染设置
// ====================

// $fn = 100; // 圆周分段数（平滑度）
