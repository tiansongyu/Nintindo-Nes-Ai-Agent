"""
NES RAM Search 教程 - 使用Manim制作的教学视频
介绍如何使用FCEUX的RAM Search工具查找游戏内存地址

运行方式:
    manim -pql ram_search_tutorial.py RAMSearchTutorial
    manim -pqh ram_search_tutorial.py RAMSearchTutorial  # 高质量渲染
"""

from manim import *

# 颜色配置
TITLE_COLOR = "#FFD700"  # 金色
HIGHLIGHT_COLOR = "#00FF88"  # 绿色高亮
ADDRESS_COLOR = "#FF6B6B"  # 红色地址
VALUE_COLOR = "#4ECDC4"  # 青色值
MEMORY_BG = "#1a1a2e"  # 深蓝背景


class TitleScene(Scene):
    """标题场景"""
    def construct(self):
        # 资源路径
        assets_dir = "..\\assets"

        # 主标题
        title = Text("NES 游戏内存Hack教程", font_size=56, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.8)

        subtitle = Text("使用FCEUX RAM Search获取游戏数据", font_size=32, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        # 上期视频说明
        last_video_note = Text("— 上期视频《NES游戏AI训练环境搭建》详细讲解 —", font_size=18, color=YELLOW)
        last_video_note.next_to(subtitle, DOWN, buff=0.3)

        # NES图片 - 左侧
        nes_image = ImageMobject(f"{assets_dir}\\nes.png")
        nes_image.scale_to_fit_height(2.5)
        nes_image.to_edge(LEFT, buff=1.2)
        nes_image.shift(DOWN * 0.5)

        # 头像 - 右侧偏左（圆形裁剪效果）
        avatar = ImageMobject(f"{assets_dir}\\lufei.jpg")
        avatar.scale_to_fit_height(2)
        avatar.to_edge(RIGHT, buff=4.2)
        avatar.shift(DOWN * 0.5)

        # 头像圆形边框
        avatar_border = Circle(radius=1.05, color=TITLE_COLOR, stroke_width=4)
        avatar_border.move_to(avatar)

        # 作者ID
        author_id = Text("__invoker", font_size=28, color=HIGHLIGHT_COLOR)
        author_id.next_to(avatar, DOWN, buff=0.3)

        # 作者标签
        author_label = Text("作者", font_size=18, color=GRAY)
        author_label.next_to(author_id, DOWN, buff=0.1)

        # 动画
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.play(FadeIn(last_video_note, shift=UP), run_time=0.8)

        # 同时显示NES图片和头像
        self.play(
            FadeIn(nes_image, shift=RIGHT),
            FadeIn(avatar, shift=LEFT),
            run_time=1
        )
        self.play(
            Create(avatar_border),
            FadeIn(author_id, shift=UP),
            FadeIn(author_label, shift=UP),
            run_time=0.8
        )

        self.wait(2)
        self.play(FadeOut(Group(title, subtitle, last_video_note, nes_image, avatar, avatar_border, author_id, author_label)))


class NESMemoryIntro(Scene):
    """NES内存结构介绍"""
    def construct(self):
        # 章节标题
        chapter = Text("第一章: NES内存结构", font_size=42, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        # 内存映射数据：地址、名称、颜色、图标、是否重要、通俗解释
        memory_data = [
            ("$0000-$00FF", "Zero Page", "#FF6B6B", "⚡", True,
             "CPU快速访问区\n游戏核心变量在这\n(生命、状态等)"),
            ("$0100-$01FF", "Stack", "#4ECDC4", "📚", True,
             "函数调用栈\n偶尔存临时数据\n(一般不用关心)"),
            ("$0200-$07FF", "RAM", "#45B7D1", "🎮", True,
             "主要数据区 ⭐重点\n生命、分数、坐标\nRAM Search主战场"),
            ("$2000-$2007", "PPU Regs", "#96CEB4", "🖼️", False,
             "图形处理器寄存器\n只负责画面显示\n(对AI训练无意义)"),
            ("$8000-$FFFF", "PRG-ROM", "#DDA0DD", "💾", False,
             "游戏程序ROM\n只读，无法修改\n(不需要关心)"),
        ]

        # 创建内存映射（左侧）
        map_title = Text("内存映射表", font_size=24, color=TITLE_COLOR)
        blocks = VGroup()
        rects = []

        for i, (addr, name, color, icon, important, _) in enumerate(memory_data):
            rect = Rectangle(width=3.0, height=0.55, color=color, fill_opacity=0.4)
            icon_text = Text(icon, font_size=16)
            addr_text = Text(addr, font_size=12, color=WHITE)
            name_text = Text(name, font_size=13, color=color)
            icon_text.move_to(rect.get_left() + RIGHT * 0.22)
            addr_text.move_to(rect.get_left() + RIGHT * 1.0)
            name_text.move_to(rect.get_right() + LEFT * 0.55)
            block = VGroup(rect, icon_text, addr_text, name_text)
            blocks.add(block)
            rects.append(rect)

        blocks.arrange(DOWN, buff=0.08)
        map_title.next_to(blocks, UP, buff=0.2)
        memory_map = VGroup(map_title, blocks)
        memory_map.to_edge(LEFT, buff=0.3)
        memory_map.shift(DOWN * 0.3)

        # 先显示内存映射
        self.play(FadeIn(memory_map))
        self.wait(0.5)

        # 逐个高亮并显示解释（右侧与映射表对齐）
        for i, (addr, name, color, icon, important, explain) in enumerate(memory_data):
            # 解释文本 - 放在映射表右侧
            explain_text = Text(explain, font_size=18, color=WHITE, line_spacing=1.2)

            # 名称标签 - 带图标
            name_label = Text(f"{icon} {name}", font_size=24, color=color)

            # 重要性标记
            if important:
                importance = Text("✓ 需要关注", font_size=16, color=HIGHLIGHT_COLOR)
            else:
                importance = Text("✗ 可以忽略", font_size=16, color=GRAY)

            # 组合右侧内容
            right_content = VGroup(name_label, explain_text, importance)
            right_content.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            right_content.next_to(memory_map, RIGHT, buff=0.5)
            right_content.align_to(rects[i], UP).shift(DOWN * 0.1)

            # 高亮当前块的矩形
            highlight = SurroundingRectangle(rects[i], color=YELLOW, stroke_width=3, buff=0.05)

            if i == 0:
                self.play(Create(highlight), FadeIn(right_content), run_time=0.8)
            else:
                self.play(
                    ReplacementTransform(prev_highlight, highlight),
                    FadeOut(prev_content),
                    FadeIn(right_content),
                    run_time=0.8
                )

            prev_highlight = highlight
            prev_content = right_content
            self.wait(1.8)

        # === 总结页：哪些区域需要关心 ===
        self.play(FadeOut(VGroup(prev_highlight, prev_content)))

        # 总结标题
        summary_title = Text("💡 总结: 我们只需要关心这些区域", font_size=24, color=TITLE_COLOR)
        summary_title.next_to(memory_map, RIGHT, buff=0.4)
        summary_title.align_to(memory_map, UP)

        # 需要关注的区域
        focus_areas = VGroup(
            Text("✓ Zero Page ($0000-$00FF)", font_size=18, color="#FF6B6B"),
            Text("   → 核心游戏变量", font_size=14, color=WHITE),
            Text("✓ Stack ($0100-$01FF)", font_size=18, color="#4ECDC4"),
            Text("   → 偶尔有临时数据", font_size=14, color=WHITE),
            Text("✓ RAM ($0200-$07FF)", font_size=18, color="#45B7D1"),
            Text("   → 最重要! 大部分数据在这", font_size=14, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        focus_areas.next_to(summary_title, DOWN, buff=0.3)

        # 不需要关注的区域
        ignore_areas = VGroup(
            Text("✗ PPU - 只管画面，没有游戏数据", font_size=16, color=GRAY),
            Text("✗ ROM - 只读，无法修改", font_size=16, color=GRAY),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        ignore_areas.next_to(focus_areas, DOWN, buff=0.3)

        self.play(FadeIn(summary_title))
        self.play(FadeIn(focus_areas))
        self.wait(1)
        self.play(FadeIn(ignore_areas))
        self.wait(3)

        # 最后淡出
        self.play(FadeOut(VGroup(chapter, memory_map, summary_title, focus_areas, ignore_areas)))


class DataTypesExplain(Scene):
    """数据类型说明 - 小端序、大端序、BCD编码"""
    def construct(self):
        chapter = Text("第二章: 数据类型与存储方式", font_size=42, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        # ========== 第一部分：字节序对比 ==========
        endian_compare_title = Text("字节序: 数据在内存中的排列方式", font_size=28, color=HIGHLIGHT_COLOR)
        endian_compare_title.next_to(chapter, DOWN, buff=0.5)
        self.play(FadeIn(endian_compare_title))

        # 数值示例
        value_text = Text("数值: 0x1234 (十进制 4660)", font_size=24, color=WHITE)
        value_text.next_to(endian_compare_title, DOWN, buff=0.4)
        self.play(FadeIn(value_text))

        # 创建小端序和大端序对比
        def create_endian_demo(title, values, color, explain):
            title_t = Text(title, font_size=22, color=color)
            boxes = VGroup()
            for addr, val in values:
                box = Rectangle(width=1, height=0.7, color=color, fill_opacity=0.2)
                addr_t = Text(addr, font_size=14, color=GRAY)
                val_t = Text(val, font_size=20, color=color)
                addr_t.next_to(box, UP, buff=0.05)
                val_t.move_to(box)
                boxes.add(VGroup(box, addr_t, val_t))
            boxes.arrange(RIGHT, buff=0.3)
            explain_t = Text(explain, font_size=16, color=WHITE)
            group = VGroup(title_t, boxes, explain_t).arrange(DOWN, buff=0.2)
            return group

        # 小端序 (NES使用)
        little_endian = create_endian_demo(
            "小端序 Little-Endian (NES使用)",
            [("$00", "34"), ("$01", "12")],
            VALUE_COLOR,
            "低位在前，高位在后 → 先存34，再存12"
        )

        # 大端序
        big_endian = create_endian_demo(
            "大端序 Big-Endian",
            [("$00", "12"), ("$01", "34")],
            ADDRESS_COLOR,
            "高位在前，低位在后 → 先存12，再存34"
        )

        endian_group = VGroup(little_endian, big_endian).arrange(RIGHT, buff=1.5)
        endian_group.next_to(value_text, DOWN, buff=0.4)

        self.play(FadeIn(little_endian))
        self.wait(1)
        self.play(FadeIn(big_endian))
        self.wait(1.5)

        # 记忆技巧
        tip = Text("💡 小端序记忆: 小的(低位)放前面", font_size=20, color=YELLOW)
        tip.next_to(endian_group, DOWN, buff=0.3)
        self.play(FadeIn(tip))
        self.wait(2)

        # 清除，进入BCD部分
        self.play(FadeOut(VGroup(endian_compare_title, value_text, endian_group, tip)))

        # ========== 第二部分：BCD编码 ==========
        bcd_title = Text("BCD编码: 用于显示的特殊存储", font_size=28, color=HIGHLIGHT_COLOR)
        bcd_title.next_to(chapter, DOWN, buff=0.5)
        self.play(FadeIn(bcd_title))

        # BCD解释
        bcd_explain = Text("每个字节只存一个十进制数字 (0-9)", font_size=22, color=WHITE)
        bcd_explain.next_to(bcd_title, DOWN, buff=0.4)
        self.play(FadeIn(bcd_explain))

        # BCD示例
        bcd_example_title = Text("例: 分数 123456 用6个字节", font_size=20, color=VALUE_COLOR)
        bcd_example_title.next_to(bcd_explain, DOWN, buff=0.4)

        bcd_boxes = VGroup()
        for val in ["1", "2", "3", "4", "5", "6"]:
            box = Rectangle(width=0.7, height=0.7, color=HIGHLIGHT_COLOR, fill_opacity=0.2)
            val_t = Text(val, font_size=22, color=HIGHLIGHT_COLOR)
            val_t.move_to(box)
            bcd_boxes.add(VGroup(box, val_t))
        bcd_boxes.arrange(RIGHT, buff=0.15)

        bcd_result = Text("直接读取显示，无需计算!", font_size=20, color=YELLOW)
        bcd_demo = VGroup(bcd_example_title, bcd_boxes, bcd_result).arrange(DOWN, buff=0.3)
        bcd_demo.next_to(bcd_explain, DOWN, buff=0.3)

        self.play(FadeIn(bcd_demo))
        self.wait(2)

        # 清除，进入对比
        self.play(FadeOut(VGroup(bcd_title, bcd_explain, bcd_demo)))

        # ========== 对比：普通二进制存储的问题 ==========
        compare_title = Text("对比: 普通二进制存储", font_size=26, color=TITLE_COLOR)
        compare_title.next_to(chapter, DOWN, buff=0.5)
        self.play(FadeIn(compare_title))

        # 普通存储
        normal_box = Rectangle(width=2.5, height=0.8, color=ADDRESS_COLOR, fill_opacity=0.3)
        normal_val = Text("0x1E240", font_size=20, color=ADDRESS_COLOR)
        normal_val.move_to(normal_box)
        normal_label = Text("123456存为一个数值", font_size=16, color=WHITE)
        normal_label.next_to(normal_box, UP, buff=0.1)
        normal_group = VGroup(normal_label, normal_box, normal_val)
        normal_group.next_to(compare_title, DOWN, buff=0.4)
        self.play(FadeIn(normal_group))

        # 问题说明
        problem = VGroup(
            Text("显示时需要除法提取每位:", font_size=18, color=YELLOW),
            Text("123456 ÷ 10 = 12345 余 6", font_size=16, color=WHITE),
            Text("12345 ÷ 10 = 1234 余 5 ...", font_size=16, color=WHITE),
            Text("6502 CPU没有除法指令，很慢!", font_size=18, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        problem.next_to(normal_group, DOWN, buff=0.4)

        self.play(FadeIn(problem))
        self.wait(2)

        # 清除
        self.play(FadeOut(VGroup(compare_title, normal_group, problem)))

        # ========== BCD优势总结 ==========
        why_title = Text("✓ BCD的优势", font_size=26, color=HIGHLIGHT_COLOR)
        why_title.next_to(chapter, DOWN, buff=0.5)
        self.play(FadeIn(why_title))

        why_points = VGroup(
            Text("• 每字节存1位: [1][2][3][4][5][6]", font_size=20, color=WHITE),
            Text("• 显示时直接读取，无需除法!", font_size=20, color=HIGHLIGHT_COLOR),
            Text("• 节省CPU时间用于游戏逻辑", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        why_points.next_to(why_title, DOWN, buff=0.4)

        for point in why_points:
            self.play(FadeIn(point, shift=RIGHT), run_time=0.5)
        self.wait(2)

        # 清除
        self.play(FadeOut(VGroup(why_title, why_points)))

        # ========== 第三部分：data.json 说明 ==========
        # 先解释 data.json 是什么
        datajson_title = Text("什么是 data.json ?", font_size=28, color=HIGHLIGHT_COLOR)
        datajson_title.next_to(chapter, DOWN, buff=0.5)
        self.play(FadeIn(datajson_title))

        # data.json 说明
        datajson_explain = VGroup(
            Text("data.json 是上期视频中 Gym 环境的配置文件", font_size=20, color=WHITE),
            Text("它定义了 AI 需要读取的游戏内存地址", font_size=20, color=WHITE),
            Text("本视频教你如何找到这些地址并正确配置", font_size=20, color=YELLOW),
        ).arrange(DOWN, buff=0.25)
        datajson_explain.next_to(datajson_title, DOWN, buff=0.4)

        # JSON 示例
        json_example = VGroup(
            Text('data.json 示例:', font_size=16, color=GRAY),
            Text('{ "lives": {"address": 34, "type": "|u1"} }', font_size=16, font="Consolas", color=VALUE_COLOR),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        json_example.next_to(datajson_explain, DOWN, buff=0.35)

        self.play(FadeIn(datajson_explain))
        self.play(FadeIn(json_example))
        self.wait(3)

        # 清除，显示类型速查表
        self.play(FadeOut(VGroup(datajson_title, datajson_explain, json_example)))

        # ========== 类型速查表 ==========
        table_title = Text("data.json 类型速查表", font_size=28, color=HIGHLIGHT_COLOR)
        table_title.next_to(chapter, DOWN, buff=0.5)

        # 类型速查表解说
        table_intro = VGroup(
            Text("常用的类型标记：", font_size=20, color=WHITE),
            Text("• |u1 表示单字节无符号", font_size=18, color=VALUE_COLOR),
            Text("• <u2 表示小端2字节", font_size=18, color=VALUE_COLOR),
            Text("• >n6 表示大端BCD 6字节", font_size=18, color=VALUE_COLOR),
            Text("这些标记会写入 data.json 配置文件", font_size=18, color=YELLOW),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        table_intro.next_to(table_title, DOWN, buff=0.4)

        self.play(Write(table_title))
        self.play(FadeIn(table_intro))
        self.wait(2.5)

        # 清除解说，显示完整表格
        self.play(FadeOut(table_intro))

        table_data = [
            ("|u1", "单字节无符号", "0~255", "生命、状态"),
            ("|i1", "单字节有符号", "-128~127", "方向"),
            ("<u2", "小端2字节", "0~65535", "坐标组合"),
            ("<u4", "小端4字节", "大数值", "内部分数"),
            (">n3", "大端BCD 3字节", "显示用", "分数显示"),
            (">n6", "大端BCD 6字节", "显示用", "高分显示"),
        ]

        # 创建表格 - 使用固定列位置对齐
        col_x = [-4.5, -2.0, 1.0, 3.5]  # 四列的X坐标

        table = VGroup()

        # 表头
        header_texts = ["标记", "含义", "范围", "用途"]
        header = VGroup()
        for i, txt in enumerate(header_texts):
            t = Text(txt, font_size=18, color=TITLE_COLOR)
            t.move_to([col_x[i], 0, 0])
            header.add(t)
        table.add(header)

        # 数据行
        for row_data in table_data:
            row = VGroup()
            for i, txt in enumerate(row_data):
                t = Text(txt, font_size=16, color=WHITE)
                t.move_to([col_x[i], 0, 0])
                row.add(t)
            table.add(row)

        table.arrange(DOWN, buff=0.25)
        table.next_to(table_title, DOWN, buff=0.4)

        self.play(FadeIn(table))
        self.wait(3)
        self.play(FadeOut(VGroup(chapter, table_title, table)))


class DataStorageCategories(Scene):
    """NES数据存储5大分类"""
    def construct(self):
        chapter = Text("第三章: NES数据存储5大分类", font_size=42, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        # 介绍文字
        intro = Text("根据4款游戏的data.json分析总结", font_size=24, color=WHITE)
        intro.next_to(chapter, DOWN, buff=0.4)
        self.play(FadeIn(intro))
        self.wait(1)

        # 5大分类数据
        categories = [
            ("类型1", "单字节简单值", "70%", ADDRESS_COLOR),
            ("类型2", "分页组合值", "15%", VALUE_COLOR),
            ("类型3", "大端BCD显示", "10%", HIGHLIGHT_COLOR),
            ("类型4", "小端多字节", "3%", "#DDA0DD"),
            ("类型5", "连续数组", "2%", "#45B7D1"),
        ]

        # 创建左侧分类卡片（加大字体）
        cat_group = VGroup()
        for cat_id, cat_name, cat_pct, cat_color in categories:
            card = Rectangle(width=3.5, height=0.6, color=cat_color, fill_opacity=0.2)
            id_text = Text(cat_id, font_size=18, color=cat_color)
            name_text = Text(cat_name, font_size=16, color=WHITE)
            pct_text = Text(cat_pct, font_size=16, color=GRAY)

            id_text.move_to(card.get_left() + RIGHT * 0.45)
            name_text.move_to(card.get_center())
            pct_text.move_to(card.get_right() + LEFT * 0.35)

            card_group = VGroup(card, id_text, name_text, pct_text)
            cat_group.add(card_group)

        cat_group.arrange(DOWN, buff=0.1)
        cat_group.next_to(intro, DOWN, buff=0.4)

        # 显示所有分类卡片
        for card in cat_group:
            self.play(FadeIn(card, shift=RIGHT), run_time=0.4)
        self.wait(1.5)

        # 将intro和cat_group移动到左侧，缩小比例调整
        left_panel = VGroup(intro, cat_group)
        self.play(
            left_panel.animate.scale(0.8).to_edge(LEFT, buff=0.25).shift(DOWN * 0.2),
            run_time=1
        )

        # 添加左侧标题
        left_title = Text("5大分类", font_size=20, color=TITLE_COLOR)
        left_title.next_to(left_panel, UP, buff=0.15)
        self.play(FadeIn(left_title))

        # 保存左侧panel引用
        self.left_panel = VGroup(left_title, left_panel)
        self.cat_cards = cat_group

        # === 右侧显示详细内容 ===
        # 类型1详解
        self.show_category_detail_right(
            chapter, 0,
            "类型1: 单字节简单值 (最常见)",
            ADDRESS_COLOR,
            [('lives', '34', '|u1'), ('health', '1424', '|u1')],
            "特点: 值范围0-255",
            "适用: 生命、血量、状态"
        )

        # 类型2详解
        self.show_category_detail_right(
            chapter, 1,
            "类型2: 分页组合值",
            VALUE_COLOR,
            [('x_pos_a', '109', '|u1'), ('x_pos_b', '134', '|u1')],
            "公式: 高位×256+低位",
            "适用: 坐标、屏幕滚动"
        )

        # 类型3详解
        self.show_category_detail_right(
            chapter, 2,
            "类型3: 大端BCD显示值",
            HIGHLIGHT_COLOR,
            [('score', '2013', '>n6'), ('time', '2040', '>n3')],
            "特点: 每半字节=1数字",
            "适用: 分数、倒计时显示"
        )

        # 类型4详解
        self.show_category_detail_right(
            chapter, 3,
            "类型4: 小端多字节",
            "#DDA0DD",
            [('score', '2020', '<d4', 'BCD')],
            "特点: 低位字节在前",
            "适用: 大数值分数"
        )

        # 类型5详解
        self.show_category_detail_right(
            chapter, 4,
            "类型5: 连续数组",
            "#45B7D1",
            [('enemy1', '22', '|u1'), ('enemy2', '23', '|u1')],
            "特点: 相邻地址存储",
            "适用: 多敌人、多子弹"
        )

        # === 查找策略总结 ===
        self.play(FadeOut(self.left_panel))

        strategy_title = Text("新游戏数据查找策略", font_size=32, color=TITLE_COLOR)
        strategy_title.next_to(chapter, DOWN, buff=0.5)
        self.play(Write(strategy_title))

        strategies = [
            ("生命/血量", "单字节简单值", "死亡时搜'值减少'"),
            ("分数", "BCD显示/小端多字节", "得分时搜'值增加'"),
            ("玩家坐标", "单字节/分页组合", "移动时搜'值变化'"),
            ("敌人位置", "连续数组", "找到一个检查相邻"),
            ("时间倒计时", "大端BCD显示", "每秒搜'值减少'"),
        ]

        # 固定列宽度位置
        col1_x, col2_x, col3_x = -4.5, -1.5, 2.0

        strat_group = VGroup()
        # 表头
        h1 = Text("数据类型", font_size=18, color=TITLE_COLOR)
        h2 = Text("推测分类", font_size=18, color=TITLE_COLOR)
        h3 = Text("搜索方法", font_size=18, color=TITLE_COLOR)
        h1.move_to([col1_x, 0, 0])
        h2.move_to([col2_x, 0, 0])
        h3.move_to([col3_x, 0, 0])
        header = VGroup(h1, h2, h3)
        strat_group.add(header)

        for data_type, category, method in strategies:
            c1 = Text(data_type, font_size=16, color=WHITE)
            c2 = Text(category, font_size=16, color=HIGHLIGHT_COLOR)
            c3 = Text(method, font_size=16, color=VALUE_COLOR)
            c1.move_to([col1_x, 0, 0])
            c2.move_to([col2_x, 0, 0])
            c3.move_to([col3_x, 0, 0])
            row = VGroup(c1, c2, c3)
            strat_group.add(row)

        strat_group.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        strat_group.next_to(strategy_title, DOWN, buff=0.4)

        self.play(FadeIn(strat_group))
        self.wait(3)
        self.play(FadeOut(VGroup(chapter, strategy_title, strat_group)))

    def show_category_detail_right(self, chapter, cat_index, title, color, examples, feature, usage):
        """在右侧显示分类详细内容，同时高亮左侧对应卡片"""
        # 高亮左侧对应的卡片
        highlight = SurroundingRectangle(self.cat_cards[cat_index], color=YELLOW, stroke_width=3)

        # 右侧详情区域 - 加大字体
        cat_title = Text(title, font_size=26, color=color)
        cat_title.move_to(RIGHT * 2.5 + UP * 1.5)

        # JSON示例 - 加大字体
        example_group = VGroup()
        for item in examples:
            if len(item) == 4:
                name, addr, dtype, desc = item
                line = Text(f'"{name}": {{addr:{addr}, type:"{dtype}"}} //{desc}',
                           font_size=16, font="Consolas", color=WHITE)
            else:
                name, addr, dtype = item
                line = Text(f'"{name}": {{addr:{addr}, type:"{dtype}"}}',
                           font_size=16, font="Consolas", color=WHITE)
            example_group.add(line)
        example_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        example_bg = Rectangle(
            width=example_group.width + 0.4,
            height=example_group.height + 0.3,
            color=color, fill_opacity=0.1, stroke_width=1
        )
        example_bg.move_to(example_group)
        example_with_bg = VGroup(example_bg, example_group)
        example_with_bg.next_to(cat_title, DOWN, buff=0.35)

        # 特点和用途 - 加大字体
        feature_text = Text(feature, font_size=20, color=HIGHLIGHT_COLOR)
        usage_text = Text(usage, font_size=20, color=WHITE)
        info_group = VGroup(feature_text, usage_text).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        info_group.next_to(example_with_bg, DOWN, buff=0.35)

        # 动画
        self.play(Create(highlight), FadeIn(cat_title), run_time=0.6)
        self.play(FadeIn(example_with_bg), run_time=0.5)
        self.play(FadeIn(info_group), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(highlight, cat_title, example_with_bg, info_group)), run_time=0.5)


class SplitAddressExplain(Scene):
    """分页存储说明 - 为什么坐标要分成两个地址"""
    def construct(self):
        chapter = Text("第四章: 分页存储详解", font_size=42, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        # === 第一页：问题 ===
        problem = VGroup(
            Text("问题: 8位CPU限制", font_size=26, color=ADDRESS_COLOR),
            Text("1字节最大值 = 255", font_size=22, color=WHITE),
            Text("马里奥关卡 > 3000像素!", font_size=22, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.3)
        problem.next_to(chapter, DOWN, buff=0.6)

        self.play(FadeIn(problem))
        self.wait(2)

        # === 第二页：解决方案 ===
        self.play(FadeOut(problem))

        solution = Text("解决: 用2个字节组合", font_size=26, color=HIGHLIGHT_COLOR)
        solution.next_to(chapter, DOWN, buff=0.5)

        # 两个地址框 - 简化
        box_a = Rectangle(width=2.5, height=1.2, color=ADDRESS_COLOR, fill_opacity=0.3)
        text_a = VGroup(
            Text("高位 (页码)", font_size=16, color=ADDRESS_COLOR),
            Text("地址: 109", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1)
        text_a.move_to(box_a)
        group_a = VGroup(box_a, text_a)

        box_b = Rectangle(width=2.5, height=1.2, color=VALUE_COLOR, fill_opacity=0.3)
        text_b = VGroup(
            Text("低位 (偏移)", font_size=16, color=VALUE_COLOR),
            Text("地址: 134", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1)
        text_b.move_to(box_b)
        group_b = VGroup(box_b, text_b)

        plus = Text("+", font_size=32, color=YELLOW)
        boxes = VGroup(group_a, plus, group_b).arrange(RIGHT, buff=0.4)
        boxes.next_to(solution, DOWN, buff=0.5)

        # 公式
        formula = Text("位置 = 高位×256 + 低位", font_size=22, color=TITLE_COLOR)
        formula.next_to(boxes, DOWN, buff=0.4)

        self.play(FadeIn(solution))
        self.play(FadeIn(boxes))
        self.play(FadeIn(formula))
        self.wait(2)

        # === 第三页：示例 ===
        self.play(FadeOut(VGroup(solution, boxes, formula)))

        example_title = Text("示例: 位置1000", font_size=26, color=HIGHLIGHT_COLOR)
        example_title.next_to(chapter, DOWN, buff=0.5)

        calc = VGroup(
            Text("1000 ÷ 256 = 3 余 232", font_size=22, color=WHITE),
            Text("高位 = 3, 低位 = 232", font_size=22, color=VALUE_COLOR),
            Text("验证: 3×256 + 232 = 1000 ✓", font_size=22, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.35)
        calc.next_to(example_title, DOWN, buff=0.5)

        self.play(FadeIn(example_title))
        for line in calc:
            self.play(FadeIn(line), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(VGroup(chapter, example_title, calc)))


class DataJsonExplain(Scene):
    """data.json配置文件说明"""
    def construct(self):
        chapter = Text("第五章: data.json 配置", font_size=42, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        # === 第一页：简化JSON示例 ===
        json_text = Text(
            '{ "lives": {"address": 34, "type": "|u1"} }',
            font_size=18, font="Consolas", color=VALUE_COLOR
        )
        json_bg = Rectangle(
            width=json_text.width + 0.4, height=0.6,
            color=WHITE, fill_opacity=0.1, stroke_width=1
        )
        json_bg.move_to(json_text)
        json_group = VGroup(json_bg, json_text)
        json_group.next_to(chapter, DOWN, buff=0.6)

        self.play(FadeIn(json_group))
        self.wait(1)

        # 字段说明 - 简洁版
        field1 = Text("address = 内存地址 (十进制)", font_size=22, color=HIGHLIGHT_COLOR)
        field2 = Text("type = 数据类型", font_size=22, color=HIGHLIGHT_COLOR)
        fields = VGroup(field1, field2).arrange(DOWN, buff=0.3)
        fields.next_to(json_group, DOWN, buff=0.5)

        self.play(FadeIn(fields))
        self.wait(2)

        # === 第二页：地址转换 ===
        self.play(FadeOut(VGroup(json_group, fields)))

        convert_title = Text("地址转换: 十六进制→十进制", font_size=26, color=TITLE_COLOR)
        convert_title.next_to(chapter, DOWN, buff=0.5)

        example = VGroup(
            Text("FCEUX显示: 0x0022", font_size=22, color=WHITE),
            Text("↓", font_size=28, color=YELLOW),
            Text("0x22 = 2×16 + 2 = 34", font_size=22, color=VALUE_COLOR),
            Text("↓", font_size=28, color=YELLOW),
            Text("data.json写: 34", font_size=22, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.3)
        example.next_to(convert_title, DOWN, buff=0.5)

        self.play(FadeIn(convert_title))
        self.play(FadeIn(example))
        self.wait(3)
        self.play(FadeOut(VGroup(chapter, convert_title, example)))


class FindLivesExample(Scene):
    """实战1: 查找生命值 - 左侧窄步骤栏，右侧视频区"""
    def construct(self):
        # 标题
        title = Text("实战演示 1: 查找生命值地址", font_size=32, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 左侧步骤区域 - 窄版竖向排布
        steps_title = Text("操作步骤", font_size=18, color=HIGHLIGHT_COLOR)

        steps = [
            "1.打开RAM Search",
            "2.记录生命=3",
            "3.搜索:等于3",
            "4.游戏中死亡",
            "5.搜索:值减少",
            "6.重复筛选",
            "7.验证记录地址",
        ]

        step_group = VGroup()
        for step_text in steps:
            step = Text(step_text, font_size=12, color=WHITE)
            step_group.add(step)

        step_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # 结果显示 - 窄版
        result_box = Rectangle(width=2.2, height=0.5, color=GREEN, stroke_width=2)
        result_box.set_fill(GREEN, opacity=0.2)
        result_text = Text("0x0022→34", font_size=11, color=GREEN)
        result_text.move_to(result_box)
        result = VGroup(result_box, result_text)

        # 组合左侧面板
        left_panel = VGroup(steps_title, step_group, result).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        left_panel.to_edge(LEFT, buff=0.2)
        left_panel.shift(DOWN * 0.3)

        # 右侧视频预留区 - 加大
        video_box = Rectangle(width=8, height=4.5, color=GRAY, stroke_width=2)
        video_box.set_fill(BLACK, opacity=0.3)
        video_label = Text("[ 视频演示区 ]", font_size=18, color=GRAY)
        video_label.move_to(video_box)
        video_area = VGroup(video_box, video_label)
        video_area.to_edge(RIGHT, buff=0.3)
        video_area.shift(DOWN * 0.2)

        # 动画
        self.play(FadeIn(steps_title))
        self.play(FadeIn(video_area))

        for i, step in enumerate(step_group):
            self.play(FadeIn(step, shift=RIGHT), run_time=0.4)
            self.wait(0.8)

        self.play(FadeIn(result))
        self.wait(2)
        self.play(FadeOut(VGroup(title, steps_title, step_group, video_area, result)))


class FindPositionExample(Scene):
    """实战2: 查找坐标 - 左侧窄步骤栏，右侧视频区"""
    def construct(self):
        # 标题
        title = Text("实战演示 2: 查找玩家坐标", font_size=32, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 左侧步骤区域 - 窄版竖向排布
        steps_title = Text("操作步骤", font_size=18, color=HIGHLIGHT_COLOR)

        steps = [
            "1.打开RAM Search",
            "2.向右移动角色",
            "3.搜索:值增加",
            "4.向左移动角色",
            "5.搜索:值减少",
            "6.站立不动",
            "7.搜索:值不变",
            "8.验证X/Y坐标",
        ]

        step_group = VGroup()
        for step_text in steps:
            step = Text(step_text, font_size=12, color=WHITE)
            step_group.add(step)

        step_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        # 结果显示 - 窄版两行
        result_box = Rectangle(width=2.2, height=0.7, color=GREEN, stroke_width=2)
        result_box.set_fill(GREEN, opacity=0.2)
        result_text = VGroup(
            Text("X:0x6D,0x86", font_size=10, color=GREEN),
            Text("Y:0x00CE", font_size=10, color=GREEN),
        ).arrange(DOWN, buff=0.05)
        result_text.move_to(result_box)
        result = VGroup(result_box, result_text)

        # 组合左侧面板
        left_panel = VGroup(steps_title, step_group, result).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        left_panel.to_edge(LEFT, buff=0.2)
        left_panel.shift(DOWN * 0.3)

        # 右侧视频预留区 - 加大
        video_box = Rectangle(width=8, height=4.5, color=GRAY, stroke_width=2)
        video_box.set_fill(BLACK, opacity=0.3)
        video_label = Text("[ 视频演示区 ]", font_size=18, color=GRAY)
        video_label.move_to(video_box)
        video_area = VGroup(video_box, video_label)
        video_area.to_edge(RIGHT, buff=0.3)
        video_area.shift(DOWN * 0.2)

        # 动画
        self.play(FadeIn(steps_title))
        self.play(FadeIn(video_area))

        for i, step in enumerate(step_group):
            self.play(FadeIn(step, shift=RIGHT), run_time=0.35)
            self.wait(0.6)

        self.play(FadeIn(result))
        self.wait(2)
        self.play(FadeOut(VGroup(title, steps_title, step_group, video_area, result)))


class FindScoreExample(Scene):
    """实战3: 查找分数 - 左侧窄步骤栏，右侧视频区"""
    def construct(self):
        # 标题
        title = Text("实战演示 3: 查找分数地址", font_size=32, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 左侧步骤区域 - 窄版竖向排布
        steps_title = Text("操作步骤", font_size=18, color=HIGHLIGHT_COLOR)

        steps = [
            "1.打开RAM Search",
            "2.得分前记录状态",
            "3.吃金币/打怪",
            "4.搜索:值增加",
            "5.重复得分筛选",
            "6.检查相邻地址",
            "7.确认BCD格式",
        ]

        step_group = VGroup()
        for step_text in steps:
            step = Text(step_text, font_size=12, color=WHITE)
            step_group.add(step)

        step_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # BCD说明 - 窄版
        bcd_note = VGroup(
            Text("BCD:每字节1位", font_size=10, color=YELLOW),
            Text("6字节存分数", font_size=10, color=WHITE),
        ).arrange(DOWN, buff=0.05)

        # 结果显示 - 窄版
        result_box = Rectangle(width=2.2, height=0.5, color=GREEN, stroke_width=2)
        result_box.set_fill(GREEN, opacity=0.2)
        result_text = Text("0x07DD(>n6)", font_size=10, color=GREEN)
        result_text.move_to(result_box)
        result = VGroup(result_box, result_text)

        # 组合左侧面板
        left_panel = VGroup(steps_title, step_group, bcd_note, result).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        left_panel.to_edge(LEFT, buff=0.2)
        left_panel.shift(DOWN * 0.3)

        # 右侧视频预留区 - 加大
        video_box = Rectangle(width=8, height=4.5, color=GRAY, stroke_width=2)
        video_box.set_fill(BLACK, opacity=0.3)
        video_label = Text("[ 视频演示区 ]", font_size=18, color=GRAY)
        video_label.move_to(video_box)
        video_area = VGroup(video_box, video_label)
        video_area.to_edge(RIGHT, buff=0.3)
        video_area.shift(DOWN * 0.2)

        # 动画
        self.play(FadeIn(steps_title))
        self.play(FadeIn(video_area))

        for i, step in enumerate(step_group):
            self.play(FadeIn(step, shift=RIGHT), run_time=0.4)
            self.wait(0.8)

        self.play(FadeIn(bcd_note))
        self.play(FadeIn(result))
        self.wait(2)
        self.play(FadeOut(VGroup(title, steps_title, step_group, video_area, bcd_note, result)))


class SummaryScene(Scene):
    """总结场景"""
    def construct(self):
        chapter = Text("总结", font_size=48, color=TITLE_COLOR)
        chapter.to_edge(UP)
        self.play(Write(chapter))

        summary_points = [
            "✓ NES使用6502 CPU，小端序存储",
            "✓ 大部分游戏数据是1字节无符号整数 (|u1)",
            "✓ RAM Search通过对比变化筛选地址",
            "✓ 找到地址后转换为十进制写入data.json",
            "✓ 常见数据: 生命、分数、坐标、关卡",
        ]

        points_vgroup = VGroup()
        for point in summary_points:
            text = Text(point, font_size=26, color=WHITE)
            points_vgroup.add(text)

        points_vgroup.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        points_vgroup.next_to(chapter, DOWN, buff=0.8)

        for point in points_vgroup:
            self.play(FadeIn(point, shift=RIGHT), run_time=0.6)
            self.wait(0.5)

        # 项目链接
        project_info = VGroup(
            Text("项目地址:", font_size=22, color=HIGHLIGHT_COLOR),
            Text("github.com/tiansongyu/Nintindo-Nes-Ai-Agent", font_size=20, color=VALUE_COLOR),
        ).arrange(DOWN, buff=0.2)
        project_info.to_edge(DOWN, buff=1)

        self.play(FadeIn(project_info, shift=UP))
        self.wait(3)

        # === 参考文献页 ===
        self.play(FadeOut(VGroup(chapter, points_vgroup, project_info)))

        ref_title = Text("参考文献 & 工具", font_size=36, color=TITLE_COLOR)
        ref_title.to_edge(UP)
        self.play(Write(ref_title))

        # GitHub项目地址 - 最显眼
        github_box = Rectangle(width=10, height=0.9, color=HIGHLIGHT_COLOR, fill_opacity=0.3, stroke_width=2)
        github_label = Text("★ 项目地址:", font_size=20, color=YELLOW)
        github_url = Text("github.com/tiansongyu/Nintindo-Nes-Ai-Agent", font_size=18, color=WHITE)
        github_content = VGroup(github_label, github_url).arrange(RIGHT, buff=0.3)
        github_content.move_to(github_box)
        github_group = VGroup(github_box, github_content)
        github_group.next_to(ref_title, DOWN, buff=0.4)

        self.play(FadeIn(github_group))
        self.wait(1)

        # 参考资料
        refs = VGroup(
            Text("参考资料:", font_size=18, color=HIGHLIGHT_COLOR),
            Text("• fceux.com/web/help/", font_size=14, color=WHITE),
            Text("• wiki.nesdev.org/", font_size=14, color=WHITE),
            Text("• MOS 6502 CPU手册", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # 制作工具
        tools = VGroup(
            Text("制作工具:", font_size=18, color=HIGHLIGHT_COLOR),
            Text("• manim.community (动画)", font_size=14, color=WHITE),
            Text("• downloads.khinsider.com (音乐)", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # 左右排列
        columns = VGroup(refs, tools).arrange(RIGHT, buff=1.2, aligned_edge=UP)
        columns.next_to(github_group, DOWN, buff=0.4)

        self.play(FadeIn(columns))

        # 提示信息
        note = Text("▶ 完整链接见视频简介", font_size=16, color=YELLOW)
        note.next_to(columns, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(3)

        # 结束
        thanks = Text("感谢观看!", font_size=48, color=TITLE_COLOR)
        thanks.move_to(ORIGIN)
        self.play(FadeOut(VGroup(ref_title, github_group, columns, note)))
        self.play(Write(thanks))
        self.wait(2)


class RAMSearchTutorial(Scene):
    """完整教程 - 所有场景合并"""
    def construct(self):
        # 依次播放所有场景
        scenes = [
            TitleScene,
            NESMemoryIntro,
            DataTypesExplain,
            DataStorageCategories,  # 新增: 5大分类
            SplitAddressExplain,
            RAMSearchDemo,
            DataJsonExplain,
            FindLivesExample,
            SummaryScene,
        ]

        # 注意: 在Manim中，如果要合并多个场景，
        # 建议单独渲染每个场景然后用视频编辑软件合并
        # 或者将每个场景的construct内容复制到这里

        # 简化版: 显示教程概述
        title = Text("NES RAM Search 完整教程", font_size=48, color=TITLE_COLOR)
        self.play(Write(title))
        self.wait(1)

        subtitle = Text("请分别运行各个场景类查看详细内容", font_size=24, color=WHITE)
        subtitle.next_to(title, DOWN)
        self.play(FadeIn(subtitle))

        scene_list = VGroup()
        for scene_class in scenes:
            name = Text(f"• {scene_class.__name__}", font_size=20, color=HIGHLIGHT_COLOR)
            scene_list.add(name)
        scene_list.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        scene_list.next_to(subtitle, DOWN, buff=0.5)

        self.play(FadeIn(scene_list))
        self.wait(3)


# 运行命令提示
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║             NES RAM Search Tutorial - Manim 视频脚本               ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║ 运行各个场景:                                                       ║
    ║   manim -pql ram_search_tutorial.py TitleScene                    ║
    ║   manim -pql ram_search_tutorial.py NESMemoryIntro                ║
    ║   manim -pql ram_search_tutorial.py DataTypesExplain              ║
    ║   manim -pql ram_search_tutorial.py DataStorageCategories         ║
    ║   manim -pql ram_search_tutorial.py SplitAddressExplain           ║
    ║   manim -pql ram_search_tutorial.py RAMSearchDemo                 ║
    ║   manim -pql ram_search_tutorial.py DataJsonExplain               ║
    ║   manim -pql ram_search_tutorial.py FindLivesExample              ║
    ║   manim -pql ram_search_tutorial.py SummaryScene                  ║
    ║                                                                   ║
    ║ 高质量渲染:                                                         ║
    ║   manim -pqh ram_search_tutorial.py <SceneName>                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

