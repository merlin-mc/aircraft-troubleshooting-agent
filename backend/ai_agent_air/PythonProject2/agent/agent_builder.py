from langchain_core.messages import SystemMessage, HumanMessage

from langchain_openai import ChatOpenAI
from config import (
    ZHIPU_API_KEY,
    ZHIPU_MODEL_NAME,
    ZHIPU_API_URL,
    MODEL_TEMPERATURE,
    MAX_TOKENS
)
from langchain.messages import (
    SystemMessage,
    ToolMessage
)
from memory.chat_memory import get_session_history
from prompt_templates import SYSTEM_PROMPT
def build_llm():
    """
    构建LLM模型,使用智谱AI
    :return: 模型对象
    """
    return ChatOpenAI(
        temperature=MODEL_TEMPERATURE,
        model=ZHIPU_MODEL_NAME,
        api_key=ZHIPU_API_KEY,
        base_url=ZHIPU_API_URL,
        max_tokens=MAX_TOKENS,
        streaming=True  
    )
from tools import TOOLS 
class AIAgent:
    """
    智能体类
    """
    def __init__(self):
        self.llm = build_llm() 
        self.llm_with_tools = self.llm.bind_tools(TOOLS)
        self.system_prompt = SYSTEM_PROMPT
    async def stream_response(
            self,
            user_input:str,
            session_id:str 
    ):
        """
        :param user_input: 用户输入
        :param session_id: 会话ID
        思路：
        1.每次开始对话时，都应该先尝试从数据库获取历史消息，
        2.并将历史加入本次对话的消息列表中
        3.将新的用户信息和AI响应的信息新增到数据库中
        """
        chat_history = get_session_history(session_id)
        history_messages=  chat_history.messages 
        messages:list = [
            SystemMessage(content=self.system_prompt),
        ]
        messages.extend(history_messages)
        user_msg = HumanMessage(content=user_input)
        messages.append(user_msg)
        chat_history.add_message(user_msg)
        full_content = ""
        try:
            resp = await self.llm_with_tools.ainvoke(messages) 
            
            if not resp.tool_calls:
                async for chunk in self.llm.astream(messages): 
                    token = chunk.content  
                    if token:
                        full_content += token  
                        yield token     
            else:
                
                print(resp)
                messages.append(resp) 
                
                chat_history.add_message(resp)
               
                for tool_call in resp.tool_calls:         
                    tool = next((t for t in TOOLS if t.name == tool_call['name']), None)
                    tool = next((t for t in TOOLS if t.name == tool_call['name']), None)
                    if tool is None:
                        print(f"⚠️ 模型请求了不存在的工具: {tool_call['name']}")
                        continue

                    tool_result = await tool.ainvoke(tool_call['args'])
                    tool_msg = ToolMessage(content=tool_result,tool_call_id= tool_call['id'])
                    messages.append(tool_msg)
                    chat_history.add_message(tool_msg)
                else:
                    async for chunk in self.llm.astream(messages):  
                        token = chunk.content  
                        if token:
                            full_content += token  
                            yield token  
        except Exception as e:
            print(f"流式响应输出失败,异常信息：{e}")
            yield "服务器异常！！"
        try:
            chat_history.add_ai_message(full_content) 
        except Exception as e:
            print(f"本次模型响应消息存储失败,异常信息：{e}")
def get_default_agent():
    """
    获取默认智能体实例
    :return: AIAgent实例
    """
    return AIAgent()