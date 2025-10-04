import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="LunarLife",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme and styling
page_style = """
    <style>
    /* Global Styles */
    body {
        background-color: #0d1117;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar customization */
    .css-1d391kg {
        background-color: rgba(15, 20, 25, 0.95);
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Feature cards */
    .description-box {
        padding: 2.5rem;
        border-radius: 1rem;
        max-width: 900px;
        margin: 1.5rem auto;
        font-size: 1.1rem;
        background: linear-gradient(135deg, rgba(30,30,30,0.9), rgba(50,50,50,0.9));
        color: #ffffff;
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        text-align: left;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .description-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Text styling */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    ul {
        line-height: 2;
        padding-left: 0.5rem;
    }

    /* Feature icons */
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        color: #61dafb;
    }
    
    /* Links */
    a {
        color: #61dafb;
        text-decoration: none;
        transition: color 0.2s ease;
    }

    a:hover {
        color: #ffffff;
    }

    /* Custom button styles */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
    }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("assets/logorm.png", width=120)
    st.markdown("<h2 style='text-align: center;'>Project LunarLife</h2>", unsafe_allow_html=True)
    
    # Navigation Menu
    st.markdown("### 🗺️ Navigation")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Dashboard.py")
    if st.button("🔍 Search & Summarize", use_container_width=True):
        st.switch_page("pages/2_Summarizer.py")
    if st.button("💬 Chat Interface", use_container_width=True):
        st.switch_page("pages/3_Chat.py")
    
    # Environment Info
    st.markdown("### ⚙️ Environment")
    if 'OPENAI_API_KEY' in os.environ:
        st.success("OpenAI API: Connected")
    else:
        st.warning("OpenAI API: Not configured")

# Main Content Area
col1, col2, col3 = st.columns([1,4,1])

with col2:
    st.image("assets/logorm.png", width=200)
    st.markdown(
        """
        <div class="description-box">
            <h1 style="text-align: center;">🚀 Welcome to LunarLife</h1>
            <p style="font-size: 1.2rem; text-align: center;">
                Your AI-powered gateway to NASA's Space Biology research, featuring 600+ publications that shape our understanding of life in space.
            </p>
            <hr style="margin: 1.5rem 0; border-color: rgba(255,255,255,0.1);">
            <p style="font-size: 1.1rem;">
                LunarLife leverages cutting-edge AI technology to help scientists, mission planners, and space enthusiasts explore and understand decades of space bioscience research, with a focus on supporting future Moon and Mars missions.
            </p>
        </div>
        
        <div class="description-box">
            <h2>� Key Features</h2>
            <ul style="list-style-type:none; padding-left:0;">
                <li style="margin: 1rem 0;">
                    <span class="feature-icon">🔍</span>
                    <b>Intelligent Search</b>
                    <p>Advanced search capabilities for finding relevant research across radiation, plants, immune systems, and more.</p>
                </li>
                <li style="margin: 1rem 0;">
                    <span class="feature-icon">🤖</span>
                    <b>AI-Powered Summaries</b>
                    <p>Quick, accurate research summaries using state-of-the-art transformer models (GPT-4 & Ollama).</p>
                </li>
                <li style="margin: 1rem 0;">
                    <span class="feature-icon">🧠</span>
                    <b>Knowledge Graphs</b>
                    <p>Interactive visualization of connections between studies, keywords, and biological systems.</p>
                </li>
                <li style="margin: 1rem 0;">
                    <span class="feature-icon">�</span>
                    <b>Interactive Chat</b>
                    <p>Natural language interface for exploring and understanding space biology research.</p>
                </li>
            </ul>
        </div>

        <div class="description-box">
            <h2>🎯 Getting Started</h2>
            <p>Choose your path to explore space biology research:</p>
            <ul style="list-style-type:none; padding-left:0;">
                <li>📚 Browse the publication database</li>
                <li>🔎 Search for specific topics or keywords</li>
                <li>💡 Get AI-generated research summaries</li>
                <li>🗺️ Explore knowledge graphs</li>
            </ul>
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="?page=pages/2_Summarizer.py" target="_self">
                    <button style="
                        background: linear-gradient(135deg, #0ea5e9, #2563eb);
                        color: white;
                        border: none;
                        padding: 0.75rem 2rem;
                        border-radius: 0.5rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    ">Start Exploring</button>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.6);">
            <p>Developed for NASA Space Apps Challenge 2025 | Powered by AI & NASA Data 🌍🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )
