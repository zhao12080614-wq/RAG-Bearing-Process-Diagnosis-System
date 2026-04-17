# 🏭 基于 Agentic RAG 的工业轴承智能诊断系统 (Industrial Bearing Agentic RAG)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-green.svg)
![LLM](https://img.shields.io/badge/LLM-Qwen%20%7C%20GLM--5.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

本项目是一个专为工业制造场景打造的**多模态 Agentic RAG（检索增强生成）系统**。它打通了工业现场的 **OT数据（如传感器振动信号）** 与企业内部的 **IT知识库（如国家标准、失效分析手册、历史理论书籍）**。通过大模型意图路由、双路召回融合以及严格的幻觉拦截机制，实现了从“工艺参数秒级查询”到“复杂故障归因”的端到端自动化。

## ✨ 核心特性 (Core Features)

- 🧠 **Agentic 意图路由 (Intent Router)**
  - 动态区分“查标准”、“查理论”与“查缺陷”意图。
  - 内置 OT 数据探针（`CWRUSignalAnalyzer`），支持在内存中对 `.mat` 振动信号进行 FFT（快速傅里叶变换），自动提取 RMS、主频等量化特征并注入 LLM 上下文。
- 🔍 **低成本高性能检索 (Custom RRF)**
  - **规避高昂商业授权**：在 Python 后端从零手写 RRF（倒数秩融合）算法，完美替代 Elasticsearch 企业版收费插件。
  - **双路召回**：结合 BM25（国标号、型号等精准字面匹配）与 KNN（文本语义/图像特征向量匹配），大幅提升复杂工业术语的 Top-5 命中率。
- 🛡️ **工业级防幻觉拦截 (Anti-Hallucination & Graceful Degradation)**
  - 采用 **Pydantic** 强类型约束输出格式（`StandardResponse` / `DefectResponse`）。
  - 创新性引入 `is_found` 状态标识。当知识库存在盲区时，系统触发“优雅降级”，强制 LLM 承认“未找到”而非捏造假参数，保障工业场景零容错底线。
- 👁️ **多模态图文共生 (Multimodal Semantic Anchoring)**
  - 针对工业手册中复杂的缺陷图片，离线阶段利用视觉大模型（Qwen-VL）结合图片上下文进行“语义蒸馏”，将失效特征转化为文本存入向量库。配合 `CLIP` 模型，实现极速的“以图搜图”和图文混合检索。
- ⚖️ **全自动质量评测闭环 (LLM-as-a-Judge)**
  - 内置基于代际压制模型（GLM-5.1）的自动化裁判系统，支持对大模型生成的答案进行四维量化打分（忠实度、相关性、正确性、完整性）。

## 📂 项目结构 (Project Structure)

```text
├── data/
│   ├── parsed/             # 解析后的 Markdown 及图片文件
│   └── qa/                 # 自动生成的 QA 测试集及评测报告
├── scripts/
│   ├── qa_generation_bearing.py   # QA 数据集生成器（支持断点续传）
│   ├── run_rag_bearing.py         # Agentic RAG 批量推理执行器
│   └── evaluate_design.py         # LLM-as-a-Judge 自动化评测脚本
├── src/
│   ├── agent/
│   │   └── intent_router.py       # 意图路由器
│   ├── evaluation/
│   │   └── rag_evaluator.py       # GLM-5.1 裁判模型评估类
│   ├── multimodal/
│   │   └── processor.py           # CLIP 多模态图像特征提取
│   ├── signal_processing/
│   │   └── cwru_analyzer.py       # .mat 振动信号分析探针
│   ├── validation/
│   │   └── pydantic_models.py     # Pydantic 结构化数据模型
│   └── pipeline.py                # Agentic RAG 核心流水线 (含手写 RRF)
├── .env.example            # 环境变量配置模板
└── README.md
```

## 🛠️ 安装与配置 (Installation)

1.  **克隆项目与安装依赖**

    ```bash
    git clone https://github.com/zhao12080614-wq/RAG-Bearing-Process-Diagnosis-System.git
    cd RAG-Bearing-Process-Diagnosis-System
    pip install -r requirements.txt
    ```

2.  **启动 Elasticsearch**
    确保本地或远程已安装并启动 Elasticsearch (8.x 版本推荐)，用于文本与向量的混合存储。

3.  **环境变量配置**
    复制 `.env.example` 为 `.env`，并填入你的配置信息：

    ```env
    # LLM 基础配置 (用于生成和路由)
    LLM_MODEL_NAME="qwen-plus"
    LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
    LLM_API_KEY="sk-your-api-key"

    # Embedding 模型配置
    EMBEDDING_MODEL_NAME="text-embedding-v4"
    EMBEDDING_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
    EMBEDDING_API_KEY="sk-your-api-key"

    # 裁判模型配置 (用于自动化评测)
    EVAL_LLM_MODEL_NAME="glm-5.1"
    EVAL_LLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
    EVAL_LLM_API_KEY="your-glm-api-key"

    # 数据库配置
    ELASTICSEARCH_URL="http://localhost:9200"
    INDEX_NAME="bearing_knowledge"

    # 解决国内下载 HuggingFace 模型 (如 CLIP) 超时问题
    HF_ENDPOINT="https://hf-mirror.com"
    ```

## 🚀 快速开始 (Quick Start)

本项目提供了一条完整的**生成 -> 推理 -> 评测**测试链路：

### Step 1: 生成测试 QA 数据集

基于已解析的工业理论文档（如《轴承设计原理》），自动生成包含理论机理与公式推导的测试集。支持增量保存与断点续传。

```bash
python scripts/qa_generation_bearing.py data/parsed/轴承设计原理_marker_fixed.md data/qa/轴承设计原理_qa.json
```

### Step 2: 运行 Agentic RAG 批量推理

加载生成的 QA 数据，系统将利用手写 RRF 算法在知识库中进行双路召回，通过 Pydantic 过滤幻觉，并输出结构化诊断结果。

```bash
python -m scripts.run_rag_bearing --qa_path data/qa/轴承设计原理_qa.json --result_path data/qa/轴承设计原理_qa_result.json
```

### Step 3: LLM-as-a-Judge 质量评测

唤醒 GLM-5.1 裁判模型，针对上一步的 RAG 输出结果进行严格打分，并生成包含详细扣分理由的评估报告。

```bash
python -m scripts.evaluate_design --input_json data/qa/轴承设计原理_qa_result.json --output-json data/qa/轴承设计原理_qa_evaluation.json
```

## 📈 评测维度说明 (Evaluation Metrics)

评估脚本从以下四个维度（1-5分）量化 RAG 系统的表现：

  - **忠实度 (Faithfulness)**：答案是否完全基于检索到的上下文？有无凭空捏造（幻觉）？
  - **相关性 (Relevance)**：答案是否直接回应了用户诉求？
  - **正确性 (Correctness)**：核心语义与真实工业知识/标准答案是否一致？
  - **完整性 (Completeness)**：是否遗漏了推导步骤或关键参数？

## 🤝 贡献与未来计划 (TODOs)

  - [ ] 接入实际工业产线的 MQTT 流数据接口，替代本地 `.mat` 文件解析。
  - [ ] 丰富前端交互界面（Gradio / Streamlit），实现更直观的时序图表可视化。
  - [ ] 支持更多模态，如基于声学特征的异常检测。

欢迎提交 Issue 或 Pull Request！

## 📄 开源协议 (License)

本项目基于 [MIT License](https://www.google.com/search?q=LICENSE) 开源。