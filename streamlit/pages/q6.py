import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Demographics Exploration")
st.subheader("When grouped by region, do immigrants from different regions show different income patterns ? 📊")

merged_country = pd.read_parquet('https://storage.googleapis.com/adult_income_cs329e/clean/merged_country.parquet')
adult = pd.read_csv('https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv')

merged_country['native_country'] = merged_country['native_country'].astype(str).str.strip()
region_map = dict(zip(merged_country['native_country'], merged_country['region']))

q6_data = adult.assign(native_country=adult['native_country'].astype(str).str.strip())
q6_data['region'] = q6_data['native_country'].map(region_map)
   
immigrants_df = q6_data[q6_data['native_country'] != 'United-States'].dropna(subset=['region'])

all_countries = sorted(immigrants_df['native_country'].unique())
selected = st.multiselect("Select specific countries to compare (Leave empty to show all):",
    options=all_countries,
    default=[],
    help="Search and add multiple countries to filter the chart.")
  
sort_choice = st.selectbox("Sort Regions by:",
    options=["Alphabetical", "Average Income (High to Low)", "Average Income (Low to High)"])

if selected:
    filtered_df = immigrants_df[immigrants_df['native_country'].isin(selected)]
else:
    filtered_df = immigrants_df

if not filtered_df.empty:
    if sort_choice == "Average Income (High to Low)":
        order = filtered_df.groupby('region')['income'].mean().sort_values(ascending=False).index
    elif sort_choice == "Average Income (Low to High)":
        order = filtered_df.groupby('region')['income'].mean().sort_values(ascending=True).index
    else:
        order = sorted(filtered_df['region'].unique())
else:
    order = None

fig, ax = plt.subplots(figsize=(14, 6))
    
sns.barplot(data=filtered_df,
    x ='region',
    y ='income',
    hue = None,
    order = order,
    palette = 'magma',
    ax = ax)

plt.title(f"Immigrant Income Rates (Sorted by {sort_choice})")
plt.xlabel("Region")
plt.ylabel("Average Income Rate")
plt.xticks(rotation=45, ha='right')
       
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Country', fontsize='xx-small', ncol=2)  
plt.tight_layout()
st.pyplot(fig)
st.subheader("Statistics")
col1, col2 = st.columns(2)
if not filtered_df.empty:
    region_avg = filtered_df.groupby('region')['income'].mean()
    with col1:st.metric("Average Immigrant Income Rate",f"{filtered_df['income'].mean():.1%}")
    with col2:st.metric("Highest Region Average",f"{region_avg.max():.1%}")
else:
    st.warning("No data available for selected filters.")
st.divider() 
st.subheader("Data Table")
st.dataframe(filtered_df.sort_values(['region', 'income'], ascending=[True, False]))

