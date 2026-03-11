import streamlit as st
import altair as alt
#from shapely.geometry import shape
from utils.io import load_data

ICE_atd, ICE_arrests, ICE_detentions, ICE_removals, ICE_ex_individuals, ICE_ex_flights, ICE_Countries, ICE_arrest_25, ICE_arrest_26 = load_data()

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


# ---------------------------
# Generate fresh arrest tables
# ---------------------------
def clean_numeric(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"nan": None, "": None})
        .astype(float)
        .fillna(0)
        .astype(int)
    )

for df in [ICE_arrest_25, ICE_arrest_26]:
    df["Male Non-Crim"] = clean_numeric(df["Male Non-Crim"])
    df["Male Crim"] = clean_numeric(df["Male Crim"])
    df["Female Non-Crim"] = clean_numeric(df["Female Non-Crim"])
    df["Female Crim"] = clean_numeric(df["Female Crim"])

    df["Men"] = df["Male Crim"] + df["Male Non-Crim"]
    df["Women"] = df["Female Crim"] + df["Female Non-Crim"]

state_totals25 = ICE_arrest_25.groupby("State")[["Men", "Women"]].sum().reset_index()
state_totals26 = ICE_arrest_26.groupby("State")[["Men", "Women"]].sum().reset_index()

state_debrev = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}

state_totals25["State Name"] = state_totals25["State"].map(state_debrev)
state_totals26["State Name"] = state_totals26["State"].map(state_debrev)

# FIPS ids required for us-10m TopoJSON state map
state_fips = {
    "Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6,
    "Colorado": 8, "Connecticut": 9, "Delaware": 10, "District of Columbia": 11,
    "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, "Illinois": 17,
    "Indiana": 18, "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22,
    "Maine": 23, "Maryland": 24, "Massachusetts": 25, "Michigan": 26,
    "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
    "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34,
    "New Mexico": 35, "New York": 36, "North Carolina": 37, "North Dakota": 38,
    "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42,
    "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46,
    "Tennessee": 47, "Texas": 48, "Utah": 49, "Vermont": 50, "Virginia": 51,
    "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56
}

#converts the state names in the dataframe into the same key (id) used by the map (topojson)
state_totals25["id"] = state_totals25["State Name"].map(state_fips)
state_totals26["id"] = state_totals26["State Name"].map(state_fips)

# Drop unmapped rows to avoid missing data
state_totals25 = state_totals25.dropna(subset=["id"]).copy()
state_totals25["id"] = state_totals25["id"].astype(int)

state_totals26 = state_totals26.dropna(subset=["id"]).copy()
state_totals26["id"] = state_totals26["id"].astype(int)
# ---------------------------
# State choropleths
# ---------------------------
st.header("3) State-level arrests by gender")

#this is the main change ---> Bypasses PyArrow Serialization
us_map = alt.topo_feature(
    "https://vega.github.io/vega-datasets/data/us-10m.json",
    feature="states"
)

selection = alt.selection_point(fields=['State Name'], empty = 'none')

ICE_detention_W25 = (
    alt.Chart(us_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(state_totals25, key="id", fields=["State Name", "Women"])
    ).encode(
        color=alt.Color("Women:Q", scale=alt.Scale(scheme="blues"), title="Women"),
        tooltip=["State Name:N", alt.Tooltip("Women:Q", format=",")],
        opacity = alt.condition(selection, alt.value(1), alt.value(0.3))
    ).add_params(
        selection
    ).project(
        type="albersUsa"
    ).properties(
        width=400, height=250, title="Women detained by ICE 2025"
    )
)

ICE_detention_M25 = (
    alt.Chart(us_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(state_totals25, key="id", fields=["State Name", "Men"])
    ).encode(
        color=alt.Color("Men:Q", scale=alt.Scale(scheme="reds"), title="Men"),
        tooltip=["State Name:N", alt.Tooltip("Men:Q", format=",")],
        opacity = alt.condition(selection, alt.value(1), alt.value(0.3))
    ).add_params(
        selection
    ).project(
        type="albersUsa"
    ).properties(
        width=400, height=250, title="Men detained by ICE 2025"
    )
)

ICE_detention_W26 = (
    alt.Chart(us_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(state_totals26, key="id", fields=["State Name", "Women"])
    )
    .encode(
        color=alt.Color("Women:Q", scale=alt.Scale(scheme="blues"), title="Women"),
        tooltip=["State Name:N", alt.Tooltip("Women:Q", format=",")],
        opacity = alt.condition(selection, alt.value(1), alt.value(0.3))
    ).add_params(
        selection
    )
    .project(type="albersUsa")
    .properties(width=400, height=250, title="Women detained by ICE 2026")
)

ICE_detention_M26 = (
    alt.Chart(us_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(state_totals26, key="id", fields=["State Name", "Men"])
    )
    .encode(
        color=alt.Color("Men:Q", scale=alt.Scale(scheme="reds"), title="Men"),
        tooltip=["State Name:N", alt.Tooltip("Men:Q", format=",")],
        opacity = alt.condition(selection, alt.value(1), alt.value(0.3))
    ).add_params(
        selection
    ).project(
        type="albersUsa"
    ).properties(
        width=400, height=250, title="Men detained by ICE 2026"
    )
)

ICE_detention_25 = (ICE_detention_W25 | ICE_detention_M25).resolve_scale(color="independent")
ICE_detention_26 = (ICE_detention_W26 | ICE_detention_M26).resolve_scale(color="independent")

st.write("Click on a state to compare accross the maps. Hover with your mouse to see the number of arrests in each state. Notice that 2026 data is available but it does not reflect the entire year. This is the most up to date ICE arrest data from US government website.")
st.altair_chart(ICE_detention_25, use_container_width=True)
st.altair_chart(ICE_detention_26, use_container_width=True)

st.write("This graphic contains a lot of useful information we can parse. Firstly, we can see which states had the most ICE arrests in 2025 and compare this to 2026.\
         There are several states where ICE made arrests in 2026 that it did not in 2025 for example. Another interesting piece is the comparison between Men and Women. \
         The detaining of men is orders of magnitude larger than the detaining of women in the same states. We can wonder whether this proportional to the undocumented population or more indicative of men's higher likelihood to be arrested at all.")

world_map = alt.topo_feature(
    "https://raw.githubusercontent.com/vega/vega/refs/heads/main/docs/data/world-110m.json",
    feature="countries"
)

country_iso = {
    "INDIA": 356,
    "CHINA": 156,
    "UNITED STATES": 840,
    "INDONESIA": 360,
    "PAKISTAN": 586,
    "NIGERIA": 566,
    "BRAZIL": 76,
    "BANGLADESH": 50,
    "RUSSIA": 643,
    "MEXICO": 484,
    "JAPAN": 392,
    "ETHIOPIA": 231,
    "PHILIPPINES": 608,
    "EGYPT": 818,
    "VIETNAM": 704,
    "DR CONGO": 180,
    "TURKEY": 792,
    "IRAN": 364,
    "GERMANY": 276,
    "THAILAND": 764,
    "UNITED KINGDOM": 826,
    "FRANCE": 250,
    "ITALY": 380,
    "TANZANIA": 834,
    "SOUTH AFRICA": 710,
    "MYANMAR": 104,
    "KENYA": 404,
    "SOUTH KOREA": 410,
    "COLOMBIA": 170,
    "SPAIN": 724,
    "UGANDA": 800,
    "ARGENTINA": 32,
    "ALGERIA": 12,
    "SUDAN": 729,
    "UKRAINE": 804,
    "IRAQ": 368,
    "AFGHANISTAN": 4,
    "POLAND": 616,
    "CANADA": 124,
    "MOROCCO": 504,
    "SAUDI ARABIA": 682,
    "UZBEKISTAN": 860,
    "PERU": 604,
    "MALAYSIA": 458,
    "ANGOLA": 24,
    "GHANA": 288,
    "MOZAMBIQUE": 508,
    "YEMEN": 887,
    "NEPAL": 524,
    "VENEZUELA": 862,
    "GUATEMALA": 320,
    "BELIZE": 84,
    "EL SALVADOR": 222,
    "HONDURAS": 340,
    "NICARAGUA": 558,
    "COSTA RICA": 188,
    "PANAMA": 591,
    "CUBA": 192,
    "HAITI": 332,
    "DOMINICAN REPUBLIC": 214,
    "BOLIVIA": 68,
    "CHILE": 152,
    "ECUADOR": 218,
    "GUYANA": 328,
    "PARAGUAY": 600,
    "SURINAME": 740,
    "URUGUAY": 858,
    "SOMALIA": 706,
    "CAMEROON": 120,
}

#converts the country names in the dataframe into the same key (id) used by the map (topojson)
ICE_Countries["id"] = ICE_Countries["Country of Citizenship"].map(country_iso)

# Drop unmapped rows to avoid missing data
ICE_Countries = ICE_Countries.dropna(subset=["id"]).copy()
ICE_Countries["id"] = ICE_Countries["id"].astype(int)

ICE_Countries_24 = ICE_Countries[ICE_Countries['Fiscal Year'] == 2024]
ICE_Origins_24 = (ICE_Countries_24.groupby('Country of Citizenship')['Removals'].sum().reset_index())

ICE_Countries_23 = ICE_Countries[ICE_Countries['Fiscal Year'] == 2023]
ICE_Origins_23 = (ICE_Countries_23.groupby('Country of Citizenship')['Removals'].sum().reset_index())

ICE_Countries_22 = ICE_Countries[ICE_Countries['Fiscal Year'] == 2022]
ICE_Origins_22 = (ICE_Countries_22.groupby('Country of Citizenship')['Removals'].sum().reset_index())

ICE_Countries_21 = ICE_Countries[ICE_Countries['Fiscal Year'] == 2021]
ICE_Origins_21 = (ICE_Countries_21.groupby('Country of Citizenship')['Removals'].sum().reset_index())


ICE_world_24= (
    alt.Chart(world_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(ICE_Countries_24, key="id", fields=["Country of Citizenship", "Removals"])
    )
    .encode(
        color=alt.Color("Removals:Q", scale=alt.Scale(scheme="reds"), title="Count"),
        tooltip=["Country of Citizenship:N", alt.Tooltip("Removals:Q", format=",")],
    ).project(
        type="mercator"
    ).properties(
        width=400, height=250, title="Deportees by Country of Origin 2024"
    )
)

ICE_world_23 = (
    alt.Chart(world_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(ICE_Countries_23, key="id", fields=["Country of Citizenship", "Removals"])
    )
    .encode(
        color=alt.Color("Removals:Q", scale=alt.Scale(scheme="reds"), title="Count"),
        tooltip=["Country of Citizenship:N", alt.Tooltip("Removals:Q", format=",")],
    ).project(
        type="mercator"
    ).properties(
        width=400, height=250, title="Deportees by Country of Origin 2023"
    )
)

ICE_world_22 = (
    alt.Chart(world_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(ICE_Countries_22, key="id", fields=["Country of Citizenship", "Removals"])
    )
    .encode(
        color=alt.Color("Removals:Q", scale=alt.Scale(scheme="reds"), title="Count"),
        tooltip=["Country of Citizenship:N", alt.Tooltip("Removals:Q", format=",")],
    ).project(
        type="mercator"
    ).properties(
        width=400, height=250, title="Deportees by Country of Origin 2022"
    )
)

ICE_world_21 = (
    alt.Chart(world_map)
    .mark_geoshape(stroke="white", strokeWidth=0.5)
    .transform_lookup(
        lookup="id",
        #lookup by id and then use the state name
        from_=alt.LookupData(ICE_Countries_21, key="id", fields=["Country of Citizenship", "Removals"])
    )
    .encode(
        color=alt.Color("Removals:Q", scale=alt.Scale(scheme="reds"), title="Count"),
        tooltip=["Country of Citizenship:N", alt.Tooltip("Removals:Q", format=",")],
    ).project(
        type="mercator"
    ).properties(
        width=400, height=250, title="Deportees by Country of Origin 2021"
    )
)
st.header("4) Deportations by Deportee Country of Origin 2021-24")
st.altair_chart((ICE_world_24 |ICE_world_23), use_container_width=True)
st.altair_chart((ICE_world_22 | ICE_world_21), use_container_width=True)

st.write("We can see some interesting patterns here though we should be careful about drawing conclusions. Notice the inclusion of Russia in 2023/24 but not in 2021/22. \
         There is also many countries in Western Asia that are included in 2024 that are not included in any other year. \
         Another interesting feature of this chart is nthe most commonly deported nationality by ICE each year. Many Central \
         American countries feature as we might expect but India is the most common in 2023 which is suprising. This graphic shows many interesting details that could motivate future study.")
