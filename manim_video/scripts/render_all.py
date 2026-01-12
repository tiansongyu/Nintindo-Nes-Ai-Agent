"""
批量渲染所有Manim场景的脚本
"""
import subprocess
import os

# 场景列表（按播放顺序）
SCENES = [
    "TitleScene",
    "NESMemoryIntro",
    "DataTypesExplain",
    "DataStorageCategories",
    "SplitAddressExplain",
    "DataJsonExplain",
    "FindLivesExample",
    "FindPositionExample",
    "FindScoreExample",
    "SummaryScene",
]

# 渲染质量选项
QUALITY_OPTIONS = {
    "low": "-pql",      # 480p, 15fps
    "medium": "-pqm",   # 720p, 30fps
    "high": "-pqh",     # 1080p, 60fps
    "4k": "-pqk",       # 4K, 60fps
}

def render_scene(scene_name, quality="medium"):
    """渲染单个场景"""
    quality_flag = QUALITY_OPTIONS.get(quality, "-pqm")
    cmd = f"manim {quality_flag} ram_search_tutorial.py {scene_name}"
    print(f"渲染中: {scene_name}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ {scene_name} 渲染完成")
    else:
        print(f"✗ {scene_name} 渲染失败: {result.stderr}")
    return result.returncode == 0

def render_all(quality="medium"):
    """渲染所有场景"""
    print(f"开始批量渲染 (质量: {quality})...")
    print("=" * 50)
    
    success_count = 0
    for scene in SCENES:
        if render_scene(scene, quality):
            success_count += 1
    
    print("=" * 50)
    print(f"完成! {success_count}/{len(SCENES)} 个场景渲染成功")
    print(f"输出目录: media/videos/ram_search_tutorial/")

if __name__ == "__main__":
    import sys
    quality = sys.argv[1] if len(sys.argv) > 1 else "medium"
    render_all(quality)

