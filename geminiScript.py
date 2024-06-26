import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def initialize_model():
    try:
        api_key = os.getenv('GEMINI_API_KEY')

        if api_key is None:
            raise ValueError("API key not found. Make sure it's set in the .env file.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        return model

    except Exception as e:
        print(f"An error occurred during model initialization: {e}")
        return None

#initialize model
model = initialize_model()

base_prompt = """
You are a Youtube video script writer,  here is a rough script written by me i want a better script don't incldue any of the prefix telling who is speaking like ( Developer: "Hey everyone ) nor any of the narration or scene setup related sentences like 
[Camera fades in on a developer sitting in front of a computer screen, with game development software visible in the background.]

This script will be only and only used as a voiceover only so keep it streightforward and simple paragraphs and sentence with proper indentation and spacing.
The script must sound humanic so use simple and verbel words only. use some of the filler words according the sentences, use appropriately.
filler_words = ["Um", "Uh", "Huh", "Well", "So", "You know", "Like", "Ah", "Okay", "Right"]

use curly braces to tell about which asset should be used now or how much pause is required between these sentence as these will be used for the voicevers
"pause" to tell the the tts that here requuire pause while speaking naturally like humans, have a pause after each sections
for 100ms of pause of 500ms requierd then { "asset" : "...", "pause": 500, "sentence": "..."} and so on.

these are the Assets file names that are being used in the script, you have to put the assets in the script wherever required, these video file names
shows what is in the file so whenever the text is related to some files then use them before that sentence. like if a filename is "sunset.mp4", and in the sentence we are talking about the sunset so you have to use that asset like this: {"asset":"sunset.mp4", "pause": 100}.
If there are multiple images in the assets like for let say lion we have [lion_0.jpg, lion_1.jpg, lion_2.jpg], and we have a sentence in which we are talking about lion and no other assets matches that well then use these imgages alternatively in that sentence like : [{"asset":"lion_0.jpb", "pause": 100, "sentence": "The lion, with its majestic mane and powerful roar,"}, {"asset":"lion.jpg", "pause": 100, "sentence" :"reigns as the undisputed king of the savanna, embodying strength, courage, and regal grace."} ]

use 100 or more pause always when you are using some Assets filename, use pause according the condition of the sentence i want pause so that the sound of these sentence be more realistic and humanic

--Assets to use in the output

ASSETS : [FILENAMES]

--End of Assets to use in the output

> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS
> * Important: never use some random filename as asset, only use which are given to you in ASSETS


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

def generate_text(input_text, fileNames):
    try:
        if model is None:
            raise ValueError("Model is not initialized")

        file_names_string = ', '.join(fileNames)
        print(fileNames)
        print(file_names_string)

        base_prompt_modified = base_prompt.replace("FILENAMES", file_names_string)

        contents=base_prompt_modified+input_text
        print(contents)
        response = model.generate_content(contents=contents)

        processed_text = response.text.strip()
        print(processed_text)

        return processed_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_text = "Hey everyone, welcome back to our game dev log. Today, I'm excited to share with you the progress we've made on our latest project. It's been an incredible journey so far, filled with late nights, endless lines of code, and more cups of coffee than I can count. But seeing our vision come to life makes it all worth it. From brainstorming ideas to sketching out character designs, every step of the way has been a labor of love. And let me tell you, the challenges we've faced along the way have only made us stronger as a team. Whether it's debugging tricky code or fine-tuning game mechanics, we've tackled each obstacle head-on, fueled by our passion for creating something truly special. So stick around as we dive deeper into the development process, sharing insights, tips, and maybe even a sneak peek or two. Thanks for joining us on this adventure, and remember, the journey is just as important as the destination. Happy gaming, everyone!"
# generated_text = generate_text(input_text,  ['intro.mp4', 'brainstorming.mp4', 'debugging.mp4', 'outro.mp4'])
# print(generated_text)
