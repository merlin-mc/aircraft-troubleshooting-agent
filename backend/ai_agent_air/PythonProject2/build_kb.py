"""
用于初始构建知识库，实际开发中，可以借助FastAPI接口，使用前端请求构建
"""
from knowledge import build_knowledge_base
if __name__ == '__main__':
    build_knowledge_base()