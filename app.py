import streamlit as st
st.title("DEMO CHATBOT")
import os
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]
# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Say something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call OpenAI API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.markdown(reply)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": reply})
