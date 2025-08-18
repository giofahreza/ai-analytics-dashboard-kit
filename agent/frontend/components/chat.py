import streamlit as st
import asyncio
from typing import Dict, List, Any

def render_chat_interface(api_client) -> None:
    """Render the AI chat interface"""
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_query = st.text_input(
                "Ask a question about mining data:",
                placeholder="e.g., Show me illegal mining sites in Jakarta",
                key="chat_input"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 🚀", type="primary")
    
    # Process query when submitted
    if submit_button and user_query.strip():
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query
        })
        
        # Show processing indicator
        with st.spinner("AI is analyzing your query..."):
            try:
                # Query the AI agent
                response = asyncio.run(api_client.query_ai_agent(user_query))
                
                if response and response.get("response"):
                    ai_response = response["response"]
                    
                    # Add metadata info
                    metadata_info = ""
                    if response.get("query_type"):
                        metadata_info += f"**Query Type:** {response['query_type'].title()}\n"
                    if response.get("intent"):
                        metadata_info += f"**Intent:** {response['intent']}\n"
                    if response.get("sql_query"):
                        metadata_info += f"**SQL Query:** `{response['sql_query']}`\n"
                    
                    full_response = f"{ai_response}\n\n---\n*Query Details:*\n{metadata_info}"
                    
                    # Add AI response to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": full_response,
                        "data": response.get("data", []),
                        "metadata": response.get("metadata", {})
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": "I apologize, but I couldn't process your query. Please try rephrasing or check the system status."
                    })
                    
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"An error occurred: {str(e)}"
                })
    
    # Display chat history
    st.markdown("### 💬 Conversation History")
    
    if st.session_state.chat_history:
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                if message["role"] == "user":
                    st.markdown(f"**🧑‍💻 You:** {message['content']}")
                else:
                    st.markdown(f"**🤖 AI Assistant:** {message['content']}")
                    
                    # Show data table if available
                    if message.get("data") and len(message["data"]) > 0:
                        with st.expander("📊 View Data Results"):
                            st.json(message["data"])
                
                st.markdown("---")
    else:
        st.info("👋 Hi! I'm your AI assistant for mining data analysis. Ask me anything about illegal mining sites, production data, or IUP information!")
    
    # Sample questions
    st.markdown("### 🔍 Sample Questions")
    col1, col2 = st.columns(2)
    
    sample_questions = [
        "Show me all illegal mining sites in Jakarta",
        "What is the total production in Bandung?",
        "How many active IUPs are there?",
        "Show production trends this month",
        "Find mining sites near coordinates -6.2, 106.8",
        "What are the regulations for illegal mining?"
    ]
    
    for i, question in enumerate(sample_questions):
        column = col1 if i % 2 == 0 else col2
        with column:
            if st.button(question, key=f"sample_{i}"):
                # Set the question in the input (for next interaction)
                st.session_state.sample_question = question
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def render_query_suggestions() -> List[str]:
    """Get query suggestions based on available data"""
    
    return [
        "Statistical queries about mining data",
        "Geographic location-based searches",
        "Production trend analysis", 
        "Regulatory compliance questions",
        "Risk assessment queries",
        "Comparative analysis between regions"
    ]
