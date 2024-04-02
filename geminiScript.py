import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def initialize_model():
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        # print(api_key)
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
You are a Youtube video script writer,  here is a rough script written by me i want a better script don't incldue any of the prefix telling who is speaking like ( Developer: "Hey everyone ) nor any of the narration related sentences like 
[Camera fades in on a developer sitting in front of a computer screen, with game development software visible in the background.]

This script will be used as a voiceover only so don't add a lot of complexities just some sections and simple paragraphs and sentence with proper indentation and spacing.
The script must sound humanic so use simple and verbel words only.

use "PAUSE 100" to tell the the tts that here requuire pause while speaking naturally like humans, have a pause after each sections
for 100ms of pause of 500ms requierd then "PAUSE 500" and so on.

example:
    Rough Script:
    Hey everyone, in this tutorial, I'm going to show you how to implement a basic enemy AI in our game. Right now, our enemies just wander around randomly, which isn't very challenging for the player. So, let's dive into the code and make our enemies smarter by adding a simple pathfinding algorithm.

    Improved Script:
    Welcome, gamers! Today, I'm excited to walk you through enhancing our game's enemy AI. [PAUSE 1000] Currently, our adversaries lack strategy—they aimlessly roam the game world. But worry not! [PAUSE 200] We're about to change that. By incorporating a straightforward pathfinding algorithm, [PAUSE 500] we'll empower our enemies to pursue the player strategically. [PAUSE 200] Let's level up the challenge together!


Rough Script:
"""

def generate_text(input_text):
    try:
        if model is None:
            raise ValueError("Model is not initialized")

        contents=base_prompt+input_text
        # print(contents)
        response = model.generate_content(contents=contents)

        processed_text = response.text.strip()
        print(processed_text)

        return processed_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_text = "Hey everyone, welcome back to our game dev log. Today, I'm excited to share with you the progress we've made on our latest project. It's been an incredible journey so far, filled with late nights, endless lines of code, and more cups of coffee than I can count. But seeing our vision come to life makes it all worth it. From brainstorming ideas to sketching out character designs, every step of the way has been a labor of love. And let me tell you, the challenges we've faced along the way have only made us stronger as a team. Whether it's debugging tricky code or fine-tuning game mechanics, we've tackled each obstacle head-on, fueled by our passion for creating something truly special. So stick around as we dive deeper into the development process, sharing insights, tips, and maybe even a sneak peek or two. Thanks for joining us on this adventure, and remember, the journey is just as important as the destination. Happy gaming, everyone!"
generated_text = generate_text(input_text)
print(generated_text)
