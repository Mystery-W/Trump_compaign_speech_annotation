# trump_annotation/main.py
import pandas as pd
from modules.segmenter import segment_text
from modules.metadata_extractor import extract_metadata
# from modules.quita_analyzer import get_quita_features # ❌ 已删除
from modules.sentiment_analyzer import analyze_sentiment
from modules.speech_to_xml import build_xml, save_xml
from modules.utils import ensure_dir_exists, get_output_path
import os

# --- 用户输入和配置路径 ---
csv_path = input("请输入清洗后CSV文件路径：\n")
# 请根据您的实际需求修改输出目录
output_dir = r"dayunv_xml"

# 确保输出目录存在
ensure_dir_exists(os.path.join(output_dir, "dummy_file.xml")) # 传入一个虚构的文件名以创建父目录

# 读取CSV文件
# 尝试多种编码读取 CSV，确保中文不乱码
# 强烈建议：将您的所有 CSV 文件统一保存为 UTF-8 编码
df = pd.DataFrame() # 初始化一个空DataFrame
try:
    df = pd.read_csv(csv_path, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(csv_path, encoding='gbk') # 尝试GBK
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_path, encoding='utf-8-sig') # 尝试带BOM的UTF-8
        except Exception as e:
            print(f"❌ 错误：无法读取CSV文件 '{csv_path}'，请检查编码。错误信息：{e}")
            exit() # 或者其他错误处理方式

# 确保 'TEXT' 列存在且不为空
if 'TEXT' not in df.columns or df['TEXT'].empty:
    print(f"❌ 错误：CSV文件 '{csv_path}' 中缺少 'TEXT' 列或内容为空。")
    exit()

# 提取元数据（不包含 QUITA 特征）
metadata = extract_metadata(df)
# ❌ 移除 QUITA 相关的调用
# quita_scores = get_quita_features(" ".join(df['TEXT'].astype(str)))
# metadata["statistics"].update(quita_scores) # ❌ 移除 QUITA 相关的更新

# 段落解析
paragraphs = []
for idx, row in df.iterrows():
    pid = f"p{idx+1}"
    text = str(row['TEXT']) # 确保文本是字符串
    duration = str(row.get("DURATION", "")) # 如果有 DURATION 列

    # 段落情感分析
    p_sentiment = analyze_sentiment(text)

    # 句子处理
    sentences_data = segment_text(text)
    # 句子级情感分析 (已在 segmenter.py 中调用)
    # for s in sentences_data:
    #     s["sentiment"] = analyze_sentiment(s["text"]) # 这部分已在 segmenter.py 中处理

    # 收集段落字段（包含非 constant 的其他列）
    paragraph_data = {
        "id": pid,
        "text": text,
        "duration": duration,
        "sentence_count": len(sentences_data),
        "word_count": sum(s["word_count"] for s in sentences_data),
        "sentiment": p_sentiment, # 段落情感
        "sentences": sentences_data
    }

    # 添加除了 'TEXT' 列和 document_info 中已包含的常量列之外的所有列作为段落元数据
    for col in df.columns:
        if col.upper() != "TEXT" and col not in metadata["document_info"]:
            paragraph_data[col] = str(row[col])

    paragraphs.append(paragraph_data)

# 生成输出路径
output_path = get_output_path(csv_path, output_dir)

# 构建并保存 XML
xml_root = build_xml(metadata, paragraphs)
save_xml(xml_root, output_path)

print(f"🎉 处理完成！XML文件已保存至：{output_path}")