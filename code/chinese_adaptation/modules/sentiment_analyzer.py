# modules/sentiment_analyzer.py
# 移除：from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict

# 引入 SnowNLP，如果选择此方案
from snownlp import SnowNLP

# 如果使用 SnowNLP，analyzer 对象就不再需要 VADER 的 SentimentIntensityAnalyzer
# analyzer = SentimentIntensityAnalyzer() # 移除此行

def analyze_sentiment(text: str) -> Dict:
    """
    对输入文本进行情感分析，返回正面、中性、负面和复合得分。
    （已修改为支持中文，使用 SnowNLP 进行情感分析）
    """
    # 检查输入文本是否为空，避免 SnowNLP 报错
    if not text.strip():
        return {
            "compound": 0.0,
            "positive": 0.0,
            "neutral": 0.0,
            "negative": 0.0
        }

    # SnowNLP 的 sentiment 返回一个 [0, 1] 之间的浮点数，
    # 接近 1 表示积极，接近 0 表示消极，0.5 左右表示中性。
    s = SnowNLP(text)
    sentiment_score = s.sentiments

    # 将 SnowNLP 的结果映射到类似 VADER 的输出格式
    # 这只是一个示例映射，您可以根据实际需求调整逻辑
    if sentiment_score >= 0.65: # 积极
        return {
            "compound": round(sentiment_score, 4),
            "positive": round(sentiment_score, 4),
            "neutral": round(1 - sentiment_score, 4), # 假设剩下的是中性
            "negative": 0.0
        }
    elif sentiment_score <= 0.35: # 消极
        return {
            "compound": round(sentiment_score, 4),
            "positive": 0.0,
            "neutral": round(sentiment_score, 4), # 假设剩下的是中性
            "negative": round(1 - sentiment_score, 4)
        }
    else: # 中性
        return {
            "compound": round(sentiment_score, 4),
            "positive": 0.0,
            "neutral": round(sentiment_score, 4),
            "negative": 0.0
        }
