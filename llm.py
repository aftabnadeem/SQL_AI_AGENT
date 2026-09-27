from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_query(model, prompt):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text
