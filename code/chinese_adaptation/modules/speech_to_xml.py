import xml.etree.ElementTree as ET
from typing import List, Dict
import xml.dom.minidom as minidom
from modules.dependency_analyzer import analyze_dependency

def indent(elem: ET.Element, level: int = 0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def build_xml(metadata: Dict, paragraphs: List[Dict]) -> ET.Element:
    root = ET.Element("Speech")

    # ===== 元数据处理 =====
    meta_el = ET.SubElement(root, "Metadata")

    info = metadata.get("document_info", {})
    info_el = ET.SubElement(meta_el, "DocumentInfo")
    for key, value in info.items():
        child = ET.SubElement(info_el, key)
        child.text = str(value)

    stats = metadata.get("statistics", {})
    stats_el = ET.SubElement(meta_el, "Statistics")
    for key, value in stats.items():
        try:
            val = float(value)
            child = ET.SubElement(stats_el, key)
            child.text = f"{val:.2f}"
        except (ValueError, TypeError):
            child = ET.SubElement(stats_el, key)
            child.text = str(value)

    # ===== 段落与句子结构 =====
    for p in paragraphs:
        tree_depths = []  # ✅ 新增
        dep_distances = []  # ✅ 新增

        paragraph_attr = {
            "id": p["id"],
            "sentence_count": str(p["sentence_count"]),
            "word_count": str(p["word_count"]),
            "sentiment_compound": str(p["sentiment"]["compound"]),
            "sentiment_pos": str(p["sentiment"]["positive"]),
            "sentiment_neu": str(p["sentiment"]["neutral"]),
            "sentiment_neg": str(p["sentiment"]["negative"]),
        }

        for k, v in p.items():
            if k not in {"id", "text", "sentence_count", "word_count", "sentiment", "sentences"}:
                paragraph_attr[k.lower()] = str(v)

        p_el = ET.SubElement(root, "Paragraph", attrib=paragraph_attr)
        text_el = ET.SubElement(p_el, "text")
        text_el.text = p["text"]

        parse_el = ET.SubElement(p_el, "parse")
        for s in p["sentences"]:
            dep_words, dep_stats = analyze_dependency(s["text"])
            dep_dict = {w["text"]: w for w in dep_words}

            tree_depths.append(dep_stats.get("tree_depth", 0))
            dep_distances.append(dep_stats.get("avg_dep_distance", 0))

            s_el = ET.SubElement(parse_el, "Sentence", attrib={
                "id": s["id"],
                "word_count": str(s["word_count"]),
                "sentiment_compound": str(s["sentiment"]["compound"]),
                "sentiment_pos": str(s["sentiment"]["positive"]),
                "sentiment_neu": str(s["sentiment"]["neutral"]),
                "sentiment_neg": str(s["sentiment"]["negative"]),
                "root": dep_stats.get("sentence_root", ""),
                "avg_dep_distance": str(dep_stats.get("avg_dep_distance", "")),
                "tree_depth": str(dep_stats.get("tree_depth", ""))
            })

            text_s = ET.SubElement(s_el, "text")
            text_s.text = s["text"]

            parse_s = ET.SubElement(s_el, "parse")
            for w in s["words"]:
                dep_info = dep_dict.get(w["text"], {})
                word_el = ET.SubElement(parse_s, "Word", attrib={
                    "text": w.get("text", ""),
                    "lemma": w.get("lemma", ""),
                    "pos": w.get("pos", ""),
                    "tag": w.get("tag", ""),
                    "dep": dep_info.get("dep", ""),
                    "head": dep_info.get("head", ""),
                    "head_index": str(dep_info.get("head_index", "")),
                    "dep_distance": str(dep_info.get("dep_distance", "")),
                    "is_stop": str(w.get("is_stop", False)),
                    "is_alpha": str(w.get("is_alpha", False)),
                    "morph": ";".join(f"{k}={v}" for k, v in w.get("morph", {}).items())
                        if isinstance(w.get("morph"), dict) else str(w.get("morph")),
                    "ent_type": w.get("ent_type", ""),
                    "ent_iob": w.get("ent_iob", "")
                })
                word_el.text = w.get("text", "")

        # ✅ 添加段落级依存信息
        if tree_depths:
            p_el.set("avg_tree_depth", f"{sum(tree_depths)/len(tree_depths):.2f}")
        if dep_distances:
            p_el.set("avg_dep_distance", f"{sum(dep_distances)/len(dep_distances):.2f}")

    indent(root)
    return root

def save_xml(root: ET.Element, output_path: str):
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
