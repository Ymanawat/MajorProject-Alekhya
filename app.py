import streamlit as st
import os

def save_uploaded_files(uploaded_files):
    for uploaded_file in uploaded_files:
        with open(os.path.join("assets", "videos", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved file: {uploaded_file.name}")

def main():
    st.title("Text and Media Uploader")

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
            save_uploaded_files(media_files)

if __name__ == "__main__":
    if not os.path.exists(os.path.join("assets", "videos")):
        os.makedirs(os.path.join("assets", "videos"))
    main()
