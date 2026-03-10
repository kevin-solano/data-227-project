import streamlit as st

st.title("Conclusions")
st.write("Each block of text here is a summary of the larger discussion findings from the visualizations page \
         keeping the scope of the questions from the narrative, think of this page as a conclusion roping everything \
         together.")



st.header("1) How Large is ICE's enforcement activity?")
st.write("Using section 1 from the visualizations page, We notice an overall increasing trend in eforcement activity \
         with emphasis on alternative ways of detention (GPS monitoring, phonecall checkups, etc) [1]. This increasing \
         trend peaked in 2023 with 22277 cases of any type of enforcement, but 2025 hasn't been fully reported yet.")



st.header("2) What is the enforcement pipeline?")

graph = """
digraph EnforcementPipeline {
    rankdir=LR;
    size = "25,15";

    Arrests -> Detentions;
    Arrests -> ATD;
    Detentions -> Removals;
    Detentions -> ATD;
}
"""

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.graphviz_chart(graph)

st.write("While the data isn't granular enough to track individuals, we can create estimates from the number of arrests, \
         detentions, removals, and ATDs across time amd track how an individual may go through the enforcement pipeline.")
st.write("Most people in the pipeline are first arrested and usually led to some form of ATD. Even those \
         who end up being detained seem to be given a setence with ATD. However, due to unkown reasons, a slight decrese \
         in ATD cases and increase in detentions and removals occurred from 2022-2023 to 2023-2024. This could be due to \
         more effective methods of criminal detection, more operations being done to catch criminals, etc.")



st.header("3) What does the history of alternatives to detention look like ?")
st.write("Using s.")



st.header("4) The impact of Title 42?")
st.write("Using section 1 hasn't been fully reported yet.")



st.header("5) Do different countries experience different enforcement outcomes?")
st.write("Using ss of any type of enforcement, but 2025 hasn't been fully reported yet.")