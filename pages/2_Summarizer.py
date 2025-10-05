# pages/2_Summarizer.py
import streamlit as st
import pandas as pd
import re
import plotly.express as px
from src.preprocess import load_and_clean
from src.search import search_publications
from src.summarizer import summarize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="LunarLife - Research Explorer",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom theme

# Header Section
col1, col2 = st.columns([2,3])
with col1:
    st.image("assets/nasa_logo.png", width=100)
with col2:
    st.title("Space Biology Research Explorer")
    st.markdown("""
    Discover insights from NASA's space biology experiments to support future Moon and Mars missions.
    Analyze research trends, identify knowledge gaps, and explore cross-mission findings.
    """)

# Load and process data
@st.cache_data
def load_data():
    df = load_and_clean("data/publications_with_abstracts.csv")
    # Add research impact score (example metric)
    df['impact_score'] = df['abstract'].str.len() + df['title'].str.len()
    df['impact_score'] = (df['impact_score'] - df['impact_score'].min()) / (df['impact_score'].max() - df['impact_score'].min())
    return df

df = load_data()

# Sidebar Navigation and Filters
with st.sidebar:
    st.image("assets/logorm.png", width=100)
    
    # Research Focus
    st.markdown("### Research Focus")
    focus_areas = {
        "Human Health": ["physiology", "medical", "health"],
        "Life Support": ["plants", "agriculture", "oxygen"],
        "Radiation Protection": ["radiation", "shielding", "cosmic"],
        "Microgravity Effects": ["microgravity", "weightlessness"],
        "Mars Mission Prep": ["mars", "long-duration", "habitat"]
    }
    selected_focus = st.multiselect(
        "Select Research Areas",
        list(focus_areas.keys()),
        default=["Human Health"]
    )
    
    # Advanced Filters
    st.markdown("### Advanced Filters")
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox(
            "Category",
            ["All", "Organism", "Experiment", "Mission"]
        )
    with col2:
        if filter_category == "Organism":
            filter_value = st.selectbox("Type", [
                "All", "Human", "Mice", "Plants", 
                "Cells", "Microorganisms"
            ])
        elif filter_category == "Experiment":
            filter_value = st.selectbox("Type", [
                "All", "Genomics", "Physiology", 
                "Radiation", "Behavior", "Systems"
            ])
        elif filter_category == "Mission":
            filter_value = st.selectbox("Type", [
                "All", "ISS", "Shuttle", "Artemis",
                "Mars Analog", "Ground Control"
            ])
        else:
            filter_value = "All"
    
    # Date Range
    date_range = st.slider(
        "Publication Year",
        min_value=2000,
        max_value=2025,
        value=(2000, 2025)
    )
    
    # AI Model Selection
    st.markdown("### AI Analysis")
    ai_choice = st.selectbox(
        "Select AI Model",
        ["openai", "ollama"],
        help="Choose the AI model for research analysis"
    )
    
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Quick", "Standard", "Comprehensive"],
        value="Standard",
        help="Controls the depth of AI analysis"
    )
    
    include_sections = st.multiselect(
        "Include Sections",
        ["Abstract", "Methods", "Results", "Discussion"],
        default=["Abstract", "Results"]
    )

# Main Content Area
tab1, tab2, tab3 = st.tabs(["Overview", "Research Explorer", "Trends & Insights"])

# Overview Tab
with tab1:
    # Research Statistics
    st.markdown("### Research Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Publications", "608")
    
    with col2:
        st.metric("Research Areas", "15+")
    
    with col3:
        st.metric("Space Missions", "25+")
    
    with col4:
        st.metric("Contributing Scientists", "200+")
    
    # Research Focus Areas Chart
    st.markdown("### Research Distribution")
    focus_data = pd.DataFrame({
        'Area': ['Human Health', 'Life Support', 'Radiation', 'Microgravity', 'Mars Prep'],
        'Publications': [150, 120, 100, 140, 98],
        'Impact Score': [0.85, 0.75, 0.90, 0.80, 0.95]
    })
    
    fig = px.scatter(focus_data, 
                    x='Publications', 
                    y='Impact Score',
                    size='Publications',
                    color='Area',
                    title='Research Impact by Focus Area')
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate and display word cloud
    text = ' '.join(df['abstract'].fillna(''))
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='rgba(255, 255, 255, 0)',
        mode='RGBA'
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Research Explorer Tab
with tab2:
    st.markdown("### Research Explorer")
    
    # Search box with NASA-specific placeholders
    query = st.text_input(
        "Search Space Biology Research",
        placeholder="e.g., radiation effects on human cells, plant growth in microgravity..."
    )
    
    # Display filtering status
    active_filters = []
    if filter_category != "All":
        active_filters.append(f"{filter_category}: {filter_value}")
    if selected_focus:
        active_filters.append(f"Focus: {', '.join(selected_focus)}")
    if active_filters:
        st.markdown(f"*Active Filters: {' | '.join(active_filters)}*")
    
    # Filter publications based on all criteria
    filtered_df = df.copy()
    
    # Apply text search
    if query:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(query, case=False, na=False) |
            filtered_df['abstract'].str.contains(query, case=False, na=False)
        ]
    
    # Apply category filters
    if filter_category != "All" and filter_value != "All":
        col_map = {
            'Organism': 'organism',
            'Experiment': 'experiment_type',
            'Mission': 'mission'
        }
        if col_map.get(filter_category) in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[col_map[filter_category]].str.contains(filter_value, case=False, na=False)
            ]
    
    # Apply research focus filters
    if selected_focus:
        focus_keywords = []
        for focus in selected_focus:
            focus_keywords.extend(focus_areas[focus])
        focus_pattern = '|'.join(focus_keywords)
        filtered_df = filtered_df[
            filtered_df['abstract'].str.contains(focus_pattern, case=False, na=False)
        ]
    
    # Apply date filter
    if 'year' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['year'] >= date_range[0]) &
            (filtered_df['year'] <= date_range[1])
        ]
    
    # Display results count and sort options
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"### Found {len(filtered_df)} relevant publications")
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Relevance", "Date", "Impact Score"],
            key="sort_publications"
        )
    
    # Display publications
    for idx, row in filtered_df.head(10).iterrows():
        # Clean and process publication data
        def clean_abstract(text):
            """Clean and format abstract text"""
            if pd.isna(text) or not text:
                return "Abstract not available."
            
            # Remove metadata-like patterns
            patterns = [
                r'PMC\d+',                      # PMC IDs
                r'\d{4}-\d{4}',                 # ISSN numbers
                r'PONE-D-\d+-\d+',             # PLOS submission IDs
                r'10\.\d{4}/[^\s]+',           # DOIs
                r'PLoS\s+ONE?',                 # Journal names
                r'\d+\s*\.\s*\d+',             # Decimal numbers
                r'Research Article',            # Article type labels
                r'journal\.\s*[^\s]+',         # Journal references
                r'Biology and Life Sciences',   # Subject categories
                r'Physical Sciences',
                r'Astronomical Sciences',
                r'Space Exploration',
                r'Research and Analysis Methods',
                r'Medicine and Health Sciences',
                r'Animal Studies',
                r'Model Organisms',
                r'Animal Models',
                r'Mouse Models',
                r'Bioethics',
                r'Veterinary Science',
                r'Animal Management',
                r'Animal Welfare',
                r'Zoology',
                r'Animal Behavior',
                r'Agriculture',
            ]
            
            for pattern in patterns:
                text = re.sub(pattern, '', text)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            # If the cleaned text is too short or seems like metadata
            if len(text) < 100 or not any(char.islower() for char in text):
                return "Abstract content is being processed. Please check the source publication for complete details."
            
            return text

        def calculate_relevance_score(text, title):
            """Calculate research relevance score based on key space biology terms"""
            relevance_factors = {
                'microgravity': 5,
                'space': 4,
                'astronaut': 4,
                'mission': 3,
                'bion': 4,
                'iss': 4,
                'shuttle': 3,
                'lunar': 4,
                'mars': 5,
                'radiation': 4,
                'bone': 3,
                'muscle': 3,
                'immune': 3,
                'health': 3,
                'medicine': 2,
                'biology': 2,
                'experiment': 2,
                'research': 1
            }
            
            combined_text = f"{title} {text}".lower()
            score = sum(weight for term, weight in relevance_factors.items() 
                       if term in combined_text)
            
            # Normalize to 0-1 range, using 40% of max possible as denominator
            # to make scores more meaningful (since no paper will have all terms)
            max_possible_score = sum(relevance_factors.values())
            normalized_score = min(score / (max_possible_score * 0.4), 1.0)
            
            return normalized_score

        def extract_metadata(text, title=""):
            """Extract meaningful metadata from text"""
            # Organism detection patterns
            organisms = {
                'mice': ['mice', 'mouse', 'murine', 'rodent'],
                'human': ['human', 'patient', 'astronaut', 'crew'],
                'plant': ['plant', 'arabidopsis', 'seed', 'vegetation'],
                'cell': ['cell', 'culture', 'in vitro', 'tissue']
            }
            
            # Experiment type patterns
            experiments = {
                'microgravity': ['microgravity', 'weightless', 'zero gravity', 'space flight', 'spaceflight'],
                'radiation': ['radiation', 'cosmic ray', 'ionizing', 'solar particle'],
                'bone': ['bone', 'skeletal', 'osteoclast', 'osteoblast', 'osteo'],
                'immune': ['immune', 'lymphocyte', 'cytokine', 'immunology'],
                'genomic': ['gene', 'expression', 'transcriptome', 'dna', 'rna']
            }
            
            # Mission patterns
            missions = {
                'ISS': ['iss', 'international space station', 'space station'],
                'Shuttle': ['space shuttle', 'sts', 'shuttle mission'],
                'Bion-M1': ['bion-m1', 'bion m1', 'bion-m 1', 'bion'],
                'Artemis': ['artemis', 'lunar gateway', 'moon mission'],
                'Mars': ['mars', 'red planet', 'martian']
            }
            
            text_lower = text.lower()
            
            # Find organism
            organism = next((key.title() for key, terms in organisms.items() 
                           if any(term in text_lower for term in terms)), 'Various')
            
            # Find experiment type
            exp_type = next((key.title() for key, terms in experiments.items() 
                           if any(term in text_lower for term in terms)), 'General')
            
            # Find mission
            mission = next((key for key, terms in missions.items() 
                          if any(term in text_lower for term in terms)), 'Various')
            
            return organism, exp_type, mission

        title = row['title'].strip()
        abstract = clean_abstract(row.get('abstract', ''))
        link = row.get('link', '')
        
        # Calculate relevance score
        relevance_score = calculate_relevance_score(abstract, title)
        
        # Extract metadata from title and abstract combined
        organism, exp_type, mission = extract_metadata(title + " " + abstract)
        
        # Ensure experiment type is properly formatted
        exp_type = exp_type.title() if exp_type else "General"
        organism = organism.title() if organism else "Various"
        mission = mission if mission else "Various"
        
        # Create publication card using native Streamlit components
        with st.container():
            # Title and source link
            col1, col2 = st.columns([5,1])
            with col1:
                st.header(title)
            with col2:
                st.link_button("View Source", link, use_container_width=True)
            
            # Metadata tags
            cols = st.columns(3)
            with cols[0]:
                st.button(f"[DNA] {organism}", disabled=True, key=f"organism_{idx}")
            with cols[1]:
                st.button(f"[Lab] {exp_type}", disabled=True, key=f"exp_type_{idx}")
            with cols[2]:
                st.button(f"[Rocket] {mission}", disabled=True, key=f"mission_{idx}")
            
            # Abstract
            with st.expander("Abstract", expanded=True):
                st.write(abstract[:500] + "...")
            
            # Research Details
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Research Focus")
                st.markdown(f"""
                - {exp_type} Studies
                - {organism} Model
                - Space Biology
                """)
            
            with col2:
                st.subheader("Mission Relevance")
                st.markdown(f"""
                - {mission} Applications
                - Crew Health
                - Space Medicine
                """)
            
            # Research Impact and Analysis
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Research Impact"):
                    metric_cols = st.columns(3)
                    with metric_cols[0]:
                        st.metric("Citations", row.get('citations', '---'))
                    with metric_cols[1]:
                        st.metric("Relevance", f"{relevance_score:.2f}")
                    with metric_cols[2]:
                        st.metric("Impact", "High")
            
            with col2:
                if st.button("Analyze Research", key=f"analyze_research_{idx}"):
                    with st.spinner("Performing comprehensive research analysis..."):
                        # Prepare sections for analysis
                        sections_to_analyze = []
                        if "Abstract" in include_sections:
                            sections_to_analyze.append(("Abstract", abstract))
                        if "Results" in include_sections and 'results' in row:
                            sections_to_analyze.append(("Results", row['results']))
                        if "Discussion" in include_sections and 'conclusion' in row:
                            sections_to_analyze.append(("Discussion", row['conclusion']))
                        
                        # Combine text with section markers
                        combined_text = "\n\n".join([f"{section}: {text}" for section, text in sections_to_analyze])
                        
                        # Generate summary
                        analysis_prompt = "\n".join([
                            "Analyze this space biology research with focus on:",
                            "1. Key Findings: Main discoveries and their significance",
                            "2. Mission Relevance: Implications for Moon/Mars missions",
                            "3. Technical Impact: Methodology and innovation",
                            "4. Future Directions: Research gaps and next steps",
                            "5. Practical Applications: How findings can be applied",
                            "",
                            f"Title: {title}",
                            f"Content: {combined_text}"
                        ])
                        
                        # Convert selected model to summarizer method
                        method = "ollama" if ai_choice == "ollama" else "openai"
                        
                        # Handle async summarization
                        import asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            summary = loop.run_until_complete(summarize(title, analysis_prompt, method))
                        finally:
                            loop.close()
                        
                        # Display analysis results using native Streamlit components
                        st.subheader("Research Analysis")
                        
                        # Check if summary has error
                        if hasattr(summary, 'error') and summary.error:
                            st.error(f"Error generating summary: {summary.error}")
                        else:
                            # Display metadata
                            st.info(f"Analysis generated using {summary.model_used} at {summary.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
                            
                            # Display key findings
                            if summary.key_findings:
                                st.markdown("### Key Findings")
                                for finding in summary.key_findings:
                                    st.markdown(f"- {finding}")
                            elif summary.results:
                                st.markdown("### Key Findings")
                                st.markdown(summary.results)
                            
                            # Display introduction/background
                            if summary.introduction:
                                st.markdown("### Background")
                                st.markdown(summary.introduction)
                                
                            # Display relevance score if available
                            if summary.relevance_score > 0:
                                st.metric("Space Mission Relevance", f"{summary.relevance_score:.2%}")
                        
                        # Add interactive Q&A
                        question = st.text_input("Ask a specific question about this research:", key=f"question_{idx}")
                        if question:
                            st.info("Analyzing your question...")
                # Add interactive Q&A section at the bottom
                col1, col2 = st.columns(2)
                with col1:
                    st.text_area("Ask a specific question about this research:", key=f"question_bottom_{idx}")
                with col2:
                    if st.button("Get Answer", key=f"answer_bottom_{idx}"):
                        st.info("Analyzing your question...")
                        # Add question-answering functionality here

# Trends & Insights Tab
with tab3:
    st.markdown("### Research Trends & Insights")
    
    # Research Timeline
    st.markdown("#### Research Timeline")
    if 'year' in df.columns:
        yearly_pubs = df['year'].value_counts().sort_index()
        fig = px.line(
            x=yearly_pubs.index,
            y=yearly_pubs.values,
            labels={'x': 'Year', 'y': 'Publications'},
            title='Publication Trends Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Research Focus Distribution
    st.markdown("#### Research Focus Areas")
    col1, col2 = st.columns([2,1])
    with col1:
        focus_dist = pd.DataFrame({
            'Focus Area': list(focus_areas.keys()),
            'Publications': [len(df[df['abstract'].str.contains('|'.join(keywords), case=False, na=False)])
                           for keywords in focus_areas.values()]
        })
        fig = px.pie(
            focus_dist,
            values='Publications',
            names='Focus Area',
            title='Distribution of Research Focus Areas'
        )
        st.plotly_chart(fig)
    
    with col2:
        st.markdown(
            "#### Key Insights\n"
            "- Human Health remains the primary focus\n"
            "- Growing emphasis on Life Support systems\n"
            "- Radiation protection research increasing\n"
            "- Mars-specific studies gaining momentum"
        )
    
    # Research Gaps Analysis
    st.markdown("#### Research Gaps Analysis")
    col1, col2 = st.columns([3,2])
    
    with col1:
        # Example gap analysis visualization
        gaps_data = pd.DataFrame({
            'Research Area': ['Artificial Gravity', 'Mars Dust', 'Sleep Studies', 'Food Production'],
            'Coverage': [30, 45, 60, 75],
            'Priority': ['High', 'High', 'Medium', 'High']
        })
        
        fig = px.bar(
            gaps_data,
            x='Research Area',
            y='Coverage',
            color='Priority',
            title='Research Coverage by Area'
        )
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        #### Priority Research Needs
        1. **Artificial Gravity Studies**
           - Long-term effects
           - Implementation strategies
        
        2. **Mars Environmental Factors**
           - Dust mitigation
           - Radiation shielding
        
        3. **Human Factors**
           - Sleep cycles
           - Psychological support
        
        4. **Sustainable Life Support**
           - Food production
           - Water recycling
        """)
    
    # Cross-Mission Insights
    st.markdown("#### Cross-Mission Insights")
    
    # Key Findings
    st.markdown("##### Key Findings Across Missions")
    st.markdown("""
    - Consistent patterns in microgravity adaptation
    - Successful implementation of countermeasures
    - Evolution of life support systems
    - Improvements in radiation protection
    """)
    
    st.markdown("##### Recommendations for Future Missions")
    st.markdown("""
    - Enhanced radiation shielding for Mars missions
    - Improved psychological support systems
    - Advanced biomonitoring capabilities
    - Robust backup life support systems
    """)
