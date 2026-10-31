from modules.nlp_loader import get_customized_nlp  # ✅ 引入自定义加载器

nlp = get_customized_nlp()  # ✅ 使用定制 tokenizer

def tag_sentence(text):
    doc = nlp(text)
    tagged_words = []

    for token in doc:
        tagged_words.append({
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

    return tagged_words
