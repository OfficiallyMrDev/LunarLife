import streamlit as st

st.set_page_config(page_title="LunarLife Menu", page_icon="🚀", layout="wide")

st.sidebar.image("assets/logorm.png", width=120)
st.sidebar.markdown("<h2>Project LunarLife</h2>", unsafe_allow_html=True)

page_style = """
    <style>
    body {
        background-color: #0d1117;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .centered {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-direction: column;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .description-box {
        padding: 40px;
        border-radius: 15px;
        max-width: 800px;
        margin: 20px auto;
        font-size: 18px;
        background: linear-gradient(135deg, rgba(30,30,30,0.8), rgba(50,50,50,0.8));
        color: #ffffff;
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
    }
    .description-box:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    ul {
        line-height: 1.8;
    }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

st.image("assets/logorm.png", width=150,  use_container_width=False)
st.markdown(
    """
    <div class="description-box">
        <h2>🚀 LunarLife</h2>
        <p>
            LunarLife is an interactive AI-powered dashboard that helps scientists, mission planners, and enthusiasts explore 600+ NASA Space Biology publications.
        </p>
        <p>
            It uses AI summarization, knowledge graphs, and intelligent search to uncover the impact of decades of space bioscience research and highlight insights relevant to future missions to the Moon and Mars.
        </p>
        <h3>🌌 Features</h3>
        <ul style="list-style-type:none; padding-left:0; text-align:left;">
            <li>🔍 <b>Smart Search:</b> Search publications by keywords (e.g., radiation, plants, immune system).</li>
            <li>📝 <b>AI Summaries:</b> Automatic summarization of research abstracts using transformer models.</li>
            <li>🧠 <b>Knowledge Graphs:</b> Visualize connections between studies, keywords, and biological systems.</li>
            <li>📊 <b>Interactive Dashboard:</b> Built with Streamlit for fast, user-friendly exploration.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
