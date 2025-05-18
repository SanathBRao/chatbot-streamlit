import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64

# --- Configure API key ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- Page config ---
st.set_page_config(page_title="Gemini Chat + Image Generator", layout="centered")
st.title("🤖 Gemini Chat + 🖼️ Image Generator (Combined)")

# --- Chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat input ---
user_input = st.text_input("Ask something or describe an image to generate:")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Generating text + image response..."):
        try:
            # Initialize Gemini image+text model
            model = genai.GenerativeModel("models/gemini-2.0-flash-preview-image-generation")

            # Call generate_content with both text + image response modalities
            response = model.generate_content(
                contents=[{"text": user_input}],
                generation_config={
                    "response_modalities": ["TEXT", "IMAGE"]
                },
                stream=False
            )

            # Extract and show chatbot text reply & image(s)
            text_response = ""
            images = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    text_response += part.text + "\n"
                elif hasattr(part, "inline_data") and part.inline_data.data:
                    image_data = base64.b64decode(part.inline_data.data)
                    image = Image.open(BytesIO(image_data))
                    images.append(image)

            # Show text
            if text_response.strip():
                st.markdown("### 🤖 Gemini says:")
                st.write(text_response.strip())

            # Show images
            if images:
                st.markdown("### 🖼️ Generated Image(s):")
                for i, img in enumerate(images):
                    st.image(img, use_column_width=True)
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format="PNG")
                    st.download_button(f"Download Image {i+1}", img_byte_arr.getvalue(), file_name=f"generated_image_{i+1}.png")
            else:
                st.warning("No images generated for this prompt.")

            # Add assistant reply to chat history (text only)
            st.session_state.chat_history.append({"role": "assistant", "content": text_response.strip()})

        except Exception as e:
            st.error(f"Error generating content: {e}")

# --- Show previous chat messages ---
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### Chat History")
    for msg in st.session_state.chat_history:
        role = "User" if msg["role"] == "user" else "Gemini"
        st.markdown(f"**{role}:** {msg['content']}")
