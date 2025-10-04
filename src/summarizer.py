# summarizer.py
import os
import openai
import requests
import subprocess
import json

def summarize_with_openai(title, abstract):
    prompt = f"Title: {title}\nAbstract: {abstract}\n\nSummarize this publication in one sentence."
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def summarize_with_ollama(title, abstract, model="gpt-oss:20b-cloud"):
    """
    Ollama CLI: runs a local Ollama model via subprocess.
    """
    prompt = f"Title: {title}\nAbstract: {abstract}\n\nSummarize this publication in one sentence."
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Ollama subprocess timed out."
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def summarize(title, abstract, method="openai"):
    if method == "openai":
        return summarize_with_openai(title, abstract)
    elif method == "ollama":
        return summarize_with_ollama(title, abstract)
    else:
        return f"Error: Unknown method '{method}'. Choose 'openai' or 'ollama'."