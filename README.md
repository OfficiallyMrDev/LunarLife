# 🚀 LunarLife

**LunarLife** is an interactive AI-powered dashboard that helps scientists, mission planners, and enthusiasts explore 600+ NASA Space Biology publications.

It uses **AI summarization, knowledge graphs, and intelligent search** to uncover the impact of decades of space bioscience research and highlight insights relevant to **future missions to the Moon and Mars**.

---

## 🌌 Features

- 🔍 **Smart Search**: Search publications by keywords (e.g., radiation, plants, immune system).
- 📝 **AI Summaries**: Automatic summarization of research abstracts using transformer models.
- 🧠 **Knowledge Graphs**: Visualize connections between studies, keywords, and biological systems.
- 📊 **Interactive Dashboard**: Built with [Streamlit](https://streamlit.io) for fast, user-friendly exploration.

---

## 📂 Project Structure

```
LunarLife /
│── app.py                     # Main Streamlit app (search + summaries + knowledge graph)
│── fetch_abstracts.py         # To pull the abstracts via NCBI
│── requirements.txt           # Python dependencies
│── README.md                  # Project description
│── data/
│   │── publications_with_abstracts.csv  # CSV containing titles, links, and abstracts
│   └── publications.csv                 # CSV containing titles, links
│── src/
│   ├── preprocess.py          # Data cleaning & parsing
│   ├── summarizer.py          # AI-based summarization & Q&A (OpenAI & Ollama)
│   └── search.py              # Search & filtering of publications
│── pages/
│   ├── 2_Publication_Chat.py  # Streamlit multi-page: click publication → chat with AI
│── assets/
│   ├── demo_slides.pdf        # Demo slides for submission
│   └── nasa_logo.png          # logo

```

---

## 🚀 Quick Start

1. Clone the repo:

   ```bash
   git clone https://github.com/OfficiallyMrDev/LunarLife.git
   cd LunarLife
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up AI API keys (optional for OpenAI):

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. Run "fetch_abstracts.py" to fetch the publications with the abstracts (If publications_with_abstracts.csv doesn't exist): SKIP

   ```bash
   python run fetch_abstracts.py
   ```

5. Run the app:

   ```bash
   streamlit run Dashboard.py
   ```

6. Open in your browser at:
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
