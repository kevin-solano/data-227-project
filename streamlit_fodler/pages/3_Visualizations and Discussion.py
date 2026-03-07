import streamlit as st
import altair as alt
from utils.io import load_data

ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights = load_data()

st.header("1) Quantifying ICE activity Across Fiscal Years.")
st.write("To visualize this, we first compiled the different tables from the ICE data into one, where each row is a Fiscal Year \
         and columns represents counts of arrests, detentions, removals, T42 expulsions, and ATD. We then used altair to \
         generate the visualization where each bar and color represents a Fiscal Year. the Y axis represents \
         counts for each bar, users can select which form of enforcement to track.")

atd_yearly = ICE_atd.groupby("Fiscal Year").size().reset_index(name="ATD")
arrests_yearly = ICE_arrests.groupby("Fiscal Year").size().reset_index(name="Arrests")
detentions_yearly = ICE_detentions.groupby("Fiscal Year").size().reset_index(name="Detentions")
removals_yearly = ICE_removals.groupby("Fiscal Year").size().reset_index(name="Removals")
expulsions_yearly = ICE_ex_individuals.groupby("Fiscal Year").size().reset_index(name="T42 Expulsions")

combined = atd_yearly.merge(arrests_yearly, on="Fiscal Year", how="outer") \
    .merge(detentions_yearly, on="Fiscal Year", how="outer") \
    .merge(removals_yearly, on="Fiscal Year", how="outer") \
    .merge(expulsions_yearly, on="Fiscal Year", how="outer")


combined = combined.fillna(0)

combined["Total"] = (
    combined["ATD"] +
    combined["Arrests"] +
    combined["Detentions"] +
    combined["Removals"] +
    combined["T42 Expulsions"]
)

long_df = combined.melt(
    id_vars="Fiscal Year",
    var_name="Enforcement_Type",
    value_name="Count"
)

selector = alt.selection_point(
    fields=["Enforcement_Type"],
    bind=alt.binding_select(
        options=[
            "ATD",
            "Arrests",
            "Detentions",
            "Removals",
            "T42 Expulsions",
            "Total"
        ],
        name="Enforcement Type: "
    ),
)
chart = (
    alt.Chart(long_df)
    .mark_bar()
    .encode(
        x=alt.X("Fiscal Year:O", title="Fiscal Year"),
        y=alt.Y("Count:Q", title="Count"),
        color="Fiscal Year:O",
        tooltip=["Fiscal Year", "Enforcement_Type", "Count"]
    )
    .add_params(selector)
    .transform_filter(selector)
    .properties(
        title="ICE Enforcement Actions by Fiscal Year"
    )
)

st.altair_chart(chart, use_container_width=True)

st.write("We noticed that T42 related expulsions happened only from 2021 to 2023, which tracks with the \
         order's timeline [2]. There was an overall increasing trend for all enforcement types but we see an increase in \
         removals and detentions while arrests and ATDs decreased from 2023 to 2024.")
st.write("With this information, we can deduce that there is an overall increasing trend of prosecution of immigration \
         related criminals. While arrests and ATD numbers have gone down, detentions and removals have increased. \
         This could be due to people that got arrested in previous fiscal years were only removed or detained in the next year. \
         There is a discrepancy between the overall numbers of enforcement tactics in 2025 and other years, this could \
         be due to a lack of data reporting, or simply because the dataset wasn't updated. This stops us from comparing \
         enforcement between administrations.")
