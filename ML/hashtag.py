import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import textwrap

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')


def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)


def generate_content(image):
    response = model.generate_content(["The images are about a cafe. Give me caption for this image to use as a post and hashtags that I can use this image to increase my social media reach. The response should always be in English.", image], stream=True)
    response.resolve()
    ans = to_markdown(response.text)
    custom_hashtags = ["#Ettarra", "#Anna.Kaapi", "#Tamma.Kaapi"]
    ans += "  ".join(custom_hashtags)
    return ans


# Streamlit App
st.title("AI Image Caption and Hashtags Generator")

# Upload image through Streamlit
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Button to generate caption and hashtags
    if st.button("Generate Caption and Hashtags"):
        # Perform generation and display the result
        st.markdown(generate_content(image))
