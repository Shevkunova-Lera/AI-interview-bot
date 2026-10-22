import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def test_connection():
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents='Return the word "Success" if you recieve this message.'
        )
        print("API Connection:", response.text)
    except Exception as e:
        print(f"Error connection to API: {e}")

if __name__ == "__main__":
    test_connection()
