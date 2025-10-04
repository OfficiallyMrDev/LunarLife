from transformers import pipeline

# Load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_publication(text, max_length=100):
    if not text or not isinstance(text, str):
        return "No abstract available."
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']