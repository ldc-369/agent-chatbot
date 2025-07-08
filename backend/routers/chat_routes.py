from langchain_core.messages.ai import AIMessage
from langchain.chains import ConversationalRetrievalChain
from fastapi import APIRouter

from schemas.chat_schemas import GeneralChatRequest, GeneralChatResponse, PDFChatRequest, PDFChatResponse
from services.general_chat_service import *
from services.pdf_chat_service import *
from utils.index import init_groq_model, clean_output_text

router = APIRouter()

@router.post("/chat", response_model=GeneralChatResponse)
def chat(request: GeneralChatRequest):
    query = request.query
    provider = request.provider.lower()
    model_name = request.model_name
    allow_search = request.allow_search
    
    agent = initialize_agent(model_name, provider, allow_search)
    
    res = agent.stream(
        input={"messages": [{"role": "user", "content": query}]}, 
        config={"configurable": {"user_name": "Cuong Bad boy", "thread_id": thread_id}},
        stream_mode="values"
    )
    
    # res = agent.invoke(...)
    # last_message = res["messages"][-1]
    
    # lặp qua mỗi node
    for step in res:
        last_message = step["messages"][-1]
        # print(last_message.text())
        # print(last_message)
        
        if hasattr(last_message, "content"):
            cleaned_text = clean_output_text(last_message.content)
        
    if isinstance(last_message, AIMessage):
        return {"data": cleaned_text, "status": True}
    else:
        print("No message found!!!")
        return {"data": "", "status": False}

@router.post("/chat-pdf", response_model=PDFChatResponse)
def chat_pdf(request: PDFChatRequest):
    model_name = request.model_name
    query = request.query
    
    model_initialized = init_groq_model(model_name, chat_mode="pdf-chat")
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=model_initialized,
        retriever=faiss_vectors.as_retriever(search_kwargs={'k':5}), # truy xuất 3 chunks gần nhất
        memory=buffer_memory,
        output_key="answer",
        combine_docs_chain_kwargs={"prompt": pdf_chat_prompt},
        return_source_documents=True,
    )
    
    answer, sources = get_response(query, qa_chain)
    cleaned_text = clean_output_text(answer)
    return {"data": {"answer": cleaned_text, "sources": sources}, "status": True}