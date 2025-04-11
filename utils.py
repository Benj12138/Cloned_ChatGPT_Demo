# from langchain_openai import ChatOpenAI
# from langchain.chains import ConversationChain
#
# from langchain.memory import ConversationBufferMemory
# import os
#
# def get_chat_response(prompt, conversation_memory, openai_api_key):
#     model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
#     chain = ConversationChain(llm=model, memory=conversation_memory)
#
#     response = chain.invoke({"input":prompt})
#     return  response["response"]
#
# memory = ConversationBufferMemory(return_messages=True)
# print(get_chat_response(prompt="爱因斯坦提出过哪些知名的定律？", conversation_memory=memory,  openai_api_key=os.getenv("OPENAI_API_KEY")))
# print(get_chat_response(prompt="我上一个问题问了什么？", conversation_memory=memory,  openai_api_key=os.getenv("OPENAI_API_KEY")))

#环境变量API_KEY
# from langchain_openai import ChatOpenAI
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# import os
#
# # 定义提示模板（包含历史消息占位符）
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个友好的助手。"),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{input}")
# ])
#
# # 初始化模型
# model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
#
# # 创建链式处理流程
# chain = prompt | model
#
# # 初始化消息历史存储
# message_history = ChatMessageHistory()
#
# # 绑定消息历史到链
# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     lambda session_id: message_history,
#     input_messages_key="input",
#     history_messages_key="history"
# )
#
# # 定义获取响应的函数
# def get_chat_response(user_input, memory):
#     response = chain_with_history.invoke(
#         {"input": user_input},
#         config={"configurable": {"session_id": "unused"}}
#     )
#     memory.add_user_message(user_input)        # 记录用户输入
#     memory.add_ai_message(response.content)  # 记录AI响应
#     return response.content
#
# # 使用示例
# # print(get_chat_response("牛顿提出过哪些知名的定律？", message_history))
# # print(get_chat_response("我上一个问题问了什么？", message_history))

# 动态变量API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 全局提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 初始化消息历史存储（全局）
message_history = ChatMessageHistory()

# 定义获取响应的函数（增加 api_key 参数）
def get_chat_response(user_input, memory, openai_api_key):
    # 根据传入的 api_key 动态创建模型
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    # 创建链式处理流程（每次调用重新绑定）
    chain = prompt | model
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="history"
    )
    # 调用链并记录历史
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "unused"}}
    )
    memory.add_user_message(user_input)
    memory.add_ai_message(response.content)
    return response.content

# 使用示例（直接传入密钥）
#api_key = "sk-your-actual-api-key-here"
# print(get_chat_response("贝多芬有哪些代表作？", message_history, openai_api_key=api_key))
# print(get_chat_response("我上一个问题问了什么？", message_history, openai_api_key=api_key))
