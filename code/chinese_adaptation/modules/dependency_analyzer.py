from typing import List, Tuple, Dict
from modules.nlp_loader import get_customized_nlp

nlp = get_customized_nlp()

def analyze_dependency(text: str) -> Tuple[List[Dict], Dict]:
    """
    对输入句子进行依存句法分析，返回词级信息和句子级统计。
    """
    doc = nlp(text)
    word_data = []

    for token in doc:
        word_data.append({
            "text": token.text,
            "dep": token.dep_,
            "head": token.head.text,
            "head_index": token.head.i,
            "token_index": token.i,
            "dep_distance": abs(token.i - token.head.i)
        })

    # 根节点识别
    roots = [t for t in doc if t.head == t]
    avg_dep_distance = round(sum(w["dep_distance"] for w in word_data) / len(word_data), 2)

    def tree_depth(token):
        if not list(token.children):
            return 1
        return 1 + max(tree_depth(child) for child in token.children)

    max_depth = max(tree_depth(r) for r in roots) if roots else 0

    # 依存结构图（token -> [child_dep: child_text]）
    dep_tree = {}
    for token in doc:
        if token.text not in dep_tree:
            dep_tree[token.text] = []
        for child in token.children:
            dep_tree[token.text].append({"dep": child.dep_, "text": child.text})

    sentence_stats = {
        "sentence_root": roots[0].text if roots else "",
        "avg_dep_distance": avg_dep_distance,
        "tree_depth": max_depth,
        "dependency_tree_structure": dep_tree
    }

    return word_data, sentence_stats
