import streamlit as st
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import base64

# --- Set up Gemini API key ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- Streamlit page config ---
st.set_page_config(page_title="Gemini Image Generator", layout="centered")
st.title("🎨 Image Generator using Google Gemini")

# --- Prompt input ---
image_prompt = st.text_area("Enter your image prompt", placeholder="e.g. Virat Kohli lifts IPL trophy")

if st.button("Generate Image"):
    if not image_prompt.strip():
        st.warning("Please enter a valid prompt.")
    else:
        with st.spinner("Generating image using Gemini..."):
            try:
                # Load the Gemini model
                model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # Note: no public image model as of now

                # ⚠️ THIS IS A PLACEHOLDER – image generation may require a different model
                # Use a preview model if your account has access (e.g. models/gemini-2.0-flash-preview-image-generation)
                response = model.generate_content(
                    contents=[{"text": image_prompt}],
                    generation_config={"response_mime_type": "image/png"},
                    stream=False
                )

                # Process response (this part may differ based on Gemini's image response structure)
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text") and part.text:
                        st.subheader("Text Response")
