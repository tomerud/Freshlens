from dotenv import load_dotenv
import os
from openai import OpenAI
from datetime import datetime

load_dotenv()

def generate_recipe(inventory):
    """
    Generates a recipe based on available ingredients, prioritizing those with the closest expiration dates.
    
    :param inventory: String of ingredients with their expiration dates.
    :param api_key: (Optional) OpenAI API key. Defaults to a predefined key.
    :return: Generated recipe as a string.
    """
    # Run before demo :
    # try:
    #     client.models.list()  # List available models (should work if the key is valid)
    #     print("API Key is working.")
    # except Exception as e:
    #     print(f"Error: {e}")

    # models = client.models.list()
    # for model in models:
    #     print(model.id)

    api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment

    try:
        client = OpenAI(api_key=api_key)
        model_engine = "gpt-3.5-turbo"

        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = " ".join([
            f"I have the following ingredients in my fridge, each with an expiration date: {{{inventory}}}.",
            f"Can you generate a recipe that prioritizes ingredients with the closest expiration date to {current_date}?",
            "The recipe should make the best use of what I have while minimizing waste.",
            "Please answer in a friendly manner.",
            "Write two recipes under the previous request and seperate them with the symbol '###' so I could pasre later.",
            "Only respond with the recipe itself, without repeating the input data."
        ])

        chat_completion = client.chat.completions.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  
            max_tokens=200  
        )

        response = chat_completion.choices[0].message.content
        return response

    except Exception as e:
        # API request failed
        print(f"Error generating recipe: {e}")
        return None
