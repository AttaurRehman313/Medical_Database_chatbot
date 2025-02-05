
import streamlit as st
import requests
import re

# Set up the app's title
st.title("CHI-TECH-Medical-bot")

# Initialize session state variables if they don't exist
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to send user query to Flask API and get a response
def get_response(query):
    try:
        payload = {'query': query}
        response = requests.post('http://127.0.0.1:5000/askdb', json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response found in the JSON.")
        else:
            return "Sorry, there was an error."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to clean the HTML response (if needed)
def clean_response(response):
    cleaned_response = re.sub(r'<\/?.*?>', '', response)  # Removes all HTML tags
    return cleaned_response.strip()

# Function to display a chat message with custom styles for user and assistant
def display_message(role, content):
    align = "right" if role == "user" else "left"
    background = "#8db698" if role == "user" else "#bddabb"
    st.markdown(f"""
        <div style="text-align: {align}; color: black; background-color: {background}; 
        padding: 10px; border-radius: 10px; margin: 10px 0; width: fit-content; 
        float: {align}; clear: both;">
            {content}
        </div>
    """, unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Accept user input
if prompt := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    display_message("user", prompt)

    # Show spinner while fetching the response
    with st.spinner("loading..."):
        ai_response = get_response(prompt)
        ai_response_cleaned = clean_response(ai_response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response_cleaned})

    # Display AI response
    display_message("assistant", ai_response_cleaned)
