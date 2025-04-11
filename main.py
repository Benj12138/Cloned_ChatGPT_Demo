import streamlit as st
from utils import get_chat_response
from langchain_community.chat_message_histories import ChatMessageHistory

left, right = st.columns([2,1],vertical_alignment="bottom")
with left:
    st.title("克隆ChatGPT")
with right:
    if st.button("🗑️清除对话并重新开始"):
        st.session_state["memory"] = ChatMessageHistory()
        st.session_state["messages"] = [{"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮助你的？"}]
        st.rerun()

with st.sidebar:
    openai_api_key = st.text_input("请输入API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ChatMessageHistory()
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮助你的？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入OpenAI API KEY")
        st.stop()
    else:
        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍后..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)

