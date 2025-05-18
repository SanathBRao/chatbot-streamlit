import streamlit as st
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Streamlit page setup
st.set_page_config(page_title="Gemini Chatbot + Image Generator", layout="centered")
st.title("🤖 Gemini Chatbot + 🎨 Image Generator")

# Set Gemini API Key
import os
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
# --- Chatbot Section ---
st.subheader("💬 Chat with Gemini")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Display previous messages
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if isinstance(msg, (HumanMessage, AIMessage)):
        with st.chat_message(role):
            st.markdown(msg.content)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = llm.invoke(st.session_state.chat_history)
            st.markdown(result.content)
            st.session_state.chat_history.append(AIMessage(content=result.content))

