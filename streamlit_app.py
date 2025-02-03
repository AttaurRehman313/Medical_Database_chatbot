
import streamlit as st
import requests
import re
import json

# Set up the app's title
st.title("Chatbox-Integration-bot")

# Initialize session state variables if they don't exist
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = ''
if 'prev_user_id' not in st.session_state:
    st.session_state['prev_user_id'] = ''

# Function to send user query to Flask API and get a response
def get_response(query, user_id):
    try:
        # Include user_id in the payload if it's provided
        payload = {'user_query': query}
        if user_id:
            payload['user_id'] = user_id
        response = requests.post('http://aidrawing.rentaghr.com/askdb', json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response found in the JSON.")
        else:
            return "Sorry, there was an error."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to clean the HTML response (if needed)
def clean_response(response):
    cleaned_response = re.sub(r'<\/?div[^>]*>', '', response)  # Removes <div> tags
    return cleaned_response.strip()

# Function to display a chat message with custom styles for user and assistant
def display_message(role, content):
    if role == "user":
        st.markdown(f"""
            <div style="text-align: right; color: black; background-color: #8db698; padding: 10px; border-radius: 10px; margin: 10px 0; width: fit-content; float: right; clear: both;">
                {content}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="text-align: left; color: black; background-color: #bddabb; padding: 10px; border-radius: 10px; margin: 10px 0; width: fit-content; float: left; clear: both;">
                {content}
            </div>
            """, unsafe_allow_html=True)

# Sidebar for user ID input
# with st.sidebar:
#     user_id = st.text_input("Enter your User ID :", value=st.session_state['user_id'])

# # Check if the user ID has changed
# if user_id != st.session_state['prev_user_id']:
#     # User ID has changed, reset the chat history
#     st.session_state['messages'] = []
#     st.session_state['prev_user_id'] = user_id  # Update the previous user ID
#     st.session_state['user_id'] = user_id
#     st.rerun()  # Rerun the app to reflect changes

# else:
#     # Update the user ID in session state
#     st.session_state['user_id'] = user_id

#     # Display chat messages from history
#     for message in st.session_state.messages:
#         display_message(message["role"], message["content"])

#     # Accept user input
#     if prompt := st.chat_input("Enter your query..."):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Display user message
#         display_message("user", prompt)

#         # Show spinner while fetching the response
#         with st.spinner("loading..."):
#             # Get the AI response, passing the user_id if provided
#             ai_response = get_response(prompt, st.session_state['user_id'])
#             ai_response_cleaned = clean_response(ai_response)

#         # Add AI response to chat history
#         st.session_state.messages.append({"role": "assistant", "content": ai_response_cleaned})

#         # Display AI response
#         display_message("assistant", ai_response_cleaned)


with st.sidebar:
    user_id = st.text_input("Enter your User ID :", value=st.session_state.get('user_id', ''))

# Check if user_id is missing
if not user_id:
    st.warning("User ID is missing, please enter your User ID to chat.")
else:
    # Check if the user ID has changed
    if user_id != st.session_state.get('prev_user_id', ''):
        # User ID has changed, reset the chat history
        st.session_state['messages'] = []
        st.session_state['prev_user_id'] = user_id  # Update the previous user ID
        st.session_state['user_id'] = user_id
        st.rerun()  # Rerun the app to reflect changes

    else:
        # Update the user ID in session state
        st.session_state['user_id'] = user_id

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
                # Get the AI response, passing the user_id if provided
                ai_response = get_response(prompt, st.session_state['user_id'])
                ai_response_cleaned = clean_response(ai_response)

            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response_cleaned})

            # Display AI response
            display_message("assistant", ai_response_cleaned)

