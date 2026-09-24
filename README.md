民航机务维修排故智能助手 Aircraft Troubleshooting Agent

项目简介
本项目是一个基于多源数据与大语言模型LLM的民航机务维修排故智能助手。旨在帮助机务维修人员快速定位飞机故障、高效检索维修手册，并提供智能化的排故建议，从而提升一线维修效率，降低人为差错

核心功能
智能问答与排故引导：基于大模型，针对机务人员的自然语言提问给出专业的排故指导
知识库检索 (RAG)：导入《民航机务维修排故手册》等PDF文档，结合向量数据库（FAISS），实现精准的知识检索增强生成
工具调用：内置机务维修专用工具，可辅助完成特定排故计算或信息查询
多轮对话记忆：支持上下文对话，能够记住之前的排故步骤，提供连贯的维修建议
交互式前端界面：提供基于现代前端框架的聊天交互界面，操作直观

技术栈
后端 Backend
语言：Python 3.10+
框架：FastAPI/Flask 
LLM 编排：LangChain
向量数据库：FAISS
数据库：MySQL
核心依赖：requirements.txt

前端 Frontend
框架：Vue 3 + Vite
语言：JavaScript / TypeScript
核心目录：frontend/ai-assistant

项目结构
aircraft-troubleshooting-agent/
├── .gitignore
├── README.md
├── backend/                     后端服务与AI Agent逻辑
│   ├── .env.example             环境变量示例
│   ├── requirements.txt         Python依赖
│   ├── app.py / main.py         后端入口
│   ├── config.py                配置文件
│   ├── agent_builder.py         Agent构建逻辑
│   ├── vector_store.py          向量数据库操作
│   ├── knowledge/               知识库
│   └── tools/                   自定义工具
└── frontend/                    前端Vue项目
    └── ai-assistant/
        ├── package.json
        └── src/
快速开始

1）后端启动
```
#进入后端目录
cd backend
```
```
#创建并激活虚拟环境 (Windows)
python -m venv .venv
.venv\Scripts\activate
```
```
#安装依赖
pip install -r requirements.txt
```
```
#配置环境变量
#复制.env.example为.env填入你的API Key和数据库密码
cp .env.example .env
```
```
#启动后端
python main.py
```
2）前端启动
```
#进入前端目录
cd frontend/ai-assistant
```
```
#安装依赖
npm install
```
```
#启动开发服务器
npm run dev
```
