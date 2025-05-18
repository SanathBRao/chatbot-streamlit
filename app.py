import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# --- Set up API key securely ---
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# --- Page config ---
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini Chatbot")

# --- Initialize model ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- Initialize chat history in session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# --- Display previous chat messages ---
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if isinstance(msg, (HumanMessage, AIMessage)):
        with st.chat_message(role):
            st.markdown(msg.content)

# --- Chat input ---
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(st.session_state.chat_history)
            st.markdown(response.content)

    # Add assistant response to chat history
    st.session_state.chat_history.append(AIMessage(content=response.content))
