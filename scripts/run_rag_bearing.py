import json
import argparse
from src.pipeline import AgenticRAGPipeline

def run_rag_batch(qa_path: str, result_path: str) -> None:
    """批量运行 RAG 推理"""
    # 加载 QA 数据
    with open(qa_path, 'r', encoding='utf-8') as f:
        qa_pairs = json.load(f)
    
    # 初始化流水线
    pipeline = AgenticRAGPipeline()
    
    # 处理每个问题
    results = []
    for qa in qa_pairs:
        result = pipeline.process_query(qa['question'])
        results.append({
            "question": qa['question'],
            "expected_answer": qa['answer'],
            "rag_answer": result.get('answer'),
            "sources": result.get('sources', [])
        })
    
    # 保存结果
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"RAG 推理结果已保存: {result_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa_path", required=True, help="QA 数据文件路径")
    parser.add_argument("--result_path", required=True, help="结果输出文件路径")
    args = parser.parse_args()
    
    run_rag_batch(args.qa_path, args.result_path)
