from langchain_openai import ChatOpenAI
from config import (
    ZHIPU_API_KEY,
    ZHIPU_MODEL_NAME,
    ZHIPU_API_URL,
    MODEL_TEMPERATURE,
    MAX_TOKENS)
from langchain.messages import SystemMessage,HumanMessage

from tools import  TOOLS

llm = ChatOpenAI(
    temperature=MODEL_TEMPERATURE,
    model=ZHIPU_MODEL_NAME,
    api_key=ZHIPU_API_KEY,
    base_url=ZHIPU_API_URL,
    max_tokens=MAX_TOKENS
)
llm_with_tools = llm.bind_tools(TOOLS)

messages = [
    SystemMessage(content="你是一个有用的 AI 助手"),
    HumanMessage(content="请介绍一下人工智能的发展历程")
]
response = llm.invoke(messages)
print(response.content)