import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from openai import AsyncOpenAI
import tempfile

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
print(OPENAI_API_KEY)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
st.title('Text to Speech Conversion')

# Text input
user_input = st.text_area("Enter the text you want to convert to speech:")

# Button for conversion
if st.button('Convert to Speech'):
    if user_input:
        try:
            # OpenAI TTS API call
            async def create_speech():
                response = await client.audio.speech.create(
                    model="tts-1-hd",
                    voice="onyx",
                    input=user_input,
                )
                return response

            response = asyncio.run(create_speech())

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