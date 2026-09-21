"""
聊天记忆存储模块开发
1.创建MySQL存储层SQLChatMessageHistory(官方MySQL存储适配器)
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.chat_message_histories import SQLChatMessageHistory
from config import MYSQL_URL

def _create_chat_history(session_id: str) -> SQLChatMessageHistory:
    """
    返回数据库存储适配器，通过参数id、可以创建或复用SQLChatMessageHistory对象
    :param session_id: 会话id,用于区分不同用户，该参数值是通过前端请求时传入的标识
    :return:
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        table_name= "agent_message_store", 
        connection= MYSQL_URL,  
    )
def get_session_history(session_id: str):
    """
    获取会话历史对象
    :param session_id: 会话id
    :return:
    """
    return _create_chat_history(session_id)

def init_db():
    """
    初始化方法
    """
    _temp = _create_chat_history("test_session_id") 
    del _temp 

if __name__ == '__main__':
    init_db()
    