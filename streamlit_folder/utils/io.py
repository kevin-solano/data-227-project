import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    ICE_atd = pd.read_excel("data/ICE_data.xlsx", sheet_name="ICE ATD")
    ICE_arrests = pd.read_excel("data/ICE_data.xlsx", sheet_name="ICE-ERO Administrative Arrests")
    ICE_detentions = pd.read_excel("data/ICE_data.xlsx", sheet_name="ICE Detentions")
    ICE_removals = pd.read_excel("data/ICE_data.xlsx", sheet_name="ICE Removals")
    ICE_ex_individuals = pd.read_excel("data/ICE_data.xlsx", sheet_name='ICE T42 Expulsions Indivduals')
    ICE_ex_flights = pd.read_excel("data/ICE_data.xlsx", sheet_name='ICE T42 Expulsions Flights ')
    ICE_arrest_25 = pd.read_csv("data/ICE25.csv", encoding= "latin-1")
    ICE_arrest_26 = pd.read_csv("data/ICE26(sheet1).csv", encoding= "latin-1")
    ICE_Countries = pd.read_csv("data/ICE_data(ICE Removals).csv", encoding = "latin-1")
    return ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights, ICE_Countries, ICE_arrest_25, ICE_arrest_26 