import os
import json
from tkinter import Tk, filedialog, Button, Label, messagebox
from PIL import Image

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_label.config(text=f"选择的文件夹: {folder}")
        generate_mcmeta_for_folder(folder)

def generate_mcmeta_for_folder(folder_path, target_duration_ticks=20):
    generated = 0
    skipped = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        if height > width:
                            frame_count = height // width
                            if frame_count <= 1:
                                skipped += 1
                                continue

                            frametime = max(1, round(target_duration_ticks / frame_count))  # 使用frametime，确保一致性
                            meta = {
                                "animation": {
                                    "frametime": frametime,  # 使用frametime变量
                                    "interpolate": True  # 设置插值为 true，平滑过渡
                                }
                            }

                            meta_filename = file_path + ".mcmeta"
                            with open(meta_filename, 'w') as f:
                                json.dump(meta, f, indent=2)
                            generated += 1
                except Exception as e:
                    print(f"跳过 {file_path}: {e}")
                    skipped += 1
    messagebox.showinfo("完成", f"已生成 {generated} 个 .mcmeta 文件，跳过 {skipped} 个文件")

# UI 设置
root = Tk()
root.title(".mcmeta 动画自动生成工具")
root.geometry("400x200")

Label(root, text="选择一个包含贴图的文件夹：").pack(pady=10)
Button(root, text="选择文件夹并生成 .mcmeta", command=select_folder).pack(pady=10)
folder_label = Label(root, text="尚未选择文件夹")
folder_label.pack(pady=10)

root.mainloop()
