import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Demographics Exploration")
st.subheader("How does an individual’s native country of origin relate to income, and how do these patterns change when comparing U.S.-born and non-U.S.-born individuals? 🫧")

merged_country = pd.read_parquet('https://storage.googleapis.com/adult_income_cs329e/clean/merged_country.parquet')

q5_data = merged_country.copy()
q5_data['native_country'] = q5_data['native_country'].astype(str).str.strip()
q5_data['origin_status'] = np.where(q5_data['native_country'] == 'United-States', 'U.S.-born', 'Non-U.S.-born')

all_countries = sorted(q5_data['native_country'].unique())
    
selected = st.multiselect("Select specific countries to compare (Leave empty to show all):",
    options=all_countries,
    default=[],
    help="Search and add multiple countries to filter the bubble chart.")

if selected:
    display_df = q5_data[q5_data['native_country'].isin(selected)]
else:
    display_df = q5_data

bubble = alt.Chart(display_df).mark_circle(opacity=0.7).encode(
    x = alt.X('native_country:N', title='Native Country', sort='-y'),
    y = alt.Y('income_rate:Q', title='Income Rate', axis=alt.Axis(format='%')),
    size = alt.Size('sample_size:Q',
        title = 'Sample Size',
        scale = alt.Scale(type='log'),
        legend = alt.Legend(symbolFillColor='red', symbolStrokeColor = 'red')),
    color = alt.Color('origin_status:N', title='Origin Status', scale = alt.Scale(scheme = 'set2')),
    tooltip = ['native_country', 'income_rate', 'sample_size']).properties(width = 800, height = 450).interactive()
  
st.altair_chart(bubble)
st.divider()
st.subheader("Statistics")
col1, col2, col3 = st.columns(3)    
with col1:
    st.metric("Avg Income (Selected)", f"{display_df['income_rate'].mean():.1%}")
with col2:
    st.metric("Total Samples", f"{display_df['sample_size'].sum():,}")
with col3:
    st.metric("Countries Shown", len(display_df))

st.dataframe(display_df.sort_values('income_rate', ascending=False))


