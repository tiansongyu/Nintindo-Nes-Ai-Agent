"""合并所有manim视频场景为一个完整视频"""
import os
from moviepy import VideoFileClip, concatenate_videoclips

# 视频目录
video_dir = r"C:\Users\Administrator\github\Nintindo-Nes-Ai-Agent\manim_video\scripts\media\videos\ram_search_tutorial\480p15"

# 按顺序列出所有场景文件
video_files = [
    "TitleScene.mp4",
    "NESMemoryIntro.mp4", 
    "DataTypesExplain.mp4",
    "DataStorageCategories.mp4",
    "SplitAddressExplain.mp4",
    "RAMSearchDemo.mp4",
    "DataJsonExplain.mp4",
    "FindLivesExample.mp4",
    "SummaryScene.mp4",
]

print("开始合并视频...")
print(f"视频目录: {video_dir}")

# 加载所有视频片段
clips = []
for f in video_files:
    path = os.path.join(video_dir, f)
    print(f"加载: {f}")
    clip = VideoFileClip(path)
    clips.append(clip)

# 合并视频
print("\n正在合并...")
final_clip = concatenate_videoclips(clips, method="compose")

# 输出文件
output_path = os.path.join(video_dir, "NES_RAM_Search_Tutorial_Complete.mp4")
print(f"\n正在写入: {output_path}")
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# 清理
for clip in clips:
    clip.close()
final_clip.close()

print("\n✅ 合并完成!")
print(f"输出文件: {output_path}")

