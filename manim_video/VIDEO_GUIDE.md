# NES RAM Search 视频制作指南

## 📁 目录结构

```
manim_video/
├── scripts/                    # Manim脚本
│   ├── ram_search_tutorial.py  # 主教程脚本
│   └── render_all.py           # 批量渲染脚本
├── docs/                       # 参考文档
│   └── NES_Memory_Reference.md # NES内存参考
├── assets/                     # 素材文件夹
│   └── README_assets.md        # 素材说明
└── VIDEO_GUIDE.md              # 本文件
```

## 🎬 视频内容概述

本教程视频包含以下章节：

1. **TitleScene** - 开场标题
2. **NESMemoryIntro** - NES内存结构介绍
3. **DataTypesExplain** - 数据类型与存储方式
4. **RAMSearchDemo** - FCEUX RAM Search工具演示
5. **DataJsonExplain** - data.json配置文件说明
6. **FindLivesExample** - 实战示例：查找生命值
7. **SummaryScene** - 总结

## 🚀 快速开始

### 1. 安装Manim
```bash
pip install manim
```

### 2. 渲染单个场景
```bash
cd manim_video/scripts
manim -pql ram_search_tutorial.py TitleScene
```

### 3. 批量渲染所有场景
```bash
cd manim_video/scripts
python render_all.py medium
```

质量选项: `low`, `medium`, `high`, `4k`

### 4. 输出位置
渲染后的视频位于: `media/videos/ram_search_tutorial/`

## 📝 视频脚本说明

### 核心知识点

1. **NES内存特性**
   - 6502 CPU是8位处理器
   - 使用小端序(Little-Endian)存储
   - 主RAM只有2KB ($0000-$07FF)

2. **data.json类型标记**
   - `|u1`: 1字节无符号整数
   - `|i1`: 1字节有符号整数
   - `<u4`: 4字节小端无符号
   - `<d4`: 4字节小端BCD编码
   - `>n6`: 6字节大端BCD编码

3. **RAM Search流程**
   - 观察游戏中的值变化
   - 使用对比搜索缩小范围
   - 验证找到的地址
   - 转换为十进制写入data.json

## 🔧 自定义修改

### 修改颜色主题
在脚本开头修改颜色常量：
```python
TITLE_COLOR = "#FFD700"      # 标题颜色
HIGHLIGHT_COLOR = "#00FF88"  # 高亮颜色
ADDRESS_COLOR = "#FF6B6B"    # 地址颜色
VALUE_COLOR = "#4ECDC4"      # 值颜色
```

### 添加新场景
1. 创建新的Scene类
2. 实现`construct`方法
3. 添加到`SCENES`列表中

## 📚 参考资源

- [FCEUX官方文档](https://fceux.com/web/help/)
- [NESdev Wiki](https://wiki.nesdev.org/)
- [Manim官方文档](https://docs.manim.community/)
- [本项目data.json示例](../SuperMarioBros_PPO/rom/data.json)

## 🎯 后续工作

1. [ ] 录制FCEUX实际操作演示
2. [ ] 添加配音/字幕
3. [ ] 使用视频编辑软件合并所有场景
4. [ ] 添加背景音乐
5. [ ] 导出最终视频

