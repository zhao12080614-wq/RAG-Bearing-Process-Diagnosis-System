from typing import Dict, Any
import re

class IntentRouter:
    """意图路由器"""
    
    def __init__(self):
        """初始化意图路由器"""
        self.intent_patterns = {
            "standard": [r"标准|国标|规范|要求|参数"],
            "theory": [r"原理|理论|公式|计算|设计"],
            "defect": [r"故障|缺陷|失效|异常|振动"]
        }
    
    def route(self, query: str) -> str:
        """路由查询到对应的意图"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    return intent
        return "general"
