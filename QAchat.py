from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
import os


import google.generativeai as genai

# Configure Generative AI with API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize Generative AI model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Function to get response from Generative AI
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit App
st.set_page_config(page_title="Gaurav's Chatbot")
st.header("ChatBot")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input
user_input = st.text_input("Input:", key="input")
submit_button = st.button("Ask the question")

# Process user input and display response
if submit_button and user_input:
    response = get_gemini_response(user_input)
    st.session_state["chat_history"].append(("You", user_input))
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("BOT", chunk.text))

# Display chat history
st.subheader("The chat history is ")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")

    
    
    
    
    
