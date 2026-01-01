import streamlit as st
import google.generativeai as genai
import os

# Page configuration
st.set_page_config(
    page_title="Financial Advisor Chatbot",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e6f3ff;
        border-left: 4px solid #1f77b4;
    }
    .assistant-message {
        background-color: #f0f8ff;
        border-left: 4px solid #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load and configure the Gemini model"""
    try:
        # For Streamlit Community Cloud - use st.secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.0-flash")
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.info("Please make sure your GEMINI_API_KEY is set in Streamlit secrets")
        return None

def initialize_chat_session(_model):
    """Initialize chat with financial advisor persona"""
    system_prompt = """
    You are a helpful and knowledgeable financial advisor.
    You assist users with personal finance, budgeting, saving strategies, debt management, and financial planning.
    Always provide clear, practical advice tailored to the user's situation.
    Avoid giving investment or legal advice unless explicitly asked.
    Be supportive, professional, and focus on providing actionable guidance.
    Keep responses conversational but informative.
    """
    
    chat_session = _model.start_chat(
        history=[{"role": "user", "parts": [system_prompt]}]
    )
    return chat_session

def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Financial Advisor Chatbot</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome! I'm your AI financial assistant. I can help you with:
    - 💸 **Budgeting** and saving strategies
    - 🏠 **Debt management** and reduction
    - 📈 **Financial planning** for future goals
    - 💰 **Personal finance** guidance
    
    *Type your questions below and I'll provide practical advice!*
    """)
    
    # Load model
    model = load_model()
    if not model:
        st.stop()
    
    # Initialize session state
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = initialize_chat_session(model)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your financial advisor. How can I help you with your financial goals today? Whether it's budgeting, saving, or debt management, I'm here to help!"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about budgeting, saving, or financial planning..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check for exit command
        if prompt.lower() in ["exit", "quit", "bye"]:
            st.session_state.messages.append({"role": "assistant", "content": "👋 Goodbye! Feel free to come back anytime you have more financial questions. Remember, good financial habits start with small steps!"})
            with st.chat_message("assistant"):
                st.markdown("👋 Goodbye! Feel free to come back anytime you have more financial questions.")
            return
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("💭 Analyzing your financial question..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    assistant_response = response.text
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    error_msg = f"⚠️ Sorry, I encountered an error processing your request. Please try again in a moment. Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Chat Controls")
        
        if st.button("🔄 Clear Chat History", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your financial advisor. How can I help you with your financial goals today?"}
            ]
            st.session_state.chat_session = initialize_chat_session(model)
            st.rerun()
        
        st.markdown("---")
        st.header("💡 Financial Tips")
        st.markdown("""
        **For Better Advice:**
        - Be specific about your situation
        - Mention your financial goals
        - Share relevant numbers (if comfortable)
        - Ask follow-up questions
        
        **Remember:** I provide educational guidance, not formal financial advice.
        """)
        
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("• 🚀 Streamlit")
        st.markdown("• 🤖 Google Gemini AI")
        st.markdown("• 💰 Financial Expertise")

if __name__ == "__main__":
    main()
