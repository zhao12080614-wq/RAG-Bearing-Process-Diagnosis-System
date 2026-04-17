import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import AgenticRAGPipeline

def main():
    """主函数"""
    try:
        # 初始化 Agentic RAG 流水线
        pipeline = AgenticRAGPipeline()
        
        print("🤖 基于 Agentic RAG 的工业轴承智能诊断系统")
        print("=======================================")
        print("输入您的问题，或输入 'exit' 退出系统")
        print("=======================================")
        
        while True:
            user_query = input("\n用户: ")
            
            if user_query.lower() == 'exit':
                print("系统已退出")
                break
            
            # 处理用户查询
            result = pipeline.process_query(user_query)
            
            # 输出结果
            print("\n系统:")
            if hasattr(result, 'answer'):
                print(result.answer)
            elif hasattr(result, 'explanation'):
                print(result.explanation)
            else:
                print(str(result))
                
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
