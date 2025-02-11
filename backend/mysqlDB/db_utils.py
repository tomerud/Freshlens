import mysql.connector
from dotenv import load_dotenv
import os

from deep_translator import GoogleTranslator
import unicodedata
import re

load_dotenv()

def get_db_connection():
    """
    Establish and return a connection to the database using environment variables.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

def execute_query(query, params=None, fetch_all=True, fetch_one=False, commit=True):
    """
    A generic function to execute SQL queries safely.
    
    Args:
        query (str): The SQL query to execute.
        params (tuple): The parameters to pass into the query.
        fetch_one (bool): If True, fetch and return one result.
        fetch_all (bool): If True, fetch and return all results.
        commit (bool): If True, commit the transaction.
    
    Returns:
        tuple | list | None: The result of the query (if applicable).
    """
    conn = None
    cursor = None
    result = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if params is None:
            params = ()

        cursor.execute(query, params)

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        
        if commit:
            conn.commit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return result


def translate_to_hebrew(word):
    """Translate English word to Hebrew using Google Translator and clean it."""
    translated = GoogleTranslator(source='auto', target='iw').translate(word)
    
    # Normalize and remove diacritics (Nikud)
    cleaned_word = ''.join(c for c in unicodedata.normalize('NFKD', translated) if not unicodedata.combining(c))
    
    cleaned_word = re.sub(r'[^\u0590-\u05FF\s]', '', cleaned_word)  # Keeps only Hebrew letters and spaces

    return cleaned_word.strip()