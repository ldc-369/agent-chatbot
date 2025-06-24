from pprint import pprint

from utils import constants
from schemas.chat_schemas import ChatRequest, ChatResponse
from utils.constants import CUSTOM_QUERY, PROVIDERS

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from fastapi import APIRouter

router = APIRouter()

def prompt (
    state: AgentState,
    config: RunnableConfig,
) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    system_msg = f"User's name is {user_name}" + CUSTOM_QUERY
    return [{"role": "system", "content": system_msg}] + state["messages"]

def initialize_agent(model_name = "gpt-4o-mini", provider = "OpenAI", allow_search = False):
    model_initialized = PROVIDERS[provider]["func_api"](
        model=model_name
    )
    agent = create_react_agent(
        model=model_initialized,
        tools=[TavilySearchResults(max_results=2)] if allow_search else [],
        prompt=prompt
    )
    return agent

default_agent = initialize_agent()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    query = request.query
    provider = request.provider
    model_name = request.model_name
    allow_search = request.allow_search
    
    agent = default_agent
    
    if model_name in PROVIDERS[provider]["models"] and model_name != "gpt-4o-mini":
        agent = initialize_agent(model_name, provider, allow_search)
    
    res = agent.invoke(
        input={"messages": [{"role": "user", "content": query}]}, 
        config={"configurable": {"user_name": "Cuong Bad boy"}}
    )
    
    last_message = res["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        # print("Last message:", last_message.content)
        return {"data": last_message.content, "status": True}
    else:
        print("No message found!!!")