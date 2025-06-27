from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.base import Runnable

from utils.constants.index import CUSTOM_PDF_CHAT_PROMPT, VECTORS_DIR
from utils.index import embedding_model

# load faiss vectors
faiss_vectors = FAISS.load_local(VECTORS_DIR, embedding_model, allow_dangerous_deserialization=True)  # nhớ chỉnh load lại (if uploadfile == True)

# prompt
pdf_chat_prompt = PromptTemplate(
    template = CUSTOM_PDF_CHAT_PROMPT, input_variables=["context", "chat_history", "question"]
)

buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",     
    input_key="question",          
    output_key="answer",           
    return_messages=True
)

def get_response(query: str, qa_chain: Runnable) -> tuple[str, list]:
    res = qa_chain.invoke({'question': query})
    answer = res["answer"]
    sources = res.get("source_documents", [])
    return answer, sources