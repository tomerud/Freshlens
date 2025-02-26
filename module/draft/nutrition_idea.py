import mysql.connector
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
from mysqlDB.user.user_queries import get_user_nutrition_consumption
from dotenv import load_dotenv

load_dotenv()
import os

def get_nutrition_data(user_id: str) -> dict:
    nutritional_values= get_user_nutrition_consumption(user_id)
    return nutritional_values



def LLM_nutrition_prompt(nutrition_data, api_key):
    # Prompt for detailed insights
    prompt_template = PromptTemplate(
        input_variables=[
            "total_energy_kcal", "total_protein_g", "total_fat_g", 
            "total_saturated_fat_g", "total_carbs_g", "total_sugars_g", 
            "total_fiber_g", "total_sodium_mg"
        ],
        template="""
            You are a nutrition and health expert. Based on the following aggregated nutritional data for the past week, analyze the user's dietary habits and provide personalized, actionable insights to improve their nutrition and overall health.

            User's Weekly Nutritional Intake:
            - Energy: {total_energy_kcal} kcal
            - Protein: {total_protein_g} grams
            - Fat: {total_fat_g} grams
            - Saturated Fat: {total_saturated_fat_g} grams
            - Carbs: {total_carbs_g} grams
            - Sugars: {total_sugars_g} grams
            - Fiber: {total_fiber_g} grams
            - Sodium: {total_sodium_mg} mg

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
    )

    nutrition_expert = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.0,
        max_output_tokens=2000
    )

    # Create a runnable sequence for detailed insights
    nutrition_chain = RunnableSequence(prompt_template | nutrition_expert)

    # Get detailed insights
    detailed_insights = nutrition_chain.invoke(nutrition_data)

    # Step 2: Summarize Insights for User
    summary_prompt = PromptTemplate(
        input_variables=["detailed_insights"],
        template="""
            You are a nutrition assistant. Summarize the given nutrition report into a **short, clear action plan** for a user.

            **Example Summary Format:**  
            - **Key Issues:** [List major concerns]  
            - **Actionable Steps:** [Simple, practical fixes]  

            Keep it **engaging, user-friendly, and motivational**. Avoid unnecessary complexity.
            if needed, you can use bullet points or numbered lists for clarity.

            **Nutrition Report:**  
            {detailed_insights}
            """
    )

    summary_expert = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=api_key,
        temperature=0.0,
        max_output_tokens=1000
    )

    # Create a runnable sequence for summary
    summary_chain = RunnableSequence(summary_prompt | summary_expert)

    # Generate summary from detailed insights
    user_summary = summary_chain.invoke({"detailed_insights": detailed_insights})

    return {"detailed_insights": detailed_insights, "summary": user_summary}



def print_nutrition_report(report):
    # Print Detailed Insights
    print("=== Detailed Insights ===")
    print(report['detailed_insights'].content)
    print("\n")

    # Print Summary
    print("=== Summary Action Plan ===")
    print(report['summary'].content)

def generate_nutrition_insights(user_id):
    api_key=os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    nutrition_data = get_nutrition_data(user_id)
    insights = LLM_nutrition_prompt(nutrition_data,api_key)
    return insights

if __name__ == "__main__":
    print("----------------")
    nutrition_report=generate_nutrition_insights("0NNRFLhbXJRFk3ER2_iTr8VulFm4")
    print_nutrition_report(nutrition_report)
    print("----------------")