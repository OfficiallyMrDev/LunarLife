import os
import subprocess

# Try importing OpenAI
try:
    import openai
    openai_available = True
except ImportError:
    openai_available = False

def summarize_publication(text, method="openai", max_tokens=200):
    """
    Summarize text using:
    - 'openai': OpenAI GPT API
    - 'ollama': local Ollama model
    """
    if not text or not isinstance(text, str):
        return "No abstract available."

    # --- OpenAI API ---
    if method == "openai" and openai_available:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "OpenAI API key not set."
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize research abstracts clearly and concisely."},
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    # --- Ollama ---
    elif method == "ollama":
        try:
            # Replace 'mistral' with the Ollama model you have installed
            cmd = ["ollama", "run", "gpt-oss:20b-cloud"]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            output, _ = proc.communicate(text)
            return output.strip()
        except Exception:
            return "Ollama summarization failed."

    # --- Fallback ---
    return "No summarization method available or method not installed."