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
st.set_page_config(page_title="Gaurav's Chatbot", page_icon=":robot_face:")

# Set the app layout
st.title("ChatBot")

# Add background color using custom CSS
bg_color = "#0000FF"  # You can change this to your desired color
st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# User input
user_input = st.text_input("Input:")
submit_button = st.button("Ask the question")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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

# Add some styling to the sidebar
logo_path = '(stablediffusionai.org)-1695064643-2.png'  
st.sidebar.image(logo_path, output_format='PNG')
st.sidebar.markdown("Hey There , My Name is Gaurav")
st.sidebar.subheader("About")
st.sidebar.markdown("This is a chatbot powered by Google Gemini API.")