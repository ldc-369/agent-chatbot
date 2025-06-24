import os
import requests

import streamlit as st
from utils.constants import PROVIDERS, API_URL

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

def apply_custom_css(path="frontend/css/styles.css"):
    with open(path, "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
apply_custom_css()

if __name__ == "__main__":
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.set_page_config(page_title="AI Medical Chatbot", page_icon="🧠", layout="centered")
    st.title("🧠 AI Medical Chatbot")
    st.caption("Ask any medical question based on your uploaded knowledge documents.")

    # SIDEBAR SETTINGS
    with st.sidebar:
        st.header("🧠 Chatbot Settings")
        provider = st.radio("🔌 Choose LLM Provider:", list(PROVIDERS.keys()), index=0)
        model = st.selectbox("🧠 Select Model:", PROVIDERS[provider])
        use_web = st.checkbox("🌐 Allow web search", value=False)
        
        st.subheader("⚙️ Custom Prompt Template")
        custom_prompt = st.text_area(
            "Define your own prompt template:",
            height=150,
            placeholder="e.g. You are a helpful medical assistant. Only use the context provided..."
        )

        st.markdown(f"""
        **Provider:** `{provider}`  
        **Model:** `{model}`  
        **Web Search Enabled:** `{use_web}`  
        """)
        st.markdown("---")
        st.markdown("✉️ [cuongld.ai@gmail.com](mailto:cuongld.ai@gmail.com)")

    # CHAT INPUT
    with st.form("chat_input", clear_on_submit=True):
        query = st.text_input("💬 Ask your medical question:", placeholder="E.g. What are the symptoms of hypertension?")
        submitted = st.form_submit_button("Send message")

        if submitted:
            if not query.strip():
                st.warning("❗ Please enter a valid question.")
            else:
                with st.spinner("🤖 Thinking..."):
                    payload = {
                        "model_name": model,
                        "provider": provider,
                        "allow_search": use_web,
                        "query": query,
                    }
                    
                    try:
                        res = requests.post(f"{API_URL}/api/chat", json=payload).json()
                    
                        if res["status"]:
                            answer = res["data"].strip()
                        
                        if answer:
                            st.session_state.chat_history.append({"user": query, "bot": answer})
                            for pair in st.session_state.chat_history[::-1]:
                                for role, msg in pair.items():
                                    css_class = "user-msg" if role == "user" else "bot-msg"
                                    st.markdown(f"<div class='{css_class}'>{msg}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")