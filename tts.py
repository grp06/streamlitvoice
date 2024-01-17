import os
import asyncio
import streamlit as st
from openai import OpenAI
import tempfile


async def create_speech(user_input, selected_voice,api_key):
    client = OpenAI(api_key=api_key)
    response = await client.audio.speech.create(
        model="tts-1-hd",
        voice=selected_voice,
        input=user_input,
    )
    return response

def tts_wrapper(api_key):
    st.title('Text to Speech Conversion')


    # Text input
    user_input = st.text_area("Enter the text you want to convert to speech:", value=st.session_state.get("user_input", ""))
    # Voice selection
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    selected_voice = st.selectbox("Select a voice:", voices, index=voices.index(st.session_state.get("selected_voice", "alloy")))

    # Button for conversion
    if st.button('Convert to Speech'):
        if user_input:
            try:
                # OpenAI TTS API call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(create_speech(user_input, selected_voice, api_key))

                # Save the response (audio data) to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp.write(response.read())
                    tmp_path = tmp.name

                # Display audio player
                st.audio(tmp_path, format='audio/mp3', start_time=0)

                # Provide a download link
                st.markdown(f"[Download Speech Audio]({tmp_path})")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter some text to convert.")

    # Save the current state
    st.session_state.user_input = user_input
    st.session_state.selected_voice = selected_voice