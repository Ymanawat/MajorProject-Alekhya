import cv2
import os
import numpy as np
from moviepy.editor import VideoClip, concatenate_videoclips, AudioFileClip, ImageClip, VideoFileClip

# Load default image
default_image = cv2.imread('default_image.jpg')

# Create a blank background video clip
def make_frame(t):  
    # Return default image frame
    return default_image if default_image is not None else np.zeros((1080, 1920, 3), dtype=np.uint8)

# Function to create a video clip from an image file
def create_image_clip(image_path, duration):
    # Extract the filename from the image_path
    filename = os.path.splitext(os.path.basename(image_path))[0]
    
    # Get the directory of the image_path
    directory = os.path.dirname(image_path)
    
    # Iterate through files in the directory
    for file in os.listdir(directory):
        # Extract the filename without extension for each file in the directory
        file_without_extension = os.path.splitext(os.path.basename(file))[0]
        # Check if filename (without extension) matches the name of any file in the directory
        if filename == file_without_extension:
            # Construct the full path for the matching file
            matching_file_path = os.path.join(directory, file)
            # Load the image using the matching file path
            image = ImageClip(matching_file_path, duration=duration)
            return image
    
    # If no matching file is found, return None or handle the error as needed
    return None

def concatenate_videos_with_audio(assets_time_list=[{"time": 1.689, "asset": "welcome.mp4"}, {"time": 5, "asset": None}], output_path="output_video.mp4", files=[], audio_path='final_audio_with_pauses.mp3'):
    print("Starting concatenation process...")
    
    # Initialize variables
    video_clips_to_concatenate = []
    base_path = "assets/videos"
    last_timestamp = 0
    last_non_none_asset = default_image
    audio_clip = None
    duration = None

    # Load the audio clip if provided
    if audio_path is not None:
        print(f"Loading audio file: {audio_path}")
        audio_clip = AudioFileClip(audio_path)
    else:
        audio_clip = None
    
    # Iterate over the indices of the array of objects
    for i in range(len(assets_time_list)):
        # Get the current and next item
        current_item = assets_time_list[i]
        next_item = assets_time_list[i + 1] if i + 1 < len(assets_time_list) else None
        
        # Get the time and asset from the current object
        time = current_item['time']
        asset = current_item['asset']
        
        print(f"Processing asset: {current_item}")
        
        # Calculate the duration for which the current asset will be inserted
        if next_item:
            next_time = next_item['time']
            duration = next_time - time
        else:
            # If there's no next item, use the audio length
            duration = audio_clip.duration - time if audio_clip else 0
        
        # If the current asset is None, use the last non-None asset
        if asset is None:
            asset = last_non_none_asset
        else:
            last_non_none_asset = asset
        
        # Load the video clip or image for the current asset
        if len(files) > 0:
            complete_path = f"{base_path}/{asset}"
            print(complete_path)
            if asset is not None:
                if asset.endswith(".mp4") or asset.endswith(".mkv"):
                    insert_clip = VideoFileClip(complete_path).subclip(t_start=0, t_end=duration)
                elif asset.endswith(".jpg") or asset.endswith(".png") or asset.endswith(".png"):
                    insert_clip = create_image_clip(complete_path, duration)
                else:
                    continue
            else:
                if last_non_none_asset.endswith(".mp4") or last_non_none_asset.endswith(".mkv"):
                    insert_clip = VideoFileClip(complete_path).subclip(t_start=0, t_end=duration)
                elif last_non_none_asset.endswith(".jpg") or last_non_none_asset.endswith(".png") or last_non_none_asset.endswith(".png"):
                    insert_clip = create_image_clip(complete_path, duration)
                else:
                    continue
                
            insert_clip = insert_clip.resize(width=1920, height=1080)
            video_clips_to_concatenate.append(insert_clip)
        
        last_timestamp = time
        
        # Update the last_non_none_asset if the current asset is not None
        if asset is not None:
            last_non_none_asset = asset
    
    # If no asset (video or image) is added, add a blank screen
    if len(files) == 0:
        blank_duration = sum(item['time'] for item in assets_time_list)  # Total duration
        blank_clip = VideoClip(lambda t: make_frame(t), duration=blank_duration)
        video_clips_to_concatenate.append(blank_clip)
    
    # Concatenate all video clips
    final_clip = concatenate_videoclips(video_clips_to_concatenate, method="compose")

    # Mute the final clip
    final_clip = final_clip.volumex(0)
    
    # Set the audio if loaded
    if audio_clip is not None:
        final_clip = final_clip.set_audio(audio_clip)
    
    # Write the final concatenated video to a file
    print(f"Writing final output to: {output_path}")
    final_clip.write_videofile(output_path, codec="libx264", fps=24)
    
    print("Concatenation process completed successfully!")

# Call the function with desired parameters
# concatenate_videos_with_audio()
