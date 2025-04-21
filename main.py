import streamlit as st
from tabs import (
    upload_overview,
    smart_segment_explorer,
    manual_segment_analysis,
    advanced_analysis,
    insight_generator,
    persona_lab,
    simulation_playground,
    report_writer,
    templates_playbook,
    quick_insight_filters
)

st.set_page_config(page_title="SPSS++", layout="wide")

PAGES = {
    "📥 Upload & Overview": upload_overview.show,
    "🧠 Smart Segment Explorer": smart_segment_explorer.show,
    "📊 Manual Segment Analysis": manual_segment_analysis.show,
    "🧪 Advanced Analysis": advanced_analysis.show,
    "🚀 Insight Generator": insight_generator.show,
    "🧬 Persona Lab": persona_lab.show,
    "🎛️ Simulation Playground": simulation_playground.show,
    "📝 Report Writer": report_writer.show,
    "📚 Use-case Templates": templates_playbook.show,
    "⚡ Quick Insight Filters": quick_insight_filters.show,
}

st.sidebar.title("SPSS++ Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[selection]()
