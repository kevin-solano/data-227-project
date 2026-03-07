import streamlit as st

st.title("How Does Law Enforcement Deal With Deportations Across Time?\n")
st.write("With the rise of protests and news suggesting excessive force and unlawful arrests/deportations \
         surrounding ICE in the new administration, we decided to explore the data provided by ICE and find trends and \
         changes across recent years by answering questions and drawing a larger narrative with them. We are not here to \
         answer questions about unlawful arrests/deportations or use of excessive force, but to show whether there are \
         changes between the years in arrests, deportations, enforcement, etc.")

st.header("1) How Large is ICE enforcement activity?")
st.write("ICE has many ways of enforcing immigration laws, from less invasive such as regular checkups over zoom \
         to deportations. We hope to quantify the number of each type of enforcement over the years.")

st.header("2) What is the enforcement pipeline?")
st.write("Not all arrests lead to removal from the country, we plan to cross-check numbers to track how many \
         arrests have led to deportations over the years, and check if more deportations are ocurring than arrests.")

st.header("3) History of alternatives to detention (ATD).")
st.write("Trackig the numbers on forms of non-custiodial supervision may show trends changing with more conservative \
         administrations.")

st.header("4) Impact of Title 42.")
st.write("Title 42 is an order that allows for removal without following the formal deportation process. Tracking \
         statistics relating to this order is crucial for understanding social issues in the U.S.")

st.header("5) Do different countries experience different enforcement outcomes?")
st.write("Some countries may have a larger number of deportations while others have more cases of other alternatives \
         to detention. Tracking this can highlight any sort of favoritism toward certain countries.")