import streamlit as st
import pandas as pd
import json


@st.cache_data
def load_data():
    ICE_atd = pd.read_excel("../data/ICE_data.xlsx", sheet_name="ICE ATD")
    ICE_arrests = pd.read_excel("../data/ICE_data.xlsx", sheet_name="ICE-ERO Administrative Arrests")
    ICE_detentions = pd.read_excel("../data/ICE_data.xlsx", sheet_name="ICE Detentions")
    ICE_removals = pd.read_excel("../data/ICE_data.xlsx", sheet_name="ICE Removals")
    ICE_ex_individuals = pd.read_excel("../data/ICE_data.xlsx", sheet_name='ICE T42 Expulsions Indivduals')
    ICE_ex_flights = pd.read_excel("../data/ICE_data.xlsx", sheet_name='ICE T42 Expulsions Flights ')
    ICE_arrest_25 = pd.read_csv("data/ICE25.csv", encoding= "latin-1")
    ICE_arrest_26 = pd.read_csv("data/ICE26(sheet1).csv", encoding= "latin-1")
    with open('data/gz_2010_us_040_00_5m.json') as f:
        USA_Map = json.load(f)
    USA_df = pd.read_json('data/gz_2010_us_040_00_5m.json')
    return ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights, ICE_arrest_25, ICE_arrest_26, USA_df, USA_Map 