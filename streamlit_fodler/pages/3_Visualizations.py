import streamlit as st
import altair as alt
import pandas as pd
from shapely.geometry import shape
from utils.io import load_data

ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights, ICE_arrest_25, ICE_arrest_26, USA_Map, USA_df = load_data()

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
        x=alt.X("Fiscal Year:O", 
                axis=alt.Axis(
                    title="Fiscal Year",
                    labelAngle=0
                )
        ),
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

st.header("2) Enforcement Pipeline, Quantifying arrests that lead to detentions and ATD, and from detentions to removals and ATD.")

st.write("Understanding how an individual moves through the enforcement pipeline is crucial in understanding how ICE \
         sees the effectiveness of each method of enforcement. This of course is completely dependent on legislation \
         but can also help determine how legislation has changed across the years, for example more removals point towards \
         legislators believing harsher punishments are more effective.")
st.write("Another important aspect to notice is that to fully track this statistic we would need individual data that can \
         be traced across different tables. This is extremely sensitive data and should only be handled by responsible authorities. \
         To account for this, we decided calculate ratios of for example the number of detentions from 2024-2025 and divide \
         by the number of arrests from the first year. This will give a percentage estimate of arrests in the two \
         years that led to detentions. The choice between two years is due to the fact that ceratin individuals may \
         have been arrested or detained in one year but only processed in the next. The following graph shows a logical \
         understanding of what the pipeline looks like.")

graph = """
digraph EnforcementPipeline {
    rankdir=LR;

    Arrests -> Detentions;
    Arrests -> ATD;
    Detentions -> Removals;
    Detentions -> ATD;
}
"""

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.graphviz_chart(graph)

st.write("The visualization below shows the results of each edge in the graph. Note that the rates are all above 1 (not a \
         true probability). We are trying to only compare previous year arrests with that year and next's possible outcomes. \
         This still gives the reader an idea of how someone may move through the pipeline even without a true percentage.")

combined = combined.sort_values("Fiscal Year")

combined["Detentions_next"] = combined["Detentions"].shift(-1)
combined["Removals_next"] = combined["Removals"].shift(-1)
combined["ATD_next"] = combined["ATD"].shift(-1)

combined["Arrest_to_Detention"] = (
    (combined["Detentions"] + combined["Detentions_next"]) /
    combined["Arrests"]
)

combined["Arrest_to_ATD"] = (
    (combined["ATD"] + combined["ATD_next"]) /
    combined["Arrests"]
)

combined["Detention_to_Removal"] = (
    (combined["Removals"] + combined["Removals_next"]) /
    combined["Detentions"]
)

combined["Detention_to_ATD"] = (
    (combined["ATD"] + combined["ATD_next"]) /
    combined["Detentions"]
)

pipeline = combined.iloc[1:-1]

pipeline_melt = pipeline.melt(
    id_vars="Fiscal Year",
    value_vars=["Arrest_to_Detention", "Detention_to_Removal", "Arrest_to_ATD", "Detention_to_ATD"],
    var_name="Stage",
    value_name="Rate"
)

chart = alt.Chart(pipeline_melt).mark_line(point=True).encode(
    x=alt.X(
        "Fiscal Year:O",
        axis=alt.Axis(
            title="Fiscal Year Window",
            labelExpr="datum.label + '–' + (parseInt(datum.label) + 1)",
            labelAngle=0
        )
    ),
    y="Rate:Q",
    color="Stage:N",
    tooltip=["Fiscal Year", "Stage", "Rate"]
)

st.altair_chart(chart, use_container_width=True)

st.write("Note how the edges leading towards ATD are usually higher than the ones leading towards either \
         detention or removal from the same source. This indicates that law enforcement and legislators tend to \
         prefer alternative methods of enforcement rather than following the traditional pipeline of arrest -> \
         detention -> removal.")
st.write("Note also that there was a slight decrease towards ATD punishements and increase in detentions or removals \
         between 2022-2023 and 2023-2024. We couldn't find any news relating to this change, but this could simply be due \
         to more effective methods of detection which increased the number of arrests and detentions.")

ICE_arrest_26['Male Non-Crim'] = [int(n.replace(',', '')) for n in ICE_arrest_26['Male Non-Crim']]
ICE_arrest_26['Male Non-Crim'] = ICE_arrest_26['Male Non-Crim'].astype(int)
ICE_arrest_26['Male Crim'] = ICE_arrest_26['Male Crim'].astype(int)
ICE_arrest_26['Men'] = ICE_arrest_26['Male Crim'] + ICE_arrest_26['Male Non-Crim']

ICE_arrest_26['Female Crim'] = ICE_arrest_26['Female Crim'].astype(int)
ICE_arrest_26['Female Non-Crim'] = ICE_arrest_26['Female Non-Crim'].astype(int)
ICE_arrest_26['Women'] = ICE_arrest_26['Female Crim'] + ICE_arrest_26['Female Non-Crim']

state_totals26 = (
    ICE_arrest_26.groupby('State')[['Men', 'Women']]
      .sum()
      .reset_index()
)

ICE_arrest_25['Male Non-Crim'] = [int(n.replace(',', '')) for n in ICE_arrest_25['Male Non-Crim']]
ICE_arrest_25['Male Non-Crim'] = ICE_arrest_25['Male Non-Crim'].astype(int)
ICE_arrest_25['Male Crim'] = ICE_arrest_25['Male Crim'].astype(int)
ICE_arrest_25['Men'] = ICE_arrest_25['Male Crim'] + ICE_arrest_25['Male Non-Crim']

ICE_arrest_25['Female Crim'] = ICE_arrest_25['Female Crim'].astype(int)
ICE_arrest_25['Female Non-Crim'] = ICE_arrest_25['Female Non-Crim'].astype(int)
ICE_arrest_25['Women'] = ICE_arrest_25['Female Crim'] + ICE_arrest_25['Female Non-Crim']

state_totals25 = (
    ICE_arrest_25.groupby('State')[['Men', 'Women']]
      .sum()
      .reset_index()
)

state_debrev = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

state_totals25['State Name'] = state_totals25['State'].map(state_debrev)

state_totals26['State Name'] = state_totals26['State'].map(state_debrev)


selection = alt.selection_point(fields=['State Name'], empty = 'none')

all_states = pd.DataFrame({
    'State Name': [f['properties']['NAME'] for f in USA_Map['features']]
})
state_totals25_full = all_states.merge(state_totals25, on='State Name', how='left')

ICE_detention_W25 = alt.Chart(alt.Data(values=USA_Map['features'])
).mark_geoshape(
    stroke='white',
    strokeWidth=0.5
).transform_lookup(
    lookup='properties.NAME',  # column in GeoJSON
    from_= alt.LookupData(state_totals25_full, key='State Name', fields=['Women'])
).encode(  
    color = alt.Color('Women:Q', scale=alt.Scale(scheme='blues'),
                title = 'Total'), 
    tooltip=['properties.NAME:N', 'Women:Q'],
).project(
    type='albersUsa'
).properties(
    width=400
)

ICE_detention_M25  = alt.Chart(
    USA_df,
    title="Men detained by ICE 2025").mark_geoshape(  
    stroke='#706545', 
    strokeWidth=0.75
).transform_lookup(
    lookup='State Name',
    from_=alt.LookupData(state_totals25_full, key= 'State Name', 
        fields=['Men'])
).encode(
    color = alt.Color('Men:Q', scale=alt.Scale(scheme='reds'),
                title = 'Total')
).add_params(
    selection
).properties(
    width=400
)

ICE_detention_25 = (ICE_detention_W25 | ICE_detention_M25).resolve_scale(color='independent')
st.altair_chart(ICE_detention_W25, use_container_width=True) 
