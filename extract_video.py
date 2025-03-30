import os
import json
import shutil

def extract_real_videos(metadata_path, source_folder, dest_folder, new_metadata_path, max_videos=240):
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # 读取原始 metadata
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    new_metadata = {}
    count = 0

    # 遍历原始 metadata
    for video_name, info in metadata.items():
        # 判断标签是否为 "REAL"
        if info.get("label") == "REAL":
            source_file = os.path.join(source_folder, video_name)
            dest_file = os.path.join(dest_folder, video_name)
            if os.path.exists(source_file):
                shutil.copy2(source_file, dest_file)
                # 构造新的 metadata 项，确保格式满足要求，不换行
                new_metadata[video_name] = {"label": "REAL", "split": "train", "original": None}
                count += 1
                print(f"已复制 {count} 个视频：{video_name}")
            else:
                print(f"文件不存在：{source_file}")
            
            if count >= max_videos:
                break

    # 写出新的 metadata，确保不换行：使用 separators 参数使 JSON 紧凑
    with open(new_metadata_path, "w", encoding="utf-8") as f:
        json.dump(new_metadata, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"共复制了 {count} 个 REAL 视频到 {dest_folder}，新的 metadata 保存在 {new_metadata_path}")

if __name__ == "__main__":
    # 根据实际情况修改以下路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    train_video_dir = os.path.join(base_dir, "dfdc_train_part_49")
    metadata_path = os.path.join(train_video_dir, "metadata.json")         # 原始 metadata 文件路径        # 包含所有视频的文件夹
    dest_folder = os.path.join(base_dir, "Balanced Sample")      # 存放 REAL 视频的目标文件夹
    new_metadata_path = os.path.join(dest_folder, "metadata.json")     # 新 metadata 保存路径
    
    extract_real_videos(metadata_path, train_video_dir, dest_folder, new_metadata_path, max_videos=240)
