"""
知识库搭建模块
"""
from knowledge.vector_store import (
    build_knowledge_base,
    get_vector_store,
    search_knowledge_base
)

__all__ = ["build_knowledge_base", "get_vector_store", "search_knowledge_base"]