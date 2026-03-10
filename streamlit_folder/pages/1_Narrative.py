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
    size="25,15";
    
    graph [pad="0.5", nodesep="1", ranksep="1.5", ratio=fill];
    node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=26 margin="0.25,0.15"];
    edge [fontname="Helvetica" fontsize=52 penwidth=2];

    Arrests [label="Identification & Arrest", fillcolor="#ffcccb"];
    Detention [label="Civil Immigration Detention", fillcolor="#ffd966"];
    ATD [label="Alternatives to Detention (ATD)\nGPS • Facial Match • Phone Check-ins", fillcolor="#cfe2f3"];
    Removal [label="Removal / Expulsion\nTitle 8 or Title 42", fillcolor="#d9ead3"];

    Arrests -> Detention [label="Custody Determination"];
    Arrests -> ATD [label="Low Flight Risk"];

    Detention -> Removal [label="Final Order of Removal"];
    Detention -> ATD [label="Release to Monitoring"];
}
"""
col1, col2, col3 = st.columns([0.5,6,0.5])
with col2:
    st.graphviz_chart(graph, use_container_width=True)
st.write("The enforcement pipeline is the 'Immigration Lifecycle' \
    managed by ERO, encompassing identification, arrest, detention, and removal. \
    Following arrest, officials make custody determinations on an individual basis \
    to decide if a person should be held in physical detention \
    or released under supervision. Not all arrests lead to removal from the country, \
    so we plan to cross-check numbers to track how many \
    arrests have led to deportations over the years, and check \
    the number deportations vs the number of arrests.")


st.header("3) History of alternatives to detention (ATD).")
st.write("In cases where physical detention is deemed unnecessary, ICE uses the \
    Alternatives to Detention program (ATD). \
    ATD has evolved to use various technologies to monitor participants remaining \
    in the country. This includes GPS ankle monitoring, telephone reporting via voice \
    recognition, and facial matching technology. As of December 2024, the program has \
    over 187,000 active participants. Tracking the forms of supervision \
    may show trends changing with more conservative administrations.")

st.header("4) The impact of Title 42.")
st.write("Between March 2020 and May 2023, the enforcement pipelin was significanlty \
    altetered by __Title 42 authority__. Unlike Title 8, Title 42 was a public health \
    authority guided by the CDC that allowed for a quicker explusion of undocumented immigrants \
    to prevent the spread of disease, an order that allows for removal \
    without following the formal deportation process. Tracking \
    statistics relating to this order is crucial for \
    understanding social issues in the U.S.")

st.header("5) Do different countries experience different enforcement outcomes?")
st.write("Enforcement trends are not always uniform, they vary significantly by country of citizenship. \
    Some countries may have a larger number of deportations \
    while others have more cases of other alternatives \
    to detention. Visualizing thesse outcomes geographically can demonstrate \
    any disproportionately higher rates of detention or removal across different nationalities.")