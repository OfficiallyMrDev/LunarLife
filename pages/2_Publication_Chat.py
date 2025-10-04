import streamlit as st
from src.summarizer import summarize
import pandas as pd

# Load publications data from CSV
@st.cache_data
def load_publications():
    df = pd.read_csv('data/publications_with_abstracts.csv')
    df = df.rename(columns={"Title": "title", "Abstract": "abstract", "Link": "link", "Results/Conclusion": "results_conclusion"})
    publications = df.to_dict(orient='records')
    return publications

publications = load_publications()

def main():
    st.title("Project LunarLife Publication Chat")

    # Sidebar controls
    ai_model = st.sidebar.selectbox("Select AI model", ["OpenAI", "Ollama"])
    titles = [pub["title"] for pub in publications]
    selected_title = st.sidebar.selectbox("Select a publication", titles)
    include_results = st.sidebar.checkbox("Include Results/Conclusion in AI prompt")

    # Find selected publication
    publication = next(pub for pub in publications if pub["title"] == selected_title)

    # Display abstract in collapsible expander
    if publication.get("abstract"):
        with st.expander("Abstract"):
            st.write(publication["abstract"])

    st.markdown("---")

    # Initialize session state for per-publication chat history
    chat_key = f"chat_history_{selected_title}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    # Use form for user input to allow multiple messages without resetting input
    with st.form(key="chat_form"):
        user_input = st.text_area("Ask a question about this publication:")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Prepare prompt based on checkbox
        prompt = user_input
        if include_results and publication.get("results_conclusion"):
            prompt = f"{user_input}\nResults/Conclusion: {publication['results_conclusion']}"
        response = summarize(
            title=selected_title,
            abstract=prompt,
            method=ai_model.lower()
        )
        # Update per-publication chat history
        st.session_state[chat_key].append({"user": user_input, "ai": response})

    st.markdown("---")
    st.write("")  # Add spacing

    # Display per-publication chat history with expanders
    chats = st.session_state[chat_key]
    for i, chat in enumerate(chats):
        expanded = (i == len(chats) - 1)
        with st.expander(f"Message {i+1}", expanded=expanded):
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**{ai_model}:** {chat['ai']}")

    st.write("")  # Add spacing
    st.markdown("---")

if __name__ == "__main__":
    main()
