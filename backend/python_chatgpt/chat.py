from dotenv import load_dotenv
import os
from openai import OpenAI
from datetime import datetime

load_dotenv()

def generate_recipe(inventory):
    """
    Generates a recipe based on available ingredients, prioritizing those with the closest expiration dates.
    """
    api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment

    try:
        client = OpenAI(api_key=api_key)
        model_engine = "gpt-3.5-turbo"

        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""
        I have the following ingredients in my fridge, each with an expiration date: {{{inventory}}}.
        Please generate **two recipes** that prioritize ingredients with the closest expiration date to {current_date}.
        
        - Use all or most of the ingredients while minimizing waste.
        - Keep instructions clear and easy to follow.
        - Separate both recipes using '###' so I can parse them later.
        - **Only return the recipes. Do not repeat the input data.**
        
        Format:
        ```
        1. [Recipe Name]
        Ingredients:
        - [Ingredient 1]
        - [Ingredient 2]
        ...
        
        Instructions:
        1. [Step 1]
        2. [Step 2]
        ...
        ```

        2. [Recipe Name]
        ...
        ```

        Ensure the response is **fully generated**.
        """

        chat_completion = client.chat.completions.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,  
            max_tokens=600  # Increased from 200 to 600
        )

        response = chat_completion.choices[0].message.content.strip()
        return response

    except Exception as e:
        print(f"Error generating recipe: {e}")
        return None