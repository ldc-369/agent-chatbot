import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
OPENAI_MODEL = "gpt-4.1-mini-2025-04-14"

# providers: azure_ai, bedrock, google_vertexai, google_anthropic_vertex, cohere, ollama, ibm, azure_openai, google_genai, deepseek, huggingface, anthropic, fireworks, bedrock_converse, mistralai, together, xai, openai, groq, perplexity
PROVIDERS = {
    "OpenAI": {"models": ["gpt-4o-mini"], "api_key": OPENAI_API_KEY},
    "Groq": {"models": ["deepseek-r1-distill-llama-70b"], "api_key": GROQ_API_KEY},
}

CUSTOM_QUERY = "You are a smart, friendly, accurate virtual assistant."