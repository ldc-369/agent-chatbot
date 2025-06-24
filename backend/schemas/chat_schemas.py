from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    model_name: str
    provider: str
    allow_search: bool
    
class ChatResponse(BaseModel):
    data: str
    status: bool