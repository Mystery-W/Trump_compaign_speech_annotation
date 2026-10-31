import os
import pandas as pd
import re
from datetime import datetime

# 设置路径
input_file = r"C:\Users\numinose\Desktop\Trump in factbase\补充：一些演讲\Trump Speech Complement.csv"
output_dir = r"C:\Users\numinose\Desktop\Trump in factbase\补充：一些演讲\Separated"

# 创建保存目录
os.makedirs(output_dir, exist_ok=True)

# 读取 CSV 文件
df = pd.read_csv(input_file, encoding='ISO-8859-1')

# 重命名原始列为统一格式
df.columns = ['TEXT', 'SPEAKER', 'TITLE']

# 提取标题和标准化日期的函数
def extract_title_and_date(full_title):
    match = re.search(r' - ([A-Za-z]+ \d{1,2}(?:,)? \d{4})$', full_title)
    if match:
        raw_date = match.group(1).replace(',', '')
        try:
            dt = datetime.strptime(raw_date, '%B %d %Y')
            date_str = f"{dt.year}/{dt.month}/{dt.day}"
        except ValueError:
            date_str = "Unknown"
        title = full_title[:match.start()]
    else:
        date_str = "Unknown"
        title = full_title
    return title.strip(), date_str

# 记录发生去重的文件
deduplicated_files = []

# 分组处理
for name, group in df.groupby('TITLE'):
    if not isinstance(name, str) or not name.strip():
        continue

    # 提取标题和日期
    title, date_str = extract_title_and_date(name)

    group = group.copy()
    group["DATE"] = date_str

    # 整行去重
    original_len = len(group)
    group = group.drop_duplicates().reset_index(drop=True)
    if len(group) < original_len:
        deduplicated_files.append(title)

    # 构造安全文件名
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", name.strip())
    safe_title = "_".join(safe_title.split())[:120]  # 限制文件名长度
    filename = f"{safe_title}.csv"
    full_path = os.path.join(output_dir, filename)

    # 保存 CSV 文件
    group.to_csv(full_path, index=False, encoding='utf-8-sig')

# 输出去重日志
if deduplicated_files:
    print("\n以下文件已去重：")
    for t in deduplicated_files:
        print(f"- {t}")
else:
    print("所有文件均未检测到重复。")

print("\n所有文件已保存至：", output_dir)
