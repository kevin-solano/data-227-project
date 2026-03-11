import streamlit as st

st.title("How Does Law Enforcement Deal With Deportations Across Time?\n")
st.write("With the rise of protests and news suggesting excessive force \
    and unlawful arrests/deportations \
    surrounding ICE in the new administration, we decided to explore the \
    data provided by ICE and find trends and \
    changes across recent years by answering questions and drawing a larger \
    narrative with them. We are not here to \
    answer questions about unlawful arrests/deportations or use of excessive force, \
    but to show whether there are \
    changes between the years in arrests, deportations, enforcement, etc.")


st.header("1) How Large is ICE's enforcement activity?")
st.write("The scale of ICE's Enforcement and Removal Operations (ERO) is massive, \
    which involves thousands of administrative actions annually. [1] \
    Recorded data from October 2020 through December 2024 shows over 527,000 administrative arrests. \
    During this same period, the agency managed more than 1.1 million \
    initial book-ins into civil immigration detention. The final stages \
    of the pipeline are equally large, with removals and expulsions \
    exceeding 616,000 events. ICE has many ways of enforcing immigration laws, \
    from less invasive such as regular checkups over zoom \
    to deportations. We hope to quantify the number of each \
    type of enforcement over the years.")

st.header("2) What is the enforcement pipeline?")
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
st.write("The enforcement pipeline is the 'Immigration Lifecycle' \
    managed by ERO, encompassing identification, arrest, detention, and removal. \
    Following arrest, officials make custody determinations on an individual basis \
    to decide if a person should be held in physical detention \
    or released under supervision. Not all arrests lead to removal from the country, \
    so we plan to cross-check numbers to track how many \
    arrests have led to deportations over the years, and check \
    the number deportations vs the number of arrests.")


st.header("3) What states have the highest ICE Detainment rates? How do these rates vary for Men versus Women?")
st.write("States with higher detention rates can point to many things. \
    It can point to a larger population of undocumented people but it can also point to a lack of regulation on ICE and law enforcement in those states. \
    There is also a story of overall increase in ICE activity in the US in recent years. \
    Some states which saw no ICE activity now do, and there is no evidence of an increase in undocumented in recent years. \
    We will compare ICE Detentions across US states in 2025 and 2026, seperating by sex to see if any interesting patterns arise. \
    Though some states may be hotspots for both sexes, we see an extroardinary difference in male and female arrest counts in pretty much every state.\
    This could be due to a higher proportion of undocumented persons in the US are men, or simply that men tend to get arrested more than women (which is consistent with general arrest statistics)")

st.header("4) What nationalities are targeted most by ICE? How has this changed in recent years?")
st.write("Enforcement trends are not uniform, they vary significantly by country of citizenship. \
    Some nationalities see a much larger number of deportations than others. \
    The countries that see larger deportations also change significantly over the course of just a few years.\
    Visualizing these outcomes geographically can demonstrate how these trends change over time and show which  \
    nationalities have the highest rates of detention or removal.")