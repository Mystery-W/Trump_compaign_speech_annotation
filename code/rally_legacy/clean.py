import os
import re

# 定义源文件夹和目标文件夹
source_folder = r"D:\\Lesson\\语料库建设与应用\\Trump rally\\General Election rallies (June 2024–November 2024)"
target_folder = r"D:\\Lesson\\语料库建设与应用\\Trump rally\\cleaned"

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

# 遍历源文件夹中的所有txt文件
for file_name in os.listdir(source_folder):
    if file_name.endswith('.txt'):
        source_file_path = os.path.join(source_folder, file_name)
        target_file_path = os.path.join(target_folder, file_name)

        with open(source_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 查找并删除以[]包含的内容
        removed_content = re.findall(r'\[.*?\]', content)
        cleaned_content = re.sub(r'\[.*?\]', '', content)

        # 将清理后的内容保存到目标文件夹
        with open(target_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        # 在终端输出删除的内容
        print(f"File: {file_name}")
        if removed_content:
            for item in removed_content:
                print(f"  Removed: {item}")
        else:
            print("  No content removed.")

print("Processing complete. Cleaned files saved to:", target_folder)