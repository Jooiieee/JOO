import json
from llm_client import LLMClient

SENTIMENT_PROMPT = """你是电商平台的评价分析助手。
请判断下面这条商品评论的情感倾向，并给出置信度。

只输出 JSON，格式如下：
{{"sentiment": "positive|negative|neutral", "confidence": 0.0~1.0, "reason": "一句话理由"}}

评论：{comment}"""

REVIEWS = [
    "质量很好，物流也快，非常满意！",
    "收到货就坏了，客服态度还特别差。",
    "一般般吧，跟图片差不多，没有惊喜。",
    "用了一个月，电池依然耐用，推荐购买。",
    "包装简陋，但商品本身还行。",
    "速度太慢了，等了一周才发货。",
    "性价比超高，已经回购第二次了。",
    "颜色和描述有点出入，差评。",
    "东西不错，就是有点贵。",
    "客服很有耐心，问题都解决了。",
    "做工精致，手感很棒，物超所值。",
    "刚拆开包装就发现划痕严重，不推荐。",
    "商品符合预期，不好不坏，可以接受。",
    "送货小哥服务贴心，整体体验很棒。",
    "材质单薄不值这个价钱，很失望。",
    "日常使用足够，没有明显优点也没有缺点。",
    "颜值在线，使用效果超出我的期待。",
    "售后处理拖沓，沟通半天得不到解决。",
    "中规中矩的一款产品，没有特别惊艳。",
    "活动入手很划算，身边朋友我都安利了。"
]

llm = LLMClient()

correct = 0
for review in REVIEWS:
    raw = llm.chat(
        messages=[{"role": "user", "content": SENTIMENT_PROMPT.format(comment=review)}],
        json_mode=True
    )
    result = json.loads(raw)
    label = "positive" if any(k in review for k in ["满意", "推荐", "性价比", "耐心", "耐用", "精致", "物超所值", "贴心", "超出", "划算", "安利"]) \
        else "negative" if any(k in review for k in ["坏了", "差", "差评", "慢", "简陋", "出入", "划痕", "失望", "单薄", "拖沓"]) \
        else "neutral"
    hit = result["sentiment"] == label
    correct += hit
    print(f"{'✓' if hit else '✗'} 预测={result['sentiment']} 标注={label} "
          f"置信度={result['confidence']} | {review}")

print(f"\n准确率: {correct}/{len(REVIEWS)} = {correct / len(REVIEWS):.0%}")