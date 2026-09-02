from pydantic import BaseModel
from typing import List

class IntentResult(BaseModel):
    chart_type: str
    confidence: float = 0.0
    keywords: List[str] = []