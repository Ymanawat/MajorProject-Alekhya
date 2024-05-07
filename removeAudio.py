from moviepy.editor import VideoFileClip

# Load the video clip
clip = VideoFileClip("welcome.mp4")

# Mute the audio
clip = clip.without_audio()

# Write the muted video to a new file
clip.write_videofile("muted_video.mp4", codec="libx264", audio_codec="aac")
