"""
后端接口：用于前后端联调
FastApi框架
"""
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
app = FastAPI(title="后端接口", description="用于前后端联调", version="1.0.0") 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True, 
)
@app.get("/test") 
async def test():
    """
    测试接口
    :return: 一般都是返回字符串值或JSON对象值
    """
    return {"msg": "hello world"}
from fastapi.responses import StreamingResponse 
from agent import default_agent
@app.get("/chat/stream")  
async def stream_chat(message: str, conversationId: str = None):
    """
    流式接口，调用智能体模块
    :param message: 用户输入
    :param conversationId: 会话ID
    :return: 流式响应结果
    """
    agent = default_agent()
    return StreamingResponse(
        agent.stream_response(message, conversationId), 
        media_type="text/plain;charset=utf-8"
    )


