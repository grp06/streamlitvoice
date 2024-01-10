import os
import streamlit as st
from openai import OpenAI

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


prompt = '''
Your the worlds top prompt engineer specialized at writing prompts for Dall E 3. Your job is to take a users prompt and make it professional. 



Your response should simply take the users input and add some details to it to make it a professional prompt. Do not add any unnecessary objects, or anything that the user did not mention.

Reply only with the rewritten prompt and nothing else. Only provide 1 version. 


Do not put anything like this: "Certainly! Here are the enhanced versions of the user-provided prompts:"

'''
 
def img_gen_wrapper():
    st.title('Image Generation')

    # Text input
    image_prompt = st.session_state.get("image_prompt", "")
    enhanced_prompt = st.session_state.get("enhanced_prompt", image_prompt)

    # Create a placeholder for the text area
    text_area_placeholder = st.empty()

    # Display the text area in the placeholder
    st.session_state.image_prompt = text_area_placeholder.text_area("Enter image prompt:", value=enhanced_prompt)

    # Enhance Prompt button
    if st.button('Enhance Prompt'):
        try:
            # Placeholder for GPT-4 prompt enhancement
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "system", "content": prompt}],
                stream=False,
            )
            enhanced_prompt = response.choices[0].message.content
            print(enhanced_prompt)
            # Set the enhanced prompt as the value in the text area
            st.session_state.enhanced_prompt = enhanced_prompt

            # Update the text area with the enhanced prompt
            st.session_state.image_prompt = text_area_placeholder.text_area("Enter image prompt:", value=enhanced_prompt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Button for generation
    if st.button('Generate Image'):
        if st.session_state.image_prompt:
            try:
                # OpenAI DALL·E 3 API call
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=st.session_state.image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                # Display image
                st.image(response.data[0].url)

                # Provide a download link
                st.markdown(f"[Download Generated Image]({response.data[0].url})")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter an image prompt.")