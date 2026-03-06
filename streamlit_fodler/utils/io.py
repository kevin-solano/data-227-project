import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    ICE_df = pd.read_excel("../data/ICE_data.xlsx")
    return ICE_df