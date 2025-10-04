import streamlit as st
from src.summarizer import summarize
import pandas as pd

# Load publications data from CSV
@st.cache_data
def load_publications():
    df = pd.read_csv('data/publications_with_abstracts.csv')
    df = df.rename(columns={"Title": "title", "Abstract": "abstract", "Link": "link"})
    publications = df.to_dict(orient='records')
    return publications

publications = load_publications()

def main():
    st.title("Publication Chat")

    # Select AI model
    ai_model = st.selectbox("Select AI model", ["OpenAI", "Ollama"])

    # Select publication title
    titles = [pub["title"] for pub in publications]
    selected_title = st.selectbox("Select a publication", titles)

    # Find selected publication
    publication = next(pub for pub in publications if pub["title"] == selected_title)

    # Display abstract (optional)
    if publication.get("abstract"):
        with st.expander("Abstract"):
            st.write(publication["abstract"])

    # Initialize session state for per-publication chat history
    chat_key = f"chat_history_{selected_title}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    # Use form for user input to allow multiple messages without resetting input
    with st.form(key="chat_form"):
        user_input = st.text_area("Ask a question about this publication:")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Combine abstract with user question for summarization
        combined_abstract = f"{publication.get('abstract', '')}\nQuestion: {user_input}"
        response = summarize(
            title=selected_title,
            abstract=combined_abstract,
            method=ai_model.lower()
        )
        # Update per-publication chat history
        st.session_state[chat_key].append({"user": user_input, "ai": response})

    # Display per-publication chat history with expanders
    chats = st.session_state[chat_key]
    for i, chat in enumerate(chats):
        expanded = (i == len(chats) - 1)
        with st.expander(f"Message {i+1}", expanded=expanded):
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**{ai_model}:** {chat['ai']}")

if __name__ == "__main__":
    main()
