import streamlit as st
import altair as alt
from utils.io import load_data

ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights = load_data()

st.title("Data Dashboard")
st.write("This dashboard highlights all data frame used with interactive features. \
         Simply find a data frame of interest, select a column and value to filter and explore!")
st.header("• ICE Data")
st.subheader("- ICE Alternatives to Detention Data")

column_1 = st.selectbox("Choose a column to filter", ICE_atd.columns)
value_1 = st.selectbox(
    "Choose a value",
    ICE_atd[column_1].dropna().unique(),
    key="atd"
)
filtered_atd_df = ICE_atd[ICE_atd[column_1] == value_1]
st.dataframe(filtered_atd_df)

st.subheader("- ICE Arrests Data")

column_2 = st.selectbox("Choose a column to filter", ICE_arrests.columns)
value_2 = st.selectbox(
    "Choose a value",
    ICE_arrests[column_2].dropna().unique(),
    key="arrests"
)
filtered_arrests_df = ICE_arrests[ICE_arrests[column_2] == value_2]
st.dataframe(filtered_arrests_df)

st.subheader("- ICE Detentions Data")

column_3 = st.selectbox("Choose a column to filter", ICE_detentions.columns)
value_3 = st.selectbox(
    "Choose a value",
    ICE_detentions[column_3].dropna().unique(),
    key="detentions"
)
filtered_detentions_df = ICE_detentions[ICE_detentions[column_3] == value_3]
st.dataframe(filtered_detentions_df)

st.subheader("- ICE Removals Data")

column_4 = st.selectbox("Choose a column to filter", ICE_removals.columns)
value_4 = st.selectbox(
    "Choose a value",
    ICE_removals[column_4].dropna().unique(),
    key="removals"
)
filtered_removals_df = ICE_removals[ICE_removals[column_4] == value_4]
st.dataframe(filtered_removals_df)

st.subheader("- ICE Expulsions Individual Data")

column_5 = st.selectbox("Choose a column to filter", ICE_ex_individuals.columns)
value_5 = st.selectbox(
    "Choose a value",
    ICE_ex_individuals[column_5].dropna().unique(),
    key="individuals"
)
filtered_individuals_df = ICE_ex_individuals[ICE_ex_individuals[column_5] == value_5]
st.dataframe(filtered_individuals_df)

st.subheader("- ICE Expulsions Flights Data")

column_6 = st.selectbox("Choose a column to filter", ICE_ex_flights.columns)
value_6 = st.selectbox(
    "Choose a value",
    ICE_ex_flights[column_6].dropna().unique(),
    key="flights"
)
filtered_flights_df = ICE_ex_flights[ICE_ex_flights[column_6] == value_6]
st.dataframe(filtered_flights_df)