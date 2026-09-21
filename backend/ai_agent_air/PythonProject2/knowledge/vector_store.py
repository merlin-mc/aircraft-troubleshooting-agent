import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config import (
    ZHIPU_API_KEY,
    ZHIPU_API_URL,
    ZHIPU_EMBEDDED_MODEL,
    KB_INDEX_DIR,
    KB_PDF_PATH
)

def build_embeddings():
    """
    构建嵌入模型
    """
    return OpenAIEmbeddings(
        model=ZHIPU_EMBEDDED_MODEL,
        api_key=ZHIPU_API_KEY,
        base_url=ZHIPU_API_URL,
        check_embedding_ctx_length=False  
    )
def split_docs(docs):
    """
    拆分文档
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  
        chunk_overlap=50,  
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]  
    )
    return splitter.split_documents(docs)  

def build_knowledge_base():
    """构建知识库
    """
    if not os.path.exists(KB_PDF_PATH):
        raise FileNotFoundError(f"知识库文档不存在：{KB_PDF_PATH}")
    print(f"开始加载文档：{KB_PDF_PATH}")
    docs = PyPDFLoader(KB_PDF_PATH).load()
    print(f"文档加载完成：共{len(docs)}页")

    chunks = split_docs(docs)
    print(f"文档切分完成：共{len(chunks)}个片段")

    embeddings = build_embeddings()  
    vector_store = FAISS.from_documents(docs, embeddings)  
    vector_store.save_local(KB_INDEX_DIR)  
    print(f"知识库创建完成：共{vector_store.index}个片段")
    return vector_store

_vector_store = None

def get_vector_store():
    """
    单例获取知识库
    """
    global _vector_store
    if _vector_store is None:
        if os.path.exists(os.path.join(KB_INDEX_DIR, "index.faiss")):
            _vector_store = FAISS.load_local(
                KB_INDEX_DIR,
                build_embeddings(),
                allow_dangerous_deserialization=True,
            )
        else:
            _vector_store = build_knowledge_base()  
    return _vector_store

def search_knowledge_base(question: str, top_k: int = 5) -> str:  
    """
    查询知识库,返回前5个最相关的文档
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(question, k=top_k)
    if not results:  
        return "知识库中未找到相关内容"
    
    return "\n-------------\n".join(
        f"[片段{i+1}](来源：第{doc.metadata.get('page', -1) + 1}页) \n{doc.page_content}"
        for i, doc in enumerate(results)
    )  



