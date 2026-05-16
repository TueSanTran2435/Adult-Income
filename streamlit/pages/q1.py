import streamlit as st
import pandas as pd
import altair as alt

st.title("Demographics Exploration")
st.subheader("How does the probability of earning more than $50K differ when considering gender and racial categories?")
st.space()
adult = pd.read_csv("https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv")
q1_data = adult.copy()
q1_data['sex'] = q1_data['sex'].replace({1: 'Male', 0: 'Female'})

all_races = sorted(q1_data['race'].unique())
all_genders = sorted(q1_data['sex'].unique())
select_races = st.multiselect(
    "Select specific races to compare:",
    options=all_races,
    default=[])
select_genders = st.multiselect(
    "Select gender to compare:",
    options=all_genders,
    default=all_genders
)
if select_races:
    summary_df = q1_data[q1_data['race'].isin(select_races)]
else:
    summary_df = q1_data

summary_df = summary_df[summary_df['sex'].isin(select_genders)]
gender_race = summary_df.groupby(['sex','race']).agg(income_rate=('income','mean')).reset_index()

race_order = (gender_race.groupby('race')['income_rate'].mean().sort_values(ascending=False).index.tolist())
bar_chart_2 = alt.Chart(gender_race).mark_bar().encode(
    x=alt.X('race:N', title='Race', sort=race_order, axis = alt.Axis(labelAngle=0)),
    y=alt.Y('income_rate:Q', title='Income Probability', scale=alt.Scale(domain=[0, gender_race['income_rate'].max()+.2])),
    color=alt.Color('sex:N', scale=alt.Scale(scheme='tableau10')),
    tooltip=['race', 'sex', alt.Tooltip('income_rate:Q', format='.2%')]
).properties(title='Income Probability by Race and Gender').configure_axis(grid=True,gridOpacity = 0.15).configure_view(stroke=None)

st.altair_chart(bar_chart_2)

st.info(""" **Visual Clarity:** Removed outer chart borders and reduced gridline opacity to keep visual emphasis on the bars rather than background elements.

**Improved Comparability:** Sorted racial categories by overall income probability, allowing for identification of highest and lowest earning racial groups.

**Strategic Highlighting:** Applied the Tableau10 color palette for clearer gender differentiation and improved accessibility.

**Accurate Scaling:** Ensured the y-axis begins at zero and added slight padding above the maximum value to prevent compression maintain perception accuracy
""")
st.divider()
st.subheader("Statistics")
col1,col2 = st.columns(2)
with col1:
    st.metric("Avg Probability of Earning an Income Higher than $50K (Selected)",
              f"{summary_df['income'].mean():.1%}")
with col2:
    st.metric("Individuals Represented",
              len(summary_df))
st.dataframe(summary_df.sort_values('income', ascending=False))
