import streamlit as st
from PIL import Image

st.set_page_config(page_title="Narrative Viz Tutorial", layout="wide")

st.title("DATA 22700 Final Project: Following Deportation trends from 2025-2026 in the U.S.")

st.write(Image.open('images/cdac_uchicago_logo.jpeg'))

st.write("This project is intended to highlight trends from given deportation data across multiple\
         sources. Charts are made using Altair, deployment done using Streamlit.\n")
st.write(
    "To explore this visual data story, please navigate it through the pages in the sidebar:\n"
    "- **Narrative**: We open with writen objectives and questions we hope to answer with our data.\n"
    "- **Data Dashboard**: Interactive Data Frame exploration.\n"
    "- **Visualizations and Discussion**: Plots with result descriptions and discussions.\n"
    "- **Conclusion**: Written compilation of what was learned in this project to complete the central narrative.\n"
    "- **Methodology and Citations**: We lay down some key details about our data and limitations to our analysis. We also link all works used.\n"
)