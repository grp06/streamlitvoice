import streamlit as st
from tts import tts_wrapper
from yt import yt_wrapper
from img_gen import img_gen_wrapper
st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", ['AI Voices', 'Clip YouTube', 'Image Generator'])

if page == 'AI Voices':
    tts_wrapper()
elif page == 'Clip YouTube':
    yt_wrapper()
elif page == 'Image Generator':
    img_gen_wrapper()