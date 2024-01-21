# yt.py
import os
import streamlit as st

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import subprocess
from datetime import datetime

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
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base_output_path = f"{output_path.rsplit('.', 1)[0]}_{timestamp}"

            trimmed_output_path = f"{base_output_path}_trimmed.mp4"
            resized_output_path = f"{base_output_path}_resized.mp4"

            # Use ffmpeg command directly to trim the video
            subprocess.call([
                'ffmpeg', '-i', output_path,
                '-ss', str(start_time_sec),
                '-to', str(end_time_sec),
                '-c:v', 'libx264', '-preset', 'slow',
                '-c:a', 'aac', '-b:a', '192k',
                '-strict', '-2',  # This may be necessary if aac is not enabled by default
                trimmed_output_path
            ])
            clip = VideoFileClip(trimmed_output_path)
            video_height = clip.size[1]
            target_width = int(video_height * (9 / 16))
            target_height = video_height
            
            crop_filter = ''
            if crop_option == '1':
                # Crop starting 10% from the left side of the screen
                crop_x = int(clip.size[0] * .05)  # 10% from the left
                crop_filter = f'crop={target_width}:{target_height}:{crop_x}:0'
            elif crop_option == '2':
                # Crop the center of the screen
                crop_x = (clip.size[0] - target_width) // 2
                crop_filter = f'crop={target_width}:{target_height}:{crop_x}:0'
            elif crop_option == '3':
                # Crop out the right side of the screen
                crop_x = clip.size[0] - target_width
                crop_filter = f'crop={target_width}:{target_height}:{crop_x}:0'

            resized_output_path = f"{trimmed_output_path.rsplit('.', 1)[0]}_resized.mp4"

            # Use ffmpeg command directly to crop and resize the video
            subprocess.call([
                'ffmpeg', '-i', trimmed_output_path,
                '-vf', crop_filter,
                '-c:v', 'libx264', '-preset', 'slow',
                '-c:a', 'copy',
                resized_output_path
            ])


            # Provide a download button for the video
            with open(resized_output_path, "rb") as file:
                btn = st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=f"resized_video_{timestamp}.mp4",
                    mime="video/mp4",
                )

        except Exception as e:
            st.error(f'Error: {e}')

    # Save the current state
    st.session_state.url = url
    st.session_state.start_time = start_time
    st.session_state.end_time = end_time