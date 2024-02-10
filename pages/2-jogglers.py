import streamlit as st
import pandas as pd
from datetime import datetime

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(page_title='Jogglers',
                   page_icon=':book:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

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
                _min = int(df[column].min())  # float(df[column].min())
                _max = int(df[column].max()) # float(df[column].max())
                step = 1   # (_max - _min) / 100                          # Want integer step sizes
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
st.markdown('#### Joggler Personal Best Times')

data = pd.read_csv('results.csv')    ## xlsx not supported.

# Create table at joggler level: nationality, years active
joggler_df = (data.groupby(['Joggler','Nationality','Gender'])
                  .agg({'Year':['min','max'],'Event / Venue':'count'})
                  .reset_index()
                  .replace({'0':'Unknown'})
)
joggler_df.columns = ['Joggler','Nationality','Gender','First Active','Last Active','Entry Count']
joggler_df['Years Active'] = 1 + joggler_df['Last Active'] - joggler_df['First Active']
joggler_df = joggler_df[['Joggler','Nationality','Gender','Years Active','First Active','Last Active','Entry Count']]

# Create personal best times for common events for each joggler
pivot_df = pd.pivot_table(data,
                          values='Finish Time',
                          index='Joggler', 
                          columns='Distance', 
                          aggfunc='min')
pivot_df = pivot_df[['3b Mile','3b 5km','3b 10km','3b Half Marathon','3b Marathon','5b Mile','5b 5km']].reset_index().fillna('-')

# Merge to produce single joggler_df
joggler_df = joggler_df.merge(pivot_df,on='Joggler')

## Wanted to remove , but it breaks the filtering
# joggler_df = joggler_df.style.format({"Year Most Recently Active": lambda x : str(x)})  

st.write(filter_dataframe(joggler_df))