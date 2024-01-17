import os
import streamlit as st
from openai import OpenAI



def gpt4_wrapper(api_key):
    st.title('GPT-4 Prompt')
    client = OpenAI(api_key=api_key)
    # System prompt text input
    system_prompt = st.text_area("Enter your system prompt:", value="You are a helpful assistant.")

    # User prompt text input
    user_prompt = st.text_area("Enter your user prompt:")

    # Button for sending prompts
    if st.button('Submit Prompts'):
        if user_prompt:
            try:
                # OpenAI GPT-4 API call with system and user prompts
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )

                # Append the result as text in the browser
                st.text(response.choices[0].message.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a user prompt.")