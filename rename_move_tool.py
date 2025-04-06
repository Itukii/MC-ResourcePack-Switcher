
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import pandas as pd

# 选择文件夹
def select_folder():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    return folder_selected

# 加载 CSV 对照表
def load_csv(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
        return df
    except Exception as e:
        messagebox.showerror("错误", f"加载 CSV 文件失败: {e}")
        return None

# 根据 CSV 修改文件名并移动文件
def rename_and_move_files(folder, target_folder, df, direction, csv_filename):
    renamed_files = []
    errors = []
    
    for index, row in df.iterrows():
        if direction == 'BedrockToJava':  # 从基岩版到Java版
            source = row['BedrockFileName']
            target = row['JavaFileName']
        else:  # 从Java版到基岩版
            source = row['JavaFileName']
            target = row['BedrockFileName']
        
        # 跳过 "No match"
        if source == "No match" or target == "No match":
            continue

        source_path = os.path.join(folder, source)
        target_path = os.path.join(target_folder, target)
        
        # 检查源文件是否存在
        if os.path.exists(source_path):
            try:
                # 创建目标文件夹（如果不存在）
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                # 移动并重命名文件
                shutil.move(source_path, target_path)
                renamed_files.append((source, target))
            except Exception as e:
                errors.append((source, target, str(e)))
        else:
            errors.append((source, target, "源文件不存在"))
    
    # 输出结果
    if renamed_files:
        messagebox.showinfo("成功", f"成功重命名并移动 {len(renamed_files)} 个文件")
    if errors:
        error_messages = "\n".join([f"{e[0]} -> {e[1]}: {e[2]}" for e in errors])
        messagebox.showwarning("错误", f"部分文件重命名失败:\n{error_messages}")
    
    # 返回修改的文件列表
    return renamed_files, errors

# GUI 主界面
def main():
    root = tk.Tk()
    root.title("批量文件重命名并移动工具")

    # 选择文件夹
    folder = ""
    def choose_folder():
        nonlocal folder
        folder = select_folder()
        print(f"选择的源文件夹: {folder}")

    # 选择目标文件夹
    target_folder = ""
    def choose_target_folder():
        nonlocal target_folder
        target_folder = select_folder()
        print(f"选择的目标文件夹: {target_folder}")

    # 获取CSV文件路径
    csv_filename = ""
    def set_csv_filename():
        nonlocal csv_filename
        csv_filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        print(f"选择的CSV文件: {csv_filename}")

    # 选择转换方向
    direction = tk.StringVar(value="BedrockToJava")  # 默认选择基岩版转Java版
    def set_direction(value):
        direction.set(value)

    # 开始重命名并移动文件
    def start_renaming():
        if folder and target_folder and csv_filename:
            df = load_csv(csv_filename)
            if df is not None:
                renamed_files, errors = rename_and_move_files(folder, target_folder, df, direction.get(), csv_filename)
                print(f"重命名并移动的文件: {renamed_files}")
                print(f"错误信息: {errors}")
        else:
            messagebox.showwarning("警告", "请先选择源文件夹、目标文件夹和CSV文件！")

    # GUI 元素
    tk.Button(root, text="选择源文件夹", command=choose_folder).pack(pady=10)
    tk.Button(root, text="选择目标文件夹", command=choose_target_folder).pack(pady=10)
    tk.Button(root, text="选择CSV文件", command=set_csv_filename).pack(pady=10)

    # 选择转换方向
    tk.Label(root, text="选择转换方向:").pack(pady=5)
    tk.Radiobutton(root, text="从基岩版到Java版", variable=direction, value="BedrockToJava").pack(pady=5)
    tk.Radiobutton(root, text="从Java版到基岩版", variable=direction, value="JavaToBedrock").pack(pady=5)

    # 开始重命名并移动按钮
    tk.Button(root, text="开始重命名并移动", command=start_renaming).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
