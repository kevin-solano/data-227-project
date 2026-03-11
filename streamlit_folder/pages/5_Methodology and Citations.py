import streamlit as st


st.title("Methodology")
st.write("ICE data involves vulnerable populations, which requires careful handling of sentive information. \
    ICE collects administrative records for every enforcement operation, meaning theese datasets record \
    events like detention book in/out, etc. These records correspond to events, not direct individuals, \
    and identifable information is removed or redacted from public releases.")
st.write("Our datasets did not include personal identifiers and focused on aggregated patterns \
    to avoid identifying specific individuals. \
    Our dataset was obtained from publicly released ICE enforcement \
    datasets that track arrests, detentions, removals, and alternative to detention. \
    We prepared our data for analysis by converting excel sheets into csv files, \
    converting data types, removing headers, and combining fiscal-year files into one dataset.")

st.write("Some caveats and limitations of our analysis include incomplete datasets, event-based data, and missing variables. \
    ICE data some times omit certain enforcement actions, they can be delayed and revised later on. These datasets are meant to \
    track events of immigration detention, not individuals, meaning the people and outcomes cannot always be properly linked across the entire \
    immigration pipeline.")

st.write("With time and more resources, we could integrate immigration court data, asylum outcomes, and regional immigraiton policies. \
    This could help connect actions and policy to legal outcomes and could reveal regional vs national trends.")

st.title("Citations:")
st.markdown("1. [ICE Enforcement and Removal Operations Statistics](https://www.ice.gov/statistics)")
st.markdown("2. [T42 Definition](https://www.cbp.gov/document/foia-record/title-42)")
st.markdown("3. [T42 Timeline](https://www.cbp.gov/newsroom/stats/cbp-enforcement-statistics/title-8-and-title-42-statistics#:~:text=Title%2042%20expulsions%20began%20March,visit%20the%20CBP%20Data%20Portal.)")
st.markdown("4. https://www.ice.gov/detain/detention-management#stats")