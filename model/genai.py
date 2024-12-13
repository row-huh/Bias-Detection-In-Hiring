import aiml
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompts import *

# fetch all .env variables

BASE_URL = "https://api.aimlapi.com/v1"
API_KEY = os.getenv('AIML_API_KEY')

# TODO
# set the user_prompt variable to come in from the streamlit app - ideally it should be the text from the pdf
user_prompt = "Tell me about San Francisco"


api = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def main():
    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=256,
    )

    response = completion.choices[0].message.content

    print("User:", user_prompt)
    print("AI:", response)


if __name__ == "__main__":
    main()