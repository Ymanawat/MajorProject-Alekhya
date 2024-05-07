import os
import time
from typing import Optional
from combiner import concatenate_videos_with_audio
from download_images import get_photos_by_query
from google_image import image_search
from gptServiceToGetKeywords import getTheKeywordsFromScriptGPT, getTheKeywordsFromScriptGemini
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from getVideosFromAssets import get_video_filenames

from geminiScript import generate_text
# from gptService import generate_text

# uncomment one you want to use and comment another
from gtts import speak_with_pauses
# from openAITTS import speak_with_pauses

def improve_script(script):
    # if there are no files then we will get some images from web
    if not get_video_filenames():
        keywords = getTheKeywordsFromScriptGPT(script)
        # keywords = getTheKeywordsFromScriptGemini(script)
        for keyword in keywords:
            image_search(keyword)
    
        # Wait for all image searches to complete
        while not get_video_filenames():
            time.sleep(1)  # Adjust sleep duration as needed

    # getting the fileNames that are finally we have
    videoFiles = get_video_filenames()

    # improve the script
    imp_script = generate_text(script, videoFiles)
    return imp_script


# the data model for request body
class ScriptData(BaseModel):
    script: str

app = FastAPI()

@app.post("/convert-to-video")
def create_item(script_data: ScriptData):
    # extracting the script from req body
    script = script_data.script
    
    # call to transform the rough script to an full video format
    improved_script = improve_script(script)
    print(improved_script)

    # sending the finally improved script to the TTS
    # [output_audio, asset_list]
    res = speak_with_pauses(improved_script)
    output_audio = res[0]
    asset_list = res[1]

    # final call to merge all and produce the video
    videoFiles = get_video_filenames()
    concatenate_videos_with_audio(assets_time_list=asset_list, audio_path=output_audio, files=videoFiles)
    return

if __name__ == "__main__":
    uvicorn.run(app)