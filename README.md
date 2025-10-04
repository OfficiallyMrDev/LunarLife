# 🚀 NASA Bio Explorer Dashboard

**NASA Bio Explorer** is an interactive AI-powered dashboard that helps scientists, mission planners, and enthusiasts explore 600+ NASA Space Biology publications.

It uses **AI summarization, knowledge graphs, and intelligent search** to uncover the impact of decades of space bioscience research and highlight insights relevant to **future missions to the Moon and Mars**.

---

## 🌌 Features

- 🔍 **Smart Search**: Search publications by keywords (e.g., radiation, plants, immune system).
- 📝 **AI Summaries**: Automatic summarization of research abstracts using transformer models.
- 🧠 **Knowledge Graphs**: Visualize connections between studies, keywords, and biological systems.
- 📊 **Interactive Dashboard**: Built with [Streamlit](https://streamlit.io) for fast, user-friendly exploration.

---

## 📂 Project Structure

```nasa-bio-explorer/
│── app.py # Main Streamlit app
│── requirements.txt # Dependencies
│── README.md # Project description
│── data/
│ └── publications.csv # NASA Space Biology publication list
│── src/
│ ├── preprocess.py # Data cleaning & parsing
│ ├── summarizer.py # AI-based summarization
│ ├── knowledge_graph.py # Knowledge graph builder
│ └── search.py # Search & filtering
│── assets/
│ └── demo_slides.pdf # Slides for submission

```
---

## 🚀 Quick Start

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/nasa-bio-explorer.git
   cd nasa-bio-explorer

   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```

3.	Set up AI API keys (optional for OpenAI):

   ```bash
    export OPENAI_API_KEY="your_openai_api_key"

   ```

4. Run the app:

   ```bash
   streamlit run app.py

   ```

4. Open in your browser at:
   ```bash
   http://localhost:8501
   ```

## 🔧 Tech Stack

	•	Python 3.9+
	•	Streamlit – Dashboard UI
	•	OpenAI GPT-4 / Ollama – AI summarization
	•	Pandas – Data handling
	•	NetworkX – Knowledge graph
	•	Matplotlib & PyVis – Visualization

## 📊 Data Sources (NASA)

    •	NASA Space Biology Publications (608 studies)
    •	NASA Open Science Data Repository (OSDR)
    •	NASA Space Life Sciences Library (NSLSL)
    •	NASA Task Book

## 🎥 Demo

Slides or demo video link: [vid]

⸻

## ✨ Team & Credits

Developed for the NASA Space Apps Challenge 2025.
Powered by open-source tools, AI, and NASA data. 🌍🚀

---