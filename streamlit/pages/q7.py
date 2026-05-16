import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Demographics Exploration")
st.subheader("How does changing the income threshold affect income disparity when comparing gender and race? 📈")

adult = pd.read_csv('https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv')

np.random.seed(42)

q7 = adult.assign(sex_label=adult['sex'].map({0: 'Female', 1: 'Male'}),
    race=adult['race'].astype(str).str.strip())
q7['simulated_income'] = np.random.normal(40000, 10000, size=len(q7)) + (q7['income'] * 20000)

min_t, max_t = st.select_slider("Select Threshold Range ($K):",
    options=[30, 40, 50, 60, 70, 80],
    value=(40, 60))

threshold_list = [t * 1000 for t in range(min_t, max_t + 10, 10)]
all_races = sorted(q7['race'].unique())
selected = st.multiselect("Filter by Race (Leave empty to show all):", options=all_races, default=[])

race_filter = selected if selected else all_races

results = []
for t in threshold_list:
    prop = (q7.assign(above_thresh=(q7['simulated_income'] > t).astype(int))
            .groupby(['sex_label', 'race'])['above_thresh']
            .mean()
            .reset_index(name='proportion'))
    prop['threshold_val'] = t
    prop['threshold'] = f'${t//1000}K'
    results.append(prop)

q7_fin = pd.concat(results, ignore_index=True)
q7_filtered = q7_fin[q7_fin['race'].isin(race_filter)]

base = alt.Chart(q7_filtered).encode(x=alt.X('threshold_val:Q', 
            title='Income Threshold (USD)', 
            axis=alt.Axis(values=threshold_list, format='$.0f', grid=False, domain=False)),
    y=alt.Y('proportion:Q', 
            title='Proportion Above Threshold', 
            axis=alt.Axis(format='%', gridOpacity=0.4, domain=False)),
    color=alt.Color('race:N', title='Race', scale=alt.Scale(scheme='tableau10')),
    detail='sex_label:N')

lines = base.mark_line(size=1.5, opacity=0.4)

points = base.mark_point(size=160, filled=True, opacity=1).encode(
    shape=alt.Shape('sex_label:N',
        title='Gender',
        scale=alt.Scale(domain=['Male', 'Female'], range=['triangle-up', 'circle']),
        legend=alt.Legend(symbolFillColor='red',
            symbolStrokeColor='red')),tooltip=[alt.Tooltip('threshold', title='Threshold'),
        alt.Tooltip('sex_label', title='Gender'),
        alt.Tooltip('race', title='Race'),
        alt.Tooltip('proportion:Q', title='Proportion', format='.2%')])
chart = (lines + points).properties(height=500,
    title=alt.TitleParams(text=f"Economic Access Disparity ({min_t}K - {max_t}K)",
        subtitle=["Proportion of individuals exceeding income thresholds by race and gender"],
        anchor='start',
        fontSize=20)).configure_view(strokeOpacity=0).configure_axis(labelFontSize=12, titleFontSize=14)

st.altair_chart(chart, use_container_width=True)
st.info("""
**Maximizing Data-Ink Ratio:** Removed chart borders and X-axis gridlines to focus attention entirely on the trend lines and data points.

**Removing Clutter:** Lower the Y-axis grid opacity and removed redundant axis domains for a cleaner view.

**Strategic Highlighting:** Tableau10 palette is better for color accessibility and increased point size to 160 for easier comparison of Gender (shape) and Race (color) .
""")


st.divider()    
st.dataframe(q7_filtered.sort_values(['threshold_val', 'proportion'], ascending=[True, False]))

