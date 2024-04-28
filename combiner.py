import cv2
import numpy as np
from moviepy.editor import VideoClip, concatenate_videoclips, AudioFileClip, VideoFileClip

def resize_clip(clip, width=1920, height=1080):
    # Convert MoviePy clip to OpenCV-compatible format
    frames = [clip.get_frame(t) for t in np.arange(0, clip.duration, 1 / clip.fps)]
    resized_frames = [cv2.resize(frame, (width, height)) for frame in frames]
    
    # Create a new MoviePy clip with the resized frames
    resized_clip = VideoClip(lambda t: resized_frames[int(t * clip.fps)], duration=clip.duration)

    return resized_clip

def concatenate_videos_with_audio(audio_path='final_audio_with_pauses.mp3', assets_time_list=[{"time": 1.689, "asset": "welcome.mp4"}, {"time": 5, "asset": "collision_detection.mp4"}], output_path="output_video.mp4"):
    print("Starting concatenation process...")
    
    # Create a blank background video clip
    def make_frame(t):
        # Create a black frame
        width, height = 1920, 1080  # assuming HD resolution
        return np.zeros((height, width, 3), dtype=np.uint8)
    
    # Initialize variables
    video_clips_to_concatenate = []
    base_path = "assets/videos"
    last_timestamp = 0
    
    # Iterate over the array of objects
    for item in assets_time_list:
        # Get the time and asset from the current object
        time = item['time']
        asset = item['asset']
        
        print(f"Processing asset: {asset}")
        
        # Calculate the duration for which the current asset will be inserted
        duration = time - last_timestamp
        
        # Create a blank clip for the duration between videos
        blank_clip = VideoClip(make_frame, duration=duration)
        
        # Append the blank clip to the list of clips
        # video_clips_to_concatenate.append(blank_clip)
        
        complete_path = f"{base_path}/{asset}"
        
        # Load the video clip for the current asset
        if asset is not None:
            insert_clip = VideoFileClip(complete_path).subclip(time)
            # Resize the video clip to fit the main frame size using OpenCV
            insert_clip = resize_clip(insert_clip, width=insert_clip.size[0], height=insert_clip.size[1])
            video_clips_to_concatenate.append(insert_clip)
        
        last_timestamp = time
    
    # Concatenate all video clips
    final_clip = concatenate_videoclips(video_clips_to_concatenate, method="compose")
    
    # Mute the final clip
    final_clip = final_clip.volumex(0)
    
    # Load the audio file if provided
    if audio_path is not None:
        print(f"Loading audio file: {audio_path}")
        audio_clip = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(audio_clip)
    
    # Write the final concatenated video to a file
    print(f"Writing final output to: {output_path}")
    final_clip.write_videofile(output_path, codec="libx264", fps=24)
    
    print("Concatenation process completed successfully!")

# Call the function with desired parameters
# concatenate_videos_with_audio()
