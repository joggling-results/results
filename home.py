import streamlit as st
import pandas as pd
from datetime import date

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(page_title='Joggling', 
                   page_icon=':zap:', 
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

update_date = '28th January 2024'

## Function to allow dataframe filtering
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()
    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 20:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
## End of dataframe filtering function

## Start of Page Content
st.title('Joggling Results Archive')
st.write("""Joggling (that is, the hybrid sport of running whilst juggling) is certainly a niche. But it is more popular than you might think. 
This web app aims to present an archive of joggling achievements from around the world.

Please submit joggling results to jogglingresults@gmail.com
""")

## Load data and reorder columns
data = pd.read_csv('results.csv')    ## xlsx not supported.
data = data[['Date', 'Joggler', 'Distance', 'Event / Venue','Finish Time', 'Drops',
             'Gender', 'Nationality', 
             'Notes / Result Links', 'Year','Standard Distance?']]

# Summary Stats
st.write(f"{len(data)} joggling results from {len(data['Joggler'].unique())} jogglers from {len(data['Nationality'].unique())-1} countries discovered so far...")

st.write(filter_dataframe(data))
st.write(f'App Updated: {update_date}')
st.write('Compiled by Scott Jenkins & Chris Edwin; 2 jogglers from the United Kingdom')
