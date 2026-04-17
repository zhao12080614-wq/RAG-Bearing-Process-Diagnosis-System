import json
import argparse
from src.evaluation.rag_evaluator import RAGEvaluator

def evaluate_rag_results(input_json: str, output_json: str) -> None:
    """评估 RAG 结果"""
    # 加载 RAG 结果
    with open(input_json, 'r', encoding='utf-8') as f:
        rag_results = json.load(f)
    
    # 初始化评估器
    evaluator = RAGEvaluator()
    
    # 评估每个结果
    evaluations = []
    for result in rag_results:
        evaluation = evaluator.evaluate(
            result['question'],
            {"answer": result['rag_answer']},
            []
        )
        evaluations.append({
            "question": result['question'],
            "rag_answer": result['rag_answer'],
            "evaluation": evaluation
        })
    
    # 保存评估结果
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, ensure_ascii=False, indent=2)
    
    print(f"评估结果已保存: {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", required=True, help="RAG 结果文件路径")
    parser.add_argument("--output_json", required=True, help="评估结果输出文件路径")
    args = parser.parse_args()
    
    evaluate_rag_results(args.input_json, args.output_json)
