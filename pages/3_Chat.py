import streamlit as st
from src.summarizer import summarize
import pandas as pd
from datetime import datetime
import asyncio # Import asyncio at the top

# Page Configuration
st.set_page_config(
    page_title="LunarLife - Research Assistant",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (Left unchanged)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #1a1a2e, #16213e);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-in;
    }
    .user-message {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        margin-left: 2rem;
    }
    .ai-message {
        background: rgba(76,175,80,0.1);
        border: 1px solid rgba(76,175,80,0.2);
        margin-right: 2rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .reference-card {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .context-box {
        background: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .suggestion-button {
        background: rgba(76,175,80,0.1);
        border: 1px solid rgba(76,175,80,0.2);
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.2rem;
        cursor: pointer;
    }
    .suggestion-button:hover {
        background: rgba(76,175,80,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Load publications data
@st.cache_data
def load_publications():
    df = pd.read_csv('data/publications_with_abstracts.csv')
    df = df.rename(columns={
        "Title": "title",
        "Abstract": "abstract",
        "Link": "link",
        "Results/Conclusion": "results_conclusion"
    })
    # Ensure all columns exist, adding defaults if necessary
    for col in ["authors", "year"]:
        if col not in df.columns:
            df[col] = "N/A"
    return df.to_dict(orient='records')

publications = load_publications()

def format_citation(pub):
    """Format publication details as a citation"""
    authors = pub.get("authors", "Unknown Authors")
    year = pub.get("year", "N/A")
    title = pub["title"]
    return f"{authors} ({year}). {title}."

# --- Helper function for AI call (using synchronous wrapper) ---
def get_ai_response(title, prompt, method):
    """Synchronously calls the async summarize function."""
    try:
        # Use asyncio.run() to execute the async function and block until it's done.
        # This is the cleanest way to call a simple async function from a sync Streamlit context.
        response = asyncio.run(summarize(
            title=title,
            abstract=prompt,
            method=method
        ))

        # Extract AI reply
        if hasattr(response, "error") and response.error:
            return f"⚠️ Error: {response.error}"
        elif hasattr(response, "key_findings") and response.key_findings:
            # Join findings into a single string for display
            return "\n".join(response.key_findings) 
        elif hasattr(response, "results") and response.results:
            return response.results
        elif hasattr(response, "introduction") and response.introduction:
            return response.introduction
        else:
            return "The AI did not return a structured response. Try rephrasing your question."
            
    except Exception as e:
        return f"An unexpected error occurred during AI processing: {str(e)}"

# --- Main Application Logic ---
def main():
    # Header
    col1, col2 = st.columns([2,3])
    with col1:
        st.image("assets/nasa_logo.png", width=100)
    with col2:
        st.title("Space Biology Research Assistant")
        st.markdown("""
        Your AI-powered guide to NASA's space biology research. Ask questions about specific studies 
        or explore broader topics in space biology research.
        """)

    # Sidebar controls
    with st.sidebar:
        st.image("assets/logorm.png", width=100)
        
        st.markdown("### AI Configuration")
        ai_model = st.selectbox(
            "Select AI Model",
            ["ollama", "openai"],
            help="Choose the AI model for research analysis"
        )
        
        st.markdown("### Publication Selection")
        titles = [pub["title"] for pub in publications]
        
        # Use a key to ensure consistent state management for the selection
        selected_title = st.selectbox("Select a publication", titles, key='selected_pub_title')
        
        st.markdown("### Analysis Options")
        include_results = st.checkbox(
            "Include Results/Conclusion in AI prompt",
            help="Include additional context from the research results",
            key='include_results_checkbox'
        )

    # Find selected publication
    publication = next(pub for pub in publications if pub["title"] == selected_title)

    # Display publication context
    st.markdown("### 📚 Current Study Context")
    with st.expander("View Abstract", expanded=False):
        st.markdown(f"""
        <div class="reference-card">
            <h4>{publication['title']}</h4>
            <p><small>{format_citation(publication)}</small></p>
            <hr>
            <p>{publication.get('abstract', 'No abstract available.')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Initialize chat history in session state, specific to the publication
    chat_key = f"chat_history_{selected_title}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    
    # Initialize input for clearing the text area
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""

    # Chat interface
    st.markdown("### 💬 Research Discussion")

    # Display chat history (Iterate backward for "bottom-up" display if preferred, 
    # but the current implementation is fine for top-down)
    for chat in st.session_state[chat_key]:
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <p><strong>You:</strong> {chat['user']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AI response
        st.markdown(f"""
        <div class="chat-message ai-message">
            <p><strong>Research Assistant:</strong></p>
            <p>{str(chat['ai'])}</p>
        </div>
        """, unsafe_allow_html=True)

    # Function to clear the input text after submission
    def clear_input():
        st.session_state['user_input'] = ""

    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input_value = st.text_area(
            "Ask a question about this publication:",
            key="input_text_area", # Key to read the value
            placeholder="e.g., What are the key findings of this research?"
        )
        
        submit_col1, submit_col2 = st.columns([6,1])
        with submit_col2:
            submitted = st.form_submit_button("Send 🚀")

    if submitted and user_input_value:
        # Prepare prompt with abstract and additional context
        prompt = f"""Based on this research abstract, please answer the following question.
        
Abstract: {publication['abstract']}

Question: {user_input_value}"""
        
        if include_results and publication.get("results_conclusion"):
            prompt += f"\n\nAdditional Context - Results/Conclusion: {publication['results_conclusion']}"
        
        with st.spinner("Analyzing research literature..."):
            # CALL THE NEW SYNCHRONOUS HELPER FUNCTION
            response_text = get_ai_response(
                title=selected_title,
                prompt=prompt,
                method=ai_model
            )
            
            # Append to chat history
            st.session_state[chat_key].append({
                "user": user_input_value,
                "ai": response_text
            })
            
            # Rerun the app to display the new chat messages
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6);">
        <p>Powered by NASA data and AI technology 🚀</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()