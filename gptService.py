from openai import OpenAI

import os
from dotenv import load_dotenv
import asyncio

from openai import ChatCompletion

load_dotenv()

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

base_prompt = """
You are a Youtube video script writer,  here is a rough script written by me i want a better script don't incldue any of the prefix telling who is speaking like ( Developer: "Hey everyone ) nor any of the narration or scene setup related sentences like 
[Camera fades in on a developer sitting in front of a computer screen, with game development software visible in the background.]

This script will be only and only used as a voiceover only so keep it streightforward and simple paragraphs and sentence with proper indentation and spacing.
The script must sound humanic so use simple and verbel words only. use some of the filler words according the sentences, use appropriately.
filler_words = ["Um", "Uh", "Huh", "Well", "So", "You know", "Like", "Ah", "Okay", "Right"]

use curly braces to tell about which asset should be used now or how much pause is required between these sentence as these will be used for the voicevers
"pause" to tell the the tts that here requuire pause while speaking naturally like humans, have a pause after each sections
for 100ms of pause of 500ms requierd then { "asset" : "...", "pause": 500, "sentence": "..."} and so on.

these are the video file names that are being used in the script, you have to put the assets in the script wherever required, these video file names
shows what is in the file so whenever the text is related to some files then use them before that sentence. like if a filename is "sunset.mp4", and in the sentence we are talking about the sunset so you have to use that asset like this: {"asset":"sunset.mp4", "pause": 100}.
use 100 pause always when you are using some video filename
video_file_names : [FILENAMES]

> * Important: never use some random filename as asset, only use which are given to you in video_file_names
> * Important: never use some random filename as asset, only use which are given to you in video_file_names

---start of example

example:
    input:
    Hey everyone, in this tutorial, I'm going to show you how to implement a basic enemy AI in our game. Right now, our enemies just wander around randomly, which isn't very challenging for the player. So, let's dive into the code and make our enemies smarter by adding a simple pathfinding algorithm.

    output:
    [{"asset": "welcome.mp4", "pause": 100, "sentence": "Welcome back, folks! Today, we're going to discuss a fundamental aspect of game development: collision detection."}, {"asset": "collision_detection", "pause": 100, "sentence": "Now, you might be wondering, what exactly is collision detection?}, {"pause": 200, "sentence": "Well, it's the process of determining when two objects in a game world intersect or come into contact with each other."}, {"pause": 200, "sentence": "This might sound straightforward, but trust me, there's a bit more to it than meets the eye."} {"pause": 300, "sentence": "Let's delve deeper into this topic and explore how we can implement collision detection in our game."}]

---end of example

I only want a valid json in response like [ { "asset" : "...", "pause" : "...", "sentence" : "..."} ]

Rough Script:
"""

async def generate_text(input_text, fileNames):
    try:
        file_names_string = ', '.join(fileNames)
        print('input_text in generate_text', input_text)
        content = base_prompt.replace("FILENAMES", file_names_string)
        content += input_text

        print(content)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
            # max_tokens=150,
            temperature=0.7,
            stop=None
        )

        processed_text = response.choices[0].message.content
        print(processed_text)
        return processed_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# input_text = "Hey everyone, welcome back to our game dev log. Today, I'm excited to share with you the progress we've made on our latest project. It's been an incredible journey so far, filled with late nights, endless lines of code, and more cups of coffee than I can count. But seeing our vision come to life makes it all worth it. From brainstorming ideas to sketching out character designs, every step of the way has been a labor of love. And let me tell you, the challenges we've faced along the way have only made us stronger as a team. Whether it's debugging tricky code or fine-tuning game mechanics, we've tackled each obstacle head-on, fueled by our passion for creating something truly special. So stick around as we dive deeper into the development process, sharing insights, tips, and maybe even a sneak peek or two. Thanks for joining us on this adventure, and remember, the journey is just as important as the destination. Happy gaming, everyone!"

# generated_text = asyncio.run(generate_text(input_text, ['welcome.mp4', 'debugging.mp4']))
# print(generated_text)
