import json
from llm_client import chat_json
from schemas import IntentResult
import logging

logger = logging.getLogger(__name__)
CHART_TYPES = {"bar","line","pie","table"}

KEYWORD_MAP = {
    "line": ["趋势", "变化", "走势", "每天", "每月", "时间", "增长", "下降"],
    "pie": ["占比", "比例", "分布", "百分比", "份额", "构成"],
    "bar": ["统计", "对比", "各", "排行", "top", "最高", "排名"],
    "table": ["明细", "列表", "详情", "所有", "全部", "具体"],
}

def rule_recognize(query:str):
    for ctype, words in KEYWORD_MAP.items():
        for w in words:
            if w in query:
                return ctype
    return "bar"

PROMPT = """你是图表推荐专家...（复用上面的Prompt）"""

def recognize_intent(query:str) -> IntentResult:
    try:
        resp = chat_json([{"role":"user","content":PROMPT.format(query=query)}])
        data = json.loads(resp)
        chart = data["chart_type"].lower()
        if chart not in CHART_TYPES:
            chart = rule_recognize(query)
        return IntentResult(chart_type=chart, confidence=data["confidence"], keywords=data["keywords"])
    except Exception as e:
        logger.warning(f"LLM调用失败 {e},使用规则兜底")
        fallback_type = rule_recognize(query)
        return IntentResult(chart_type=fallback_type, confidence=0.4)