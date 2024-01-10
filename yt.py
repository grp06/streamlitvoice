import os
import streamlit as st

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def yt_wrapper():
    st.title('YouTube Video Downloader, Trimmer and Resizer')

    url = st.text_input("Enter a YouTube URL", value=st.session_state.get("url", ""))
    start_time = st.text_input("Enter the start time (format: MM:SS)", value=st.session_state.get("start_time", ""))
    end_time = st.text_input("Enter the end time (format: MM:SS)", value=st.session_state.get("end_time", ""))

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

            # Crop the video to the desired aspect ratio
            cropped_clip = clip.crop(x_center=clip.w/2, width=width)

            resized_output_path = f"{trimmed_output_path.rsplit('.', 1)[0]}_resized.mp4"
            cropped_clip.write_videofile(resized_output_path)

            st.success(f'Video downloaded, trimmed and resized successfully at {resized_output_path}')

        except Exception as e:
            st.error(f'Error: {e}')

    # Save the current state
    st.session_state.url = url
    st.session_state.start_time = start_time
    st.session_state.end_time = end_time