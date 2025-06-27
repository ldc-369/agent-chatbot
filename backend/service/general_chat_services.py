import re
import uuid

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import MemorySaver
from langchain_tavily import TavilySearch

from utils.constants.index import CUSTOM_GENERAL_CHAT_PROMPT, PROVIDERS
from utils.constants.keys import TAVILY_API_KEY

search_tool = TavilySearch(max_results=2)
memory = MemorySaver()
thread_id = str(uuid.uuid4())

def prompt (
    state: AgentState,
    config: RunnableConfig,
) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    custom_query = f"User's name is {user_name}. {CUSTOM_GENERAL_CHAT_PROMPT}"
    return [{"role": "system", "content": custom_query}] + state["messages"]  

pre_model = ""
pre_agent = None

def initialize_agent(model_name, provider, allow_search: bool = False):
    global pre_model, pre_agent
    
    if model_name == pre_model:
        return pre_agent
    
    pre_model = model_name
    
    model_initialized = PROVIDERS[provider]["init_func"](model_name)
    tools = []
    
    if allow_search:
        tools.append(search_tool)
        
    agent = create_react_agent(
        model=model_initialized,
        tools=tools,
        prompt=prompt,
        checkpointer=memory
    )
    pre_agent = agent
    return agent

# def clean_output_text(text: str) -> str:
#     return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
