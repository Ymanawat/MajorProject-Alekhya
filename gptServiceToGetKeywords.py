import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

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

#for initializing the gemini model
model = initialize_model()

base_prompt = """
Your task is to analyze the script and extract relevant keywords. Provide an array containing these keywords, ensuring they capture the essence of the script while minimizing redundancy. Each keyword should represent a distinct concept or object discussed in the script.

the output should be like an of those keywords like : ["keyword1", "keyword2", "keyword3",...]

for example if there are three sentence talking about lion only then only one lion should in in the keyword array for those three sentences no need to mention that keyword multiple time.

i want object as prefix like if we are talking about lion i want lion in all the keywords related to that, if we are talking about car i want car in all the keywords, if talking about game want game in all the keywords

Limit the number of keywords per topic to a maximum of five, unless there are fewer than five sentences discussing a particular topic. In such cases, include only 2-3 keywords that are essential for understanding the topic.

avoid overly generic keywords like 'proud' or 'majesty'. 'nice', 'good', 'round' and so on. Just use object or the action in the script.

Script to analyze:

"""

# this function is used when we want to use Gemini LLLM
def getTheKeywordsFromScriptGemini(input_text):
    try:
        response = model.generate_content(contents=base_prompt+input_text)

        print(response)

        processed_text = response.text.strip()

        # Remove the square brackets and split the string at commas
        array = json.loads(processed_text)

        return array

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# this function is used when we want to use GPT
def getTheKeywordsFromScriptGPT(input_text):
    content=base_prompt+input_text
    response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": content}],
            # max_tokens=150,
            temperature=0.4,
            stop=None
        )

    processed_text = response.choices[0].message.content
    
    # Remove the square brackets and split the string at commas
    array = processed_text[1:-1].split(', ')

    # Remove double quotes from each element
    array = [element.strip('"') for element in array]
    print(array)

    return array

# example test
# input_text = "In the jungle's heart, the Lion reigns supreme, his roar echoing his royal decree. With a mane of gold, he rules with majesty untold."
# getTheKeywordsFromScriptGemini(input_text)