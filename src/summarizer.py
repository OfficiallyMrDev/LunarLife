# summarizer.py
import os
import openai
import requests

def summarize_with_openai(title, abstract):
    prompt = f"Title: {title}\nAbstract: {abstract}\n\nSummarize this publication in one sentence."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response['choices'][0]['message']['content']

def summarize_with_ollama(title, abstract, model="llama2"):
    """
    Ollama API: expects a local Ollama server running or remote endpoint.
    """
    prompt = f"Title: {title}\nAbstract: {abstract}\n\nSummarize this publication in one sentence."
    url = f"http://localhost:11434/api/v1/generate"  # Default local Ollama server
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 150
    }
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        return data['completion']  # Ollama returns the text in 'completion'
    except Exception as e:
        return f"Error: {e}"