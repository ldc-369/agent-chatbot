from pydantic import BaseModel
from langchain_core.documents import Document

class GeneralChatRequest(BaseModel):
    query: str
    model_name: str
    provider: str
    allow_search: bool
    
class PDFChatRequest(BaseModel):
    query: str
    model_name: str
    
class GeneralChatResponse(BaseModel):
    data: str | None
    status: bool
    
class PDFChatResponse(BaseModel):
    data: dict[str, str | list[Document]] | None
    status: bool