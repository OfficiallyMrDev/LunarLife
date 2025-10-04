# summarizer.py
import os
import openai
import requests
import subprocess
import json

def summarize_with_openai(title, abstract, results=None, conclusion=None):
    if results or conclusion:
        combined_abstract = ""
        if abstract:
            combined_abstract += abstract + "\n"
        if results:
            combined_abstract += "Results: " + results + "\n"
        if conclusion:
            combined_abstract += "Conclusion: " + conclusion
    else:
        combined_abstract = abstract
    prompt = f"Please summarize the following publication in three sections: Introduction, Results, Conclusion.\nTitle: {title}\nContent: {combined_abstract}"
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def summarize_with_ollama(title, abstract, results=None, conclusion=None, model="gpt-oss:20b-cloud"):
    """
    Ollama CLI: runs a local Ollama model via subprocess.
    """
    if results or conclusion:
        combined_abstract = ""
        if abstract:
            combined_abstract += abstract + "\n"
        if results:
            combined_abstract += "Results: " + results + "\n"
        if conclusion:
            combined_abstract += "Conclusion: " + conclusion
    else:
        combined_abstract = abstract
    prompt = f"Please summarize the following publication in three sections: Introduction, Results, Conclusion.\nTitle: {title}\nContent: {combined_abstract}"
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

def summarize(title, abstract, method="openai", results=None, conclusion=None):
    if method == "openai":
        return summarize_with_openai(title, abstract, results=results, conclusion=conclusion)
    elif method == "ollama":
        return summarize_with_ollama(title, abstract, results=results, conclusion=conclusion)
    else:
        return f"Error: Unknown method '{method}'. Choose 'openai' or 'ollama'."