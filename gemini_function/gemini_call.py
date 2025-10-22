from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

gemini__prompt = "Please research important climate datapoints that have surfaced within the last week." \
"Once completed, please summarize these findings in a consise manner and structure as a _____ file." \
"An example of this would be: "


def gemini_data():
    # Use the client that already has the API key loaded from .env
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=gemini__prompt
    )
    return response.text