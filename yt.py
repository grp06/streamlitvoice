# yt.py
import os
import streamlit as st

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def yt_wrapper(api_key):
    
    st.title('YouTube Video Downloader, Trimmer and Resizer')

    url = st.text_input("Enter a YouTube URL", value=st.session_state.get("url", ""))
    start_time = st.text_input("Enter the start time (format: MM:SS)", value=st.session_state.get("start_time", ""))
    end_time = st.text_input("Enter the end time (format: MM:SS)", value=st.session_state.get("end_time", ""))

    # Radio buttons for crop options
    crop_option = st.radio("Select crop option:", ['1', '2', '3'], index=1)

    if st.button('Download, Trim and Resize'):
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            output_path = stream.download()

            start_min, start_sec = map(int, start_time.split(':'))
            end_min, end_sec = map(int, end_time.split(':'))
            start_time_sec = start_min * 60 + start_sec
            end_time_sec = end_min * 60 + end_sec

            trimmed_output_path = f"{output_path.rsplit('.', 1)[0]}_trimmed.mp4"
            ffmpeg_extract_subclip(output_path, start_time_sec, end_time_sec, targetname=trimmed_output_path)

            clip = VideoFileClip(trimmed_output_path)
            height = clip.size[1]
            width = int(height * 9 / 16)  # Calculate width for 9:16 aspect ratio

            # Crop the video based on the selected option
            if crop_option == '1':
                # Crop the left 30% of the screen
                cropped_clip = clip.crop(x1=clip.w * 0.1, width=width)
            elif crop_option == '2':
                # Crop the center for 9:16 aspect ratio
                cropped_clip = clip.crop(x_center=clip.w/2, width=width)
            elif crop_option == '3':
                # Crop the right 30% of the screen
                cropped_clip = clip.crop(x1=clip.w - clip.w * 0.3 - width, width=width)

            resized_output_path = f"{trimmed_output_path.rsplit('.', 1)[0]}_resized.mp4"
            cropped_clip.write_videofile(resized_output_path)

            # Provide a download button for the video
            with open(resized_output_path, "rb") as file:
                btn = st.download_button(
                    label="Download Video",
                    data=file,
                    file_name="resized_video.mp4",
                    mime="video/mp4",
                )

        except Exception as e:
            st.error(f'Error: {e}')

    # Save the current state
    st.session_state.url = url
    st.session_state.start_time = start_time
    st.session_state.end_time = end_time