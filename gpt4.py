import os
import streamlit as st
from openai import OpenAI

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def gpt4_wrapper():
    st.title('GPT-4 Prompt')

    # Text input
    user_prompt = st.text_area("Enter your prompt:")

    # Button for sending prompt
    if st.button('Submit Prompt'):
        if user_prompt:
            try:
                # OpenAI GPT-4 API call
                response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[{"role": "user", "content": user_prompt}]
                )

                # Append the result as text in the browser
                st.text(response.choices[0].message.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a prompt.")