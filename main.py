import streamlit as st
from tts import tts_wrapper
from yt import yt_wrapper
from img_gen import img_gen_wrapper
from gpt4 import gpt4_wrapper

# Function to set or get the API key from session state
def set_or_get_api_key():
    # Check if the API key is already set in the session state
    if 'api_key' not in st.session_state:
        # If not, set it to None or prompt the user to enter it
        st.session_state.api_key = None
    return st.session_state.api_key

# Sidebar for API key setup
st.sidebar.title('Setup')
# Prompt the user to enter their API key if it's not already set
api_key = st.sidebar.text_input('Enter your OpenAI API key', value=set_or_get_api_key())
# Update the session state with the entered API key
st.session_state.api_key = api_key

st.sidebar.title('Navigation')
# Set 'GPT-4' as the default page
page = st.sidebar.radio("Go to", ['GPT-4', 'AI Voices', 'Clip YouTube', 'Image Generator'], index=0)

if page == 'GPT-4':
    gpt4_wrapper(api_key)
elif page == 'AI Voices':
    tts_wrapper(api_key)
elif page == 'Clip YouTube':
    yt_wrapper(api_key)
elif page == 'Image Generator':
    img_gen_wrapper(api_key)