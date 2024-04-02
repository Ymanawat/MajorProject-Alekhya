from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from getVideosFromAssets import get_video_filenames
from geminiScript import generate_text
from xtts import speak, speak_and_save


def improve_script(script):
    videoFiles = get_video_filenames()
    imp_script = generate_text(script)
    return imp_script


class ScriptData(BaseModel):
    script: str

app = FastAPI()

@app.post("/convert-to-video")
def create_item(script_data: ScriptData):
    # print(script_data)
    script = script_data.script
    improved_script = improve_script(script)

    output_audio_file = "output.mp3"
    speak_and_save(improved_script, output_audio_file)
    # print(script)

    return


if __name__ == "__main__":
    uvicorn.run(app)