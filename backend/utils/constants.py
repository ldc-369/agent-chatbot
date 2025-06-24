import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = ""
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
OPENAI_MODEL = "gpt-4.1-mini-2025-04-14"

PROVIDERS = {
    "OpenAI": {"models": ["gpt-4o-mini"], "func_api": ChatOpenAI},
    "GroqCloud": {"models": ["deepseek-r1-distill-llama-70b"], "func_api": ChatGroq}
}

CUSTOM_QUERY = "You are a smart, friendly, accurate virtual assistant."