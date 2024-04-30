import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

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
You are a expert script analyzer, Your task is to extract keywords from the script and reponse with an array of those keywords like : ["keyword1", "keyword2", "keyword3",...]

How to extract keywords? 
To Extract keywords you have to analyse the sentences and if any sentence talk about something like some object person or doing something i want that as keyword from that sentence the keyword can also be a small string like "man_drinking_tea", "lion", "walking"
I want only the bare minimum keywords no need to add a lot of keywords only atmost 5 which suits the script and condition and actions in that script.

But if there is less sentences than 5 then give me only the keywords that are necessary only 2-3. I want less keywords always but i also want them to be a little descriptive not just keys like "proud", "mane", "majesty". instead i want like "the_proud_lion", "lion_Majesty_of_jungle"

i want object as prefix like if we are talking about lion i want lion in all the keywords related to that, if we are talking about car i want car in all the keywords, if talking about game want game in all the keywords

Script to analyze:

"""

def getTheKeywordsFromScriptGemini(input_text):
    try:
        response = model.generate_content(contents=base_prompt+input_text)

        processed_text = response.text.strip()

        # Remove the square brackets and split the string at commas
        array = processed_text[1:-1].split(', ')

        # Remove double quotes from each element
        array = [element.strip('"') for element in array]
        print(array)

        return array

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def getTheKeywordsFromScriptGPT(input_text):
    content=base_prompt+input_text
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
            # max_tokens=150,
            temperature=0.7,
            stop=None
        )

    processed_text = response.choices[0].message.content
    
    # Remove the square brackets and split the string at commas
    array = processed_text[1:-1].split(', ')

    # Remove double quotes from each element
    array = [element.strip('"') for element in array]
    print(array)

    return array

input_text = "In the jungle's heart, the Lion reigns supreme, his roar echoing his royal decree. With a mane of gold, he rules with majesty untold."

getTheKeywordsFromScriptGemini(input_text)