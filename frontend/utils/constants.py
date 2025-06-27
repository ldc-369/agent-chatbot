import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

PROVIDERS = {
    "OpenAI": ["gpt-4o-mini"],
    "Groq": ["deepseek-r1-distill-llama-70b", "meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct", "meta-llama/llama-prompt-guard-2-22m", "meta-llama/llama-prompt-guard-2-86m", "mistral-saba-24b", "qwen-qwq-32b", "qwen/qwen3-32b"],
    "HF-Inference": ["meta-llama/Llama-3.1-8B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3", "meta-llama/Llama-3.3-70B-Instruct", "Qwen/Qwen3-32B", "HuggingFaceH4/zephyr-7b-beta", "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF", "Qwen/QwQ-32B"]
}