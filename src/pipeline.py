import os
import json
from typing import Dict, Any, Optional
from src.agent.intent_router import IntentRouter
from src.hybrid_search.engine import HybridSearchEngine
from src.evaluation.rag_evaluator import RAGEvaluator

class AgenticRAGPipeline:
    """Agentic RAG 核心流水线"""
    
    def __init__(self):
        """初始化流水线"""
        self.intent_router = IntentRouter()
        self.search_engine = HybridSearchEngine()
        self.evaluator = RAGEvaluator()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """处理用户查询"""
        # 1. 意图识别
        intent = self.intent_router.route(query)
        
        # 2. 混合检索
        search_results = self.search_engine.search(query, intent=intent)
        
        # 3. 生成响应
        response = self._generate_response(query, search_results, intent)
        
        return response
    
    def _generate_response(self, query: str, search_results: Dict[str, Any], intent: str) -> Dict[str, Any]:
        """生成响应"""
        # 这里简化处理，实际会调用 LLM 生成
        return {
            "query": query,
            "intent": intent,
            "answer": f"基于检索结果的回答: {search_results.get('hits', [])[0].get('content', 'No results')[:100]}...",
            "sources": [hit.get('source') for hit in search_results.get('hits', [])[:3]]
        }
