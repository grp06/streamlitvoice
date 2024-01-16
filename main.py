import streamlit as st
from tts import tts_wrapper
from yt import yt_wrapper
from img_gen import img_gen_wrapper
from gpt4 import gpt4_wrapper  # Import the GPT-4 wrapper function

st.sidebar.title('Navigation')
# Add 'GPT-4' to the list and make it the default page
page = st.sidebar.radio("Go to", ['GPT-4', 'AI Voices', 'Clip YouTube', 'Image Generator'], index=0)

if page == 'GPT-4':
    gpt4_wrapper()
elif page == 'AI Voices':
    tts_wrapper()
elif page == 'Clip YouTube':
    yt_wrapper()
elif page == 'Image Generator':
    img_gen_wrapper()