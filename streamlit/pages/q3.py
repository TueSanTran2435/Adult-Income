import streamlit as st
import pandas as pd
import altair as alt

st.title("Demographics Exploration")
st.subheader("How do hours worked per week differ between income groups, and does this relationship change across occupations?")
st.space()

adult = pd.read_csv("https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv")
q3_data = adult.copy()
alt.data_transformers.disable_max_rows()

q3_data['income_label'] = q3_data['income'].replace({0: '≤ $50K', 1: '> $50K'})
q3_data['occupation_short'] = q3_data['occupation'].str.replace('-', '\n')
top_8 = q3_data['occupation'].value_counts().nlargest(8).index.tolist()
select_occupations = st.multiselect(
    "Select occupations to compare:",
    options=top_8,
    default=top_8)
if select_occupations:
    summary_df = q3_data[q3_data['occupation'].isin(select_occupations)]
else:
    summary_df = q3_data
boxplot_aggregate = alt.Chart(summary_df).mark_boxplot().encode(
    x=alt.X('income_label:O', title='Income Group'),
    y=alt.Y('hours_per_week:Q', title='Hours per Week'),
    color=alt.Color('income_label:N', title='Income Group', sort=['≤ $50K', '> $50K'])
).properties(
    title='Distribution of Weekly Hours by Income Group'
)
st.altair_chart(boxplot_aggregate)
faceted_boxplot = alt.Chart(summary_df).mark_boxplot(extent='min-max').encode(
    x=alt.X('income_label:N', title='Income Group'),
    y=alt.Y('hours_per_week:Q', title='Hours per Week')).facet(
    facet='occupation_short:N',
    columns=4).properties(
    title='Hours Worked by Income Group Across Occupations')

st.altair_chart(faceted_boxplot)
st.divider()

st.subheader("Statistics")
col1, col2 = st.columns(2)
with col1:
    st.metric("Average Hours Worked",
              f"{summary_df['hours_per_week'].mean():.1f}")
with col2:
    st.metric("Individuals Represented",
              len(summary_df))
st.dataframe(summary_df.sort_values('hours_per_week', ascending=False))