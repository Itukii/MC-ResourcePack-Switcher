import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageChops
import imagehash
import os
import pandas as pd

# 选择文件夹
def select_folder():
    return filedialog.askdirectory()

# 获取所有图片路径（支持 .png 和 .tga）
def get_image_files(folder):
    image_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.png') or file.endswith('.tga'):
                image_files.append(os.path.join(root, file))
    return image_files

# 计算哈希值
def calculate_hash(image_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        return imagehash.average_hash(img)
    except Exception as e:
        print(f"无法处理图片 {image_path}: {e}")
        return None

# 对比图片
def compare_images(folder1, folder2):
    matches = []
    unmatched_bedrock = []
    unmatched_java = []

    folder1_files = {os.path.relpath(f, folder1): calculate_hash(f) for f in get_image_files(folder1)}
    folder2_files = {os.path.relpath(f, folder2): calculate_hash(f) for f in get_image_files(folder2)}

    used_java_files = set()

    for f1, hash1 in folder1_files.items():
        if hash1 is None:
            continue
        matched = False
        for f2, hash2 in folder2_files.items():
            if f2 in used_java_files or hash2 is None:
                continue
            if hash1 == hash2:
                # 哈希一致，再做像素级确认
                try:
                    img1 = Image.open(os.path.join(folder1, f1)).convert("RGBA")
                    img2 = Image.open(os.path.join(folder2, f2)).convert("RGBA")
                    if img1.size == img2.size and list(img1.getdata()) == list(img2.getdata()):
                        matches.append((f1, f2))
                        matched = True
                        used_java_files.add(f2)
                        break
                except Exception as e:
                    print(f"像素对比失败：{f1} vs {f2}：{e}")
        if not matched:
            unmatched_bedrock.append(f1)

    # 查找未使用的Java图像
    for f2 in folder2_files:
        if f2 not in used_java_files:
            unmatched_java.append(f2)

    return matches, unmatched_bedrock, unmatched_java

# 生成CSV报告
def generate_report(matches, unmatched_bedrock, unmatched_java, csv_filename):
    data = []
    for match in matches:
        data.append({"BedrockFileName": match[0], "JavaFileName": match[1], "NamesMatch": "Yes" if match[0] == match[1] else "No"})
    for f in unmatched_bedrock:
        data.append({"BedrockFileName": f, "JavaFileName": "No match", "NamesMatch": "No match"})
    for f in unmatched_java:
        data.append({"BedrockFileName": "No match", "JavaFileName": f, "NamesMatch": "No match"})

    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"Report saved as '{csv_filename}'")

# GUI 主界面
def main():
    root = tk.Tk()
    root.title("Bedrock vs Java Texture Comparison Tool")

    folder1 = ""
    folder2 = ""
    csv_filename = ""

    def choose_folder1():
        nonlocal folder1
        folder1 = select_folder()
        print(f"Bedrock Folder: {folder1}")

    def choose_folder2():
        nonlocal folder2
        folder2 = select_folder()
        print(f"Java Folder: {folder2}")

    def set_csv_filename():
        nonlocal csv_filename
        csv_filename = csv_entry.get()
        print(f"CSV Filename: {csv_filename}")

    def start_comparison():
        if folder1 and folder2 and csv_filename:
            matches, unmatched_bedrock, unmatched_java = compare_images(folder1, folder2)
            generate_report(matches, unmatched_bedrock, unmatched_java, csv_filename)
            print("Comparison completed! Report generated.")
        else:
            print("Please make sure both folders and CSV filename are set.")

    tk.Button(root, text="Select Bedrock Folder", command=choose_folder1).pack(pady=10)
    tk.Button(root, text="Select Java Folder", command=choose_folder2).pack(pady=10)
    tk.Label(root, text="Enter CSV Filename:").pack(pady=5)
    csv_entry = tk.Entry(root)
    csv_entry.pack(pady=5)
    tk.Button(root, text="Set CSV Filename", command=set_csv_filename).pack(pady=10)
    tk.Button(root, text="Start Comparison", command=start_comparison).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()