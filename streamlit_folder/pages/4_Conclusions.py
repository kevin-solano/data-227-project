import streamlit as st

st.title("Conclusions")
st.write("A summary of the findings from our visualizations page keeping \
    with the scope of the questions from the narrative, think of this page as a conclusion roping everything \
    together.")



st.header("1) How Large is ICE's enforcement activity?")
st.write("From the ICE activity section, we notice an overall increasing trend in eforcement activity \
         with emphasis on alternative ways of detention (GPS monitoring, phonecall checkups, etc) [1]. This increasing \
         trend peaked in 2023 with 22277 cases of any type of enforcement, but 2025 hasn't been fully reported yet.")



st.header("2) What is the enforcement pipeline?")

st.write("While the data isn't granular enough to track individuals, we can create estimates from the number of arrests, \
         detentions, removals, and ATDs across time amd track how an individual may go through the enforcement pipeline.")
st.write("Most people in the pipeline are first arrested and usually led to some form of ATD. Even those \
         who end up being detained seem to be given a setence with ATD. However, due to unkown reasons, a slight decrese \
         in ATD cases and increase in detentions and removals occurred from 2022-2023 to 2023-2024. This could be due to \
         more effective methods of criminal detection, more operations being done to catch criminals, etc.")



st.header("3) Where in the country is ICE most active, how is this changing and how does it vary for Men versus Women?")
st.write("The most impactful statistic shown by this map is the increase in Ice Detentions from 2025 to 2026 in practically every state accross both men and women.\
         This change is even more alarming when you realize that we are still not even halfway through 2026.\
         Notice as well that the scales for both men and women are increased by over 1.5 times in 2026 comopared to 2025.\
         Though we have seen a general increase in ICE activity over the last 6 years, this jump is particularly massive, and particularly difficult to analyze.\
         There was only one reliable data set with information from 2026 and underreporting is almost certainly occurring. Notice that Illinois is not included in any of the four maps, yet I know people personally who were detained by ICE in Illinois.\
         These likely do not classify as arrests, or ICE officers are not obligated to report stops unless they book someone.\
         In any event, this is certainly an under-estimate of ICE activity yet it still shows such a massive increase in just one year.")


st.header("4) What nationalities are targeted most by ICE? How has this changed in recent years?")
st.write("While the counts per country was overall low, there were interesting trends from 2021-2022 to 2023-2024. \
         As time passed, there was a larger number of countries receiving deportees. There were also very unexpected \
         countries with deportees such as Russia and some other Eastern European countries. There was also a noticeable \
         spike in the number of deportees from India from 2023 to 2024. Moreover, there were no deportees going to India \
         in 2021, and a small number in 2022. An unexpected trend showed regarding Mexico, a country with expected high \
         deportation rates, showed a larger number of deportees from there in 2021, but then it rapidly decrease in the \
         following years.")