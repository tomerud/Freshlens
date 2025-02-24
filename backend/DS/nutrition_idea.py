import mysql.connector
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
import os

def get_nutrition_data(user_id: str) -> dict:
    nutritional_values= get_last_month_nutrition_data(user_id)
    # Ensure that null values are replaced with 0
    # return {
    #     "total_protein": result["total_protein"] or 0,
    #     "total_fat": result["total_fat"] or 0,
    #     "total_sugars": result["total_sugars"] or 0
    # }
    return nutritional_values


def LLM_nutrition_prompt(nutrition_data,api_key):
    nutrition_prompt ="""
        You are a nutrition and health expert. Based on the following aggregated nutritional data for the past month, analyze the user's dietary habits and provide personalized, actionable insights to improve their nutrition and overall health.

        User's Monthly Nutritional Intake:
        - Protein: {total_protein} grams
        - Fat: {total_fat} grams
        - Sugars: {total_sugars} grams

        Instructions:
        - Identify any nutritional imbalances, such as excessive sugar intake or insufficient protein consumption.
        - Provide specific recommendations for improvement, including food alternatives and practical dietary changes.
        - Consider overall health implications and suggest adjustments that align with balanced nutrition.
        - Ensure that recommendations are realistic, sustainable, and aligned with general dietary guidelines.

        Example Guidance:
        - If sugar intake is high, suggest ways to reduce added sugars, such as choosing whole fruits over processed snacks.
        - If protein intake is low, recommend lean protein sources like chicken, fish, tofu, or legumes.
        - If fat intake is excessive, provide alternatives like healthy unsaturated fats from nuts, seeds, and avocados.

        Provide insights in a concise and practical manner, ensuring they are easy to understand and implement.
        """    
    prompt = PromptTemplate(
        input_variables=["total_protein", "total_fat", "total_sugars"],
        template=nutrition_prompt
    )
    nutrition_expert= ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # Gemini 2.0 Flash model
        api_key=api_key,
        temperature=0.0,
        max_output_tokens=2000 # Gemini uses max_output_tokens
    )
    
    # Create the LLMChain with the custom LLM and prompt template
    nutrition_chain = nutrition_prompt | nutrition_expert
    nutrtion_tips = nutrition_chain.invoke({"total_protein": nutrition_data.get("total_protein"), "total_fat": nutrition_data.get("total_fat"), "total_sugars": nutrition_data.get("total_sugars")})
    
    return nutrtion_tips


def generate_nutrition_insights(user_id):
    api_key=os.getenv("GEMINI_API_KEY")
    nutrition_data = get_nutrition_data(user_id)
    insights = LLM_nutrition_prompt(nutrition_data,api_key)
    return insights

