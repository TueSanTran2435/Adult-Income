import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from st_aggrid import AgGrid, GridOptionsBuilder

def get_adult():
    return pd.read_csv('https://storage.googleapis.com/adult_income_cs329e/prim/adult_new.csv')

def get_merged_country():
    return pd.read_parquet('https://storage.googleapis.com/adult_income_cs329e/clean/merged_country.parquet')

def get_countries():
    return pd.read_csv('https://storage.googleapis.com/adult_income_cs329e/suppl/countries_new.csv')

def lookup_dataset_by_name(selected_dataset):
    match selected_dataset:
        case 'adult':
            return get_adult()
        case 'merged_country':
            return get_merged_country()
        case 'countries':
            return get_countries()

def render_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filterable=True, selectable=True, filter="agTextColumnFilter") 
    grid_options = gb.build()
    return AgGrid(df, gridOptions=grid_options, height=400)
