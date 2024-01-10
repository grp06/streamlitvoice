import streamlit as st
from tts import tts_wrapper
from yt import yt_wrapper

st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", ['AI Voices', 'Clip YouTube'])

if page == 'AI Voices':
    tts_wrapper()
elif page == 'Clip YouTube':
    yt_wrapper()