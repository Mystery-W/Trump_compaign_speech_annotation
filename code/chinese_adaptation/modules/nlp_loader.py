import spacy
# from spacy.tokenizer import Tokenizer # 如果不自定义tokenizer，则不需要
# import re # 如果不自定义tokenizer，则不需要

def get_customized_nlp():
    """
    加载并返回一个定制化的 spaCy NLP 模型，支持中文处理。
    对于中文，通常使用 spaCy 默认的中文分词器即可，无需额外自定义。
    """
    try:
        # 加载中文模型
        # 您可以选择 zh_core_web_sm 或 zh_core_web_lg
        # 请确保您已通过 'python -m spacy download zh_core_web_sm' 或 'zh_core_web_lg' 安装了中文模型
        nlp = spacy.load("zh_core_web_lg")
    except OSError:
        print("警告：未找到中文 spaCy 模型 'zh_core_web_sm'。")
        print("请运行以下命令安装：")
        print("python -m spacy download zh_core_web_sm")
        print("或尝试加载 'zh_core_web_lg'。")
        # 作为备用，如果中文模型加载失败，可以考虑抛出错误或加载英文模型（不推荐，因为会导致中文处理失败）
        raise  # 抛出错误，强制用户安装模型

    # 对于中文，spaCy 的默认分词器（Tokenizer）通常已经足够强大和准确。
    # 大多数情况下，您不需要为中文自定义 Tokenizer 规则。
    # 移除或注释掉原先为英文设计的自定义分词规则。
    # 原有的英文定制规则 (如处理 A.I., U.S.A., 连字符单词等) 不适用于中文。

    # 如果您有非常特殊的中文分词需求，可以重新设计 custom_token_match，
    # 但这通常意味着对 spaCy 中文分词器的深度定制，超出了基本中文支持的范畴。
    # 保持代码简洁，依赖 spaCy 默认的中文分词能力是最佳实践。

    return nlp

# --- 测试代码 ---
if __name__ == "__main__":
    print("--- 正在测试 spaCy 中文模型加载 ---")
    try:
        test_nlp = get_customized_nlp()
        print(f"成功加载 spaCy 模型: {test_nlp.meta['name']} (版本: {test_nlp.meta['version']})")
        
        # 简单测试模型功能
        text = "这是一个中文测试句子。"
        doc = test_nlp(text)
        print(f"原始文本: '{text}'")
        print("分词结果:")
        for token in doc:
            print(f"  - '{token.text}' (词性: {token.pos_}, 依存关系: {token.dep_})")
        
        print("测试完成。模型加载成功。")
    except Exception as e:
        print(f"测试失败: {e}")
        print("请确保已按提示下载了 spaCy 中文模型，例如：python -m spacy download zh_core_web_lg")
    print("--- 测试结束 ---")