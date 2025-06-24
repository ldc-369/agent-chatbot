from routers import chat_routes

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="LangGraph AI Agent")

app.include_router(chat_routes.router, prefix="/api")

@app.get("/")
def run_main():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)