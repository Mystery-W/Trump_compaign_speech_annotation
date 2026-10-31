# trump_annotation/modules/metadata_extractor.py

import pandas as pd
from modules.nlp_loader import get_customized_nlp
from modules.dependency_analyzer import analyze_dependency  # ✅ 新增

nlp = get_customized_nlp()

def is_meaningful_token(token) -> bool:
    return not token.is_punct and any(char.isalnum() for char in token.text)

def extract_constant_columns(df: pd.DataFrame) -> dict:
    """
    提取所有值完全一致的列，作为文档层元数据。
    """
    constant_fields = {}
    for col in df.columns:
        if col.upper() == "TEXT":
            continue
        if df[col].nunique() == 1:
            constant_fields[col] = df[col].iloc[0]
    return constant_fields

def extract_metadata(df: pd.DataFrame) -> dict:
    paragraph_count = len(df)
    sentence_count = 0
    word_count = 0
    total_sentence_length = 0
    total_word_length = 0
    all_meaningful_tokens = []

    all_tree_depths = []
    all_dep_distances = []

    for text in df["TEXT"]:
        doc = nlp(str(text))
        sentences = list(doc.sents)
        sentence_count += len(sentences)

        for sent in sentences:
            meaningful_tokens = [token for token in sent if is_meaningful_token(token)]
            word_count += len(meaningful_tokens)
            total_sentence_length += len(meaningful_tokens)
            total_word_length += sum(len(token.text) for token in meaningful_tokens)
            all_meaningful_tokens.extend(token.text for token in meaningful_tokens)

            # ✅ 加入依存结构分析
            _, sent_stats = analyze_dependency(sent.text)
            all_tree_depths.append(sent_stats.get("tree_depth", 0))
            all_dep_distances.append(sent_stats.get("avg_dep_distance", 0))

    unique_types = set(all_meaningful_tokens)
    type_token_ratio = round(len(unique_types) / len(all_meaningful_tokens), 2) if all_meaningful_tokens else 0

    statistics = {
        "paragraph_count": paragraph_count,
        "sentence_count": sentence_count,
        "word_count": word_count,
        "type_token_ratio": type_token_ratio,
        "avg_sentence_length": round(total_sentence_length / sentence_count, 2) if sentence_count else 0,
        "avg_word_length": round(total_word_length / word_count, 2) if word_count else 0,
        # ✅ 添加依存统计
        "max_tree_depth": max(all_tree_depths) if all_tree_depths else 0,
        "avg_dep_distance": round(sum(all_dep_distances) / len(all_dep_distances), 2) if all_dep_distances else 0
    }

    return {
        "document_info": extract_constant_columns(df),
        "statistics": statistics
    }
