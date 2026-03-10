import streamlit as st
from langchain_core.messages import HumanMessage

from gmail_agent.client.graph import app

st.set_page_config(page_title="Gmail AI Assistant", page_icon="📧")
st.title("Akin's Gmail Assistant")
st.markdown("How can I help you today? (e.g., 'Read my latest emails' or 'Send an email to John about the meeting')")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking and connecting to Gmail..."):
            input_message = HumanMessage(content=prompt)
            
            config = {"configurable": {"thread_id": "1"}}
            
            result = app.invoke({"messages": [input_message]}, config=config)
            
            final_response = result["messages"][-1].content
            
            st.markdown(final_response)
            
            st.session_state.messages.append({"role": "assistant", "content": final_response})