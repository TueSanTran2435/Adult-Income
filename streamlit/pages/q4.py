import streamlit as st
import pandas as pd
import altair as alt

st.title("Demographics Exploration")
st.subheader("Which occupations have the highest proportion of high-income earners, and how do these patterns differ by education level? 🔥")

adult = pd.read_csv('https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv')

q4_base = (adult.assign(occupation=adult['occupation'].astype(str).str.strip())
      .groupby(['occupation', 'education_num'])['income']
      .mean()
      .reset_index(name='high_income_prop'))

min_edu, max_edu = st.select_slider("Select Education Year Range:",
    options=sorted(q4_base['education_num'].unique()),
    value=(int(q4_base['education_num'].min()), int(q4_base['education_num'].max())))

all_occupations = sorted(q4_base['occupation'].unique())
selected = st.multiselect("Filter by Occupation (Leave empty to show all):",
    options=all_occupations,
    default=[])

filtered_q4 = q4_base[(q4_base['education_num'] >= min_edu) & 
    (q4_base['education_num'] <= max_edu)]

if selected:
    filtered_q4 = filtered_q4[filtered_q4['occupation'].isin(selected)]

stacked_bar = alt.Chart(filtered_q4).mark_bar().encode(x=alt.X('occupation:N', 
            sort=alt.EncodingSortField(field='high_income_prop', op='sum', order='descending'), 
            title='Occupation',
            axis=alt.Axis(labelAngle=-45, grid=False)),
    y=alt.Y('high_income_prop:Q', 
            title='High-Income Proportion', 
            axis=alt.Axis(format='%', gridOpacity=0.3, domain=False)),
    color=alt.Color('education_num:O', 
                    title='Education (Years)', 
                    scale=alt.Scale(scheme='viridis'),
                    legend=alt.Legend(orient='right', symbolType='square')),
    tooltip=[alt.Tooltip('occupation', title='Occupation'),
        alt.Tooltip('education_num', title='Years of Education'),
        alt.Tooltip('high_income_prop:Q', title='Income Rate', format='.2%')]).properties(width=700, 
    height=450,
    title=alt.TitleParams(text="High-Income Proportion Breakdown by Occupation and Education",
        subtitle=["Visualizing the impact of educational attainment on earnings across different sectors"],
        anchor='start')).configure_view(strokeOpacity=0).interactive()

st.altair_chart(stacked_bar)

st.info("""
**Maximized data-ink ratio:** Removed the outer border and X-axis gridlines to drive attention to the bar heights.

**Dynamic sorting:** The X-axis automatically sorts occupations based on the total high-income proportion of the current selection, making top high earners identifiable.

**Strategic highlighting:** Viridis scale is perceptually uniform and provides better contrast for education levels.
""")

st.divider()

heatmap = alt.Chart(filtered_q4).mark_rect().encode(
    x=alt.X('education_num:O', title='Education Level (Years)', axis=alt.Axis(grid=False)),
    y=alt.Y('occupation:N', sort=alt.EncodingSortField(field='high_income_prop', op='mean', order='descending'),title='Occupation'),
    color=alt.Color('high_income_prop:Q',title='High-Income Proportion',scale=alt.Scale(scheme='viridis'),legend=alt.Legend(format='.0%'))
).properties(
    width=700,
    height=450,
    title=alt.TitleParams(
        text="Heatmap View: Income Probability by Occupation and Education",
        subtitle=["Color intensity represents likelihood of earning >$50K"],
        anchor='start'
    )
).configure_view(
    strokeOpacity=0)

st.altair_chart(heatmap)
st.divider()

st.subheader("Statistics")
col1, col2 = st.columns(2)
with col1:
    st.metric("Average High-Income Proportion (Selected)",f"{filtered_q4['high_income_prop'].mean():.1%}")
with col2:
    st.metric("Occupation-Education Combinations",len(filtered_q4))
st.dataframe(filtered_q4.sort_values(['high_income_prop', 'occupation'], ascending=[False, True]))