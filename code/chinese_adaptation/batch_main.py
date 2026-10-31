# trump_annotation/batch_main.py
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.segmenter import segment_text
from modules.metadata_extractor import extract_metadata
# from modules.quita_analyzer import get_quita_features # ❌ 已删除
from modules.sentiment_analyzer import analyze_sentiment
from modules.speech_to_xml import build_xml, save_xml
from modules.utils import ensure_dir_exists

# --- 配置路径 ---
# 请根据您的实际路径修改这里
input_root = r"C:\Users\numinose\Desktop\Trump in factbase\Trump and assassination\data\csv\stage3"
output_root = r"C:\Users\numinose\Desktop\Trump in factbase\Trump and assassination\data\xml\stage3"

# 收集所有 CSV 路径
csv_files = []
for subdir, _, files in os.walk(input_root):
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(os.path.join(subdir, file))

print(f"🗂 共找到 {len(csv_files)} 个 CSV 文件，准备批处理...")

def process_csv(csv_path: str):
    try:
        # 尝试多种编码读取 CSV，确保中文不乱码
        # 强烈建议：将您的所有 CSV 文件统一保存为 UTF-8 编码
        df = pd.DataFrame() # 初始化一个空DataFrame，以防读取失败
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(csv_path, encoding='gbk') # 尝试GBK
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(csv_path, encoding='utf-8-sig') # 尝试带BOM的UTF-8
                except Exception as e:
                    raise ValueError(f"无法读取CSV文件，请检查编码: {e}")

        # 确保 'TEXT' 列存在且不为空
        if 'TEXT' not in df.columns or df['TEXT'].empty:
            raise ValueError(f"CSV文件 '{csv_path}' 中缺少 'TEXT' 列或内容为空。")

        # 提取元数据（不包含 QUITA 特征）
        metadata = extract_metadata(df)
        # ❌ 移除 QUITA 相关的调用
        # quita_scores = get_quita_features(" ".join(df["TEXT"].astype(str)))
        # metadata["statistics"].update(quita_scores)

        # 段落解析
        paragraphs = []
        for idx, row in df.iterrows():
            pid = f"p{idx+1}"
            text = str(row['TEXT']) # 确保文本是字符串，处理 NaN 等情况
            duration = str(row.get("DURATION", "")) # 如果有 DURATION 列

            # 段落情感分析
            p_sentiment = analyze_sentiment(text)

            # 句子处理
            sentences_data = segment_text(text)
            # 句子级情感分析 (已在 segmenter.py 中调用)
            # for s in sentences_data:
            #     s["sentiment"] = analyze_sentiment(s["text"]) # 这部分已在 segmenter.py 中处理

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

        # 生成输出路径并确保目录存在
        rel_path = os.path.relpath(csv_path, input_root)
        output_path = os.path.join(output_root, os.path.splitext(rel_path)[0] + ".xml")
        ensure_dir_exists(output_path) # 确保目录存在

        # 构建并保存 XML
        xml_root = build_xml(metadata, paragraphs)
        save_xml(xml_root, output_path)

        return f"✅ {csv_path} → {output_path}"

    except Exception as e:
        return f"❌ 错误处理 {csv_path}: {e}"

# ✅ 多线程处理 + 进度条
MAX_WORKERS = os.cpu_count() or 4 # 根据CPU核心数调整，避免过度占用资源

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(process_csv, csv_path) for csv_path in csv_files]
    for future in tqdm(as_completed(futures), total=len(csv_files), desc="处理CSV文件"):
        print(future.result())

print("🎉 批处理完成！")