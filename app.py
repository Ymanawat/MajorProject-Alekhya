import time
import streamlit as st
import os
import requests

def save_uploaded_files(uploaded_files):
    for uploaded_file in uploaded_files:
        with open(os.path.join("assets", "videos", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved file: {uploaded_file.name}")

def main():
    st.title("Alekhyaa - Text to video solution")
    delete_all_files_in_directory()
    delete_files()

    # Textarea for entering text
    text_input = st.text_area("Enter your text here:")

    # File uploader for images and videos
    media_files = st.file_uploader("Upload Images or Videos", type=['jpg', 'jpeg', 'png', 'gif', 'mp4'], accept_multiple_files=True)

    if st.button("Submit"):
        if text_input:
            st.write("Entered Text:", text_input)
        if media_files:
            for media_file in media_files:
                file_details = {"FileName": media_file.name, "FileType": media_file.type}
                st.write(file_details)
                if 'image' in media_file.type:
                    st.image(media_file, caption='Uploaded Image', use_column_width=True)
                elif 'video' in media_file.type:
                    st.video(media_file)

        # Make API POST request
        api_url = "http://localhost:8000/convert-to-video"
        response = requests.post(api_url, json={"script": text_input})
        print(response)

        if response.status_code == 200:
            st.write("API request successful. Processing...")
        else:
            st.write("Error: API request failed.")
            return

        # Continuous checking for output video
        while True:
            output_video_path = os.path.join("output_video.mp4")
            if os.path.exists(output_video_path):
                st.video(output_video_path)
                break  # Exit the loop once the video is found
            else:
                st.write("Processing your input...")
                time.sleep(1)  # Adjust the sleep duration as needed

        # save_uploaded_files(media_files)  

def delete_files(files=["output_video.mp4", "temp.wav", "final_audio_with_pauses.mp3", "pause_durations.json"]):
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

def delete_all_files_in_directory(directory='assets/videos'):
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting files in directory {directory}: {e}")

    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting files in directory {directory}: {e}")


if __name__ == "__main__":
    if not os.path.exists(os.path.join("assets", "videos")):
        os.makedirs(os.path.join("assets", "videos"))
    main()
