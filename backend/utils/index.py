import re

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings

from utils.constants.keys import OPENAI_API_KEY, GROQ_API_KEY, HF_TOKEN
from utils.constants.embedding_models import HF_EMBEDDING_MODEL
from services.pdf_chat_service import get_response

def init_openai_model(model_name, **kwargs):
    return ChatOpenAI(model=model_name, temperature=0.5, verbose=True, api_key=OPENAI_API_KEY, **kwargs)

pre_groq_model_name = ""
pre_groq_model = None
def init_groq_model(model_name, chat_mode = "general-chat", **kwargs):
    if chat_mode == "general-chat":
        return ChatGroq(model=model_name, temperature=0.5, verbose=True, api_key=GROQ_API_KEY, **kwargs)
    elif chat_mode == "pdf-chat":
        global pre_groq_model_name, pre_groq_model
        
        if model_name == pre_groq_model_name:
            return pre_groq_model
        
        model_initialized = ChatGroq(model=model_name, temperature=0.0, verbose=True, api_key=GROQ_API_KEY, **kwargs)
        
        pre_groq_model_name = model_name
        pre_groq_model = model_initialized
        return model_initialized

embedding_model = HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)
pre_hf_model_name = ""
pre_hf_model = None

def init_hf_model(model_name, chat_mode = "general-chat", **kwargs):
    if chat_mode == "general-chat":
        model_initialized = HuggingFaceEndpoint(
            repo_id=model_name,
            provider = "hf-inference",
            task = "text-generation",
            temperature=0.5,
            verbose=True,
            max_new_tokens=512,
            huggingfacehub_api_token=HF_TOKEN,
            **kwargs
        )
        return ChatHuggingFace(
            llm=model_initialized,
        )
    elif chat_mode == "pdf-chat":
        global pre_hf_model_name, pre_hf_model
        if model_name == pre_hf_model_name:
            return pre_hf_model
        
        model_initialized = HuggingFaceEndpoint(
            repo_id=model_name,
            task = "text-generation",
            temperature=0.5,
            verbose=True,
            max_new_tokens=512,
            huggingfacehub_api_token=HF_TOKEN,
            **kwargs
        )
        pre_hf_model_name = model_name
        pre_hf_model = model_initialized
        return model_initialized
    
def clean_output_text(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    
def test_init_hf_model():
    chat=init_hf_model("mistralai/Mistral-7B-Instruct-v0.3")
    messages = [
        ("system", "You are a helpful assistant."),
        ("human", "I love programming."),
    ]
    res = chat.invoke(messages)
    print(type(res))
    for chunk in chat.stream(messages):
        print(chunk)
        
def test_pdf_chat():
    while True:
        query = input("\n❓ Enter your question (type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            print("👋 Goodbye!")
            break

        answer, sources = get_response(query)
        
        print("\n📌 Answer:", answer)
        print("\n📚 Source Documents:")
        
        for i, doc in enumerate(sources, start=1):
            print(f"\n--- Document {i} ---")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(doc.page_content)
        print("\n")