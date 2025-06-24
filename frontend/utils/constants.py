import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

PROVIDERS = {
    "OpenAI": ["gpt-4o-mini"],
    "GroqCloud": ["deepseek-r1-distill-llama-70b"]
}