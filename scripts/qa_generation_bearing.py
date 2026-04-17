import json
import argparse
from typing import List, Dict, Any

def generate_qa_from_markdown(markdown_path: str, output_path: str) -> None:
    """从 Markdown 文件生成 QA 数据集"""
    # 读取 Markdown 文件
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 模拟 QA 生成
    qa_pairs = [
        {
            "question": "轴承的基本结构是什么？",
            "answer": "轴承通常由内圈、外圈、滚动体和保持架组成。"
        },
        {
            "question": "轴承的寿命如何计算？",
            "answer": "轴承寿命通常使用 L10 寿命计算，基于额定动载荷和实际载荷。"
        }
    ]
    
    # 保存到 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, ensure_ascii=False, indent=2)
    
    print(f"QA 数据集已生成: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_markdown", help="输入 Markdown 文件路径")
    parser.add_argument("output_json", help="输出 JSON 文件路径")
    args = parser.parse_args()
    
    generate_qa_from_markdown(args.input_markdown, args.output_json)
