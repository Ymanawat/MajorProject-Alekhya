import os

def get_video_filenames(folder_path="assets/videos"):
  """
  This function takes a (relative) folder path and returns a list of video filenames within that folder.

  Args:
      folder_path (str, optional): The relative path to the folder containing the videos. Defaults to "assets/videos".

  Returns:
      list: A list containing the filenames of all videos in the folder.
  """
  script_dir = os.path.dirname(__file__)  # Get the directory of the script
  absolute_path = os.path.join(script_dir, folder_path)  # Combine script dir and folder path
  video_filenames = []
  for filename in os.listdir(absolute_path):
    # Check if the filename ends with a common video extension (modify as needed)
    if filename.lower().endswith((".mp4", ".avi", ".mkv", ".wmv")):
      video_filenames.append(filename)
  return video_filenames

# Example usage
# video_filenames = get_video_filenames()

# print(f"Video filenames in 'folder_path':", video_filenames)
