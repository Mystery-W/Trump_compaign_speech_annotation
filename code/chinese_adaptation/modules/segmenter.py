# trump_annotation/modules/segmenter.py

from modules.sentiment_analyzer import analyze_sentiment
from modules.nlp_loader import get_customized_nlp
from modules.dependency_analyzer import analyze_dependency  # ✅ 新增
from typing import List, Dict

nlp = get_customized_nlp()

def is_meaningful_token(token) -> bool:
    return not token.is_punct and any(char.isalnum() for char in token.text)

def segment_text(paragraph_text: str) -> List[Dict]:
    doc = nlp(paragraph_text)
    sentences_data = []

    for sent_id, sent in enumerate(doc.sents):
        sent_text = sent.text
        dep_words, dep_stats = analyze_dependency(sent_text)  # ✅ 句法分析调用

        words = []
        for token in sent:
            words.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_,
                "head": token.head.text,
                "is_stop": token.is_stop,
                "is_alpha": token.is_alpha,
                "morph": token.morph.to_dict(),
                "ent_type": token.ent_type_,
                "ent_iob": token.ent_iob_
            })

        sentence = {
            "id": f"s{sent_id+1}",
            "text": sent_text,
            "word_count": sum(1 for token in sent if is_meaningful_token(token)),
            "sentiment": analyze_sentiment(sent_text),
            "words": words,
            # ✅ 附加依存信息
            "sentence_root": dep_stats["sentence_root"],
            "avg_dep_distance": dep_stats["avg_dep_distance"],
            "tree_depth": dep_stats["tree_depth"],
            "dependency_tree_structure": dep_stats["dependency_tree_structure"]
        }
        sentences_data.append(sentence)

    return sentences_data

# 测试
if __name__ == "__main__":
    sample_text = (
        "They make -- then it got up to 550 million, and the market crashed."
    )
    results = segment_text(sample_text)
    from pprint import pprint
    pprint(results)
