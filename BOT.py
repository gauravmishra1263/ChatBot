from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from markdown import Markdown
 



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def get_gemini_response_image(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text


st.header("Gaurav's Chatbot 👾")
logo_path = '(stablediffusionai.org)-1695064643-2.png'  

st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
# Set sidebar padding to 0
st.markdown("<style>div[data-testid='stSidebar'] div.stBlock {padding-top: 0;}</style>", unsafe_allow_html=True)
#st.sidebar.image(logo_path, output_format='PNG')

with st.sidebar:
   
    
    st.header("Text as input")
    
    text_input_prompt =st.text_input("Enter the prompt: ",key="input")
    st.markdown("<h1 style='text-align: center;'>(or)</h1>", unsafe_allow_html=True)
    st.header("Text+ Image as input")
    img_input_prompt =st.text_input("Enter the prompt: ",key="input1")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"]) or st.camera_input("Take a picture")
     
    image="" 
    submit=st.button("Generate response")
    



if submit:
    if text_input_prompt:
        response=get_gemini_response(text_input_prompt)
        st.subheader("Generated response:")
        st.session_state["chat_history"].append(("You",text_input_prompt ))
        st.write(response)
        st.session_state["chat_history"].append(("BOT", response))
    elif uploaded_file:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
        st.subheader("Generated response:")
        response=get_gemini_response_image(img_input_prompt,image)
        st.session_state["chat_history"].append(("You",img_input_prompt ))
        st.write(response)
        st.session_state["chat_history"].append(("BOT", response))
        
    
st.divider()

# Display chat history
st.subheader(" Chat History  ")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
    
    
    

