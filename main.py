import os
from typing import Optional

from combiner import concatenate_videos_with_audio # type: ignore
from test import speak_with_pauses # type: ignore
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from getVideosFromAssets import get_video_filenames
from gptService import generate_text
from xtts import speak, speak_and_save

# """welcome, game developers. Today we are going to discuss the fundamental concept of game dev, collision detection."""

text = """Welcome back, folks! Today, we're going to discuss a fundamental aspect of game development: collision detection. Now, you might be wondering, what exactly is collision detection? Well, it's the process of determining when two objects in a game world intersect or come into contact with each other. This might sound straightforward, but trust me, there's a bit more to it than meets the eye.Let's delve deeper into this topic and explore how we can implement collision detection in our game"""

# test_text = """{"asset": "welcome.mp4", "pause": 100 }Welcome back, folks! Today, we're going to discuss a fundamental aspect of game development: collision detection. {"asset": "collision_detection.mp4", "PAUSE": 100} Now, you might be wondering, what exactly is collision detection? {"PAUSE": 200} Well, it's the process of determining when two objects in a game world intersect or come into contact with each other. {"PAUSE": 200} This might sound straightforward, but trust me, there's a bit more to it than meets the eye. {"PAUSE": 300} Let's delve deeper into this topic and explore how we can implement collision detection in our game. {"PAUSE": 300}"""

def improve_script(script):
    videoFiles = get_video_filenames()
    imp_script = generate_text(script, videoFiles)
    return imp_script

class ScriptData(BaseModel):
    script: str

app = FastAPI()

@app.post("/convert-to-video")
async def create_item(script_data: ScriptData):
    # print(script_data)

    script = script_data.script
    improved_script = await improve_script(script)
    print(script_data)
    res = speak_with_pauses(improved_script)
    output_audio = res[0]
    asset_list = res[1]
    # [output_audio, asset_list]
    concatenate_videos_with_audio(output_audio, asset_list)
    return

if __name__ == "__main__":
    uvicorn.run(app)