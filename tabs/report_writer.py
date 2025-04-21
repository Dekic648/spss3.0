import streamlit as st
from utils.story_engine import build_narrative

def show():
    st.header("📝 Report Writer")

    st.markdown("""
    **What is this?**  
    This tool assembles a plain-text summary of your findings — ideal for copying into PowerPoint, Word, or email reports.

    **How to use:**  
    1. Run Insight Generator, Segment Explorer, or Persona Lab  
    2. Manually paste your insights here, or write them live  
    3. This page generates a narrative-style report  
    """)

    example_insights = [
        "High satisfaction users use the app more frequently.",
        "Users aged 45+ are less likely to recommend the service.",
        "Cluster 1 represents highly engaged and loyal users."
    ]

    st.subheader("📋 Example Insights")
    st.write(example_insights)

    st.subheader("📖 Generated Narrative")
    report = build_narrative(example_insights)
    st.text_area("Narrative Output", value=report, height=300)
