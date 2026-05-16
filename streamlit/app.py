import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title= "Demographics Exploration + Analysis", page_icon="📊", layout="wide")

q1 = st.Page("pages/q1.py", title="How does the probability of earning more than $50K differ when considering gender and racial categories?", icon="📊")

q2 = st.Page("pages/q2.py",title="What is the relationship between education level and the likelihood of earning more than $50K?",icon="📈")

q3 = st.Page("pages/q3.py", title="How do hours worked per week differ between income groups, and does this relationship change based on the occupation of the individual", icon="📦")

q4 = st.Page("pages/q4.py", title="Which occupations have the highest proportion of high-income earners, and how do these patterns differ by education level?", icon="🔥")

q5 = st.Page("pages/q5.py", title="How does an individual’s native country of origin relate to income, and how do these patterns change when comparing U.S.-born and non-U.S.-born individuals?", icon="🫧")

q6 = st.Page("pages/q6.py", title="When grouped by region, do immigrants from different regions show different income patterns in?", icon="📊")

q7 = st.Page("pages/q7.py", title="How does changing the income threshold affect income disparity when comparing gender and race?", icon="📈")

vis_agent = st.Page("pages/vis_agent_page.py", title = "Visualization Agent", icon = "🤖")

pg = st.navigation({"Exploration": [q1, q2, q3, q4, q5, q6, q7], "AI Tools": [vis_agent]})

pg.run()