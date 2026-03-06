import streamlit as st
from PIL import Image

st.set_page_config(page_title="Narrative Viz Tutorial", layout="wide")

st.title("DATA 22700 Final Project: Following Deportation trends from 2025-2026 in the U.S.")

st.write(Image.open('images/cdac_uchicago_logo.jpeg'))

st.write("This project is intended to highlight trends from given deportation data across multiple\
         sources. Charts are made using Altair, deployment done using Streamlit.\n")
st.write(
    "To explore this visual data story, please navigate it through the pages in the sidebar:\n"
    "- **Central Narrative**: We open with writen objectives and questions we hope to answer with our data.\n"
    "- **Exploration**: We lay down the exploration steps done to understand the data and generate each visualization.\n"
    "- **Visualizations**: Plots with result descriptions and discussions.\n"
    "- **Methodology**: We lay down some key details about our data and limitations to our analysis.\n"
)