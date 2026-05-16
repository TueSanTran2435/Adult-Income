import streamlit as st
import pandas as pd
import altair as alt

st.title("Demographics Exploration")
st.subheader("What is the relationship between education level and the likelihood of earning more than $50K?")
st.space()

adult = pd.read_csv("https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv")
q2_data = adult.copy()

min_edu = int(q2_data['education_num'].min())
max_edu = int(q2_data['education_num'].max())

edu_range = st.slider(
    "Select range of years of education:",
    min_value=min_edu,
    max_value=max_edu,
    value=(min_edu, max_edu))

summary_df = q2_data[(q2_data['education_num'] >= edu_range[0]) & (q2_data['education_num'] <= edu_range[1])]

education_income = summary_df.groupby(['education_num']).agg(
    income_rate=('income', 'mean')).reset_index()
line_chart = alt.Chart(education_income).mark_line(point=True).encode(
    x=alt.X('education_num:Q', title='Years of Education'),
    y=alt.Y('income_rate:Q', title='Income Probability')
).properties(
    title='Income Probability by Education Level')
st.altair_chart(line_chart)
st.divider()
st.subheader("Statistics")
col1, col2 = st.columns(2)
with col1:
    st.metric("Avg Probability of Earning an Income Higher than $50K (Selected)",
              f"{summary_df['income'].mean():.1%}")
with col2:
    st.metric("Individuals Represented",
              len(summary_df))
st.dataframe(summary_df.sort_values('education_num', ascending=True))