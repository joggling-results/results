import streamlit as st
import pandas as pd

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

st.set_page_config(page_title='Joggling', 
                   page_icon=':zap:', 
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

update_date = '19th November 2024'

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
st.write("""Joggling (the hybrid sport of running whilst juggling) is a type of Sport Juggling. It is certainly a niche, but it is far more popular than you might think. 
This web app aims to present an archive of joggling achievements from a growing community of athletes around the world. So far...
""")

## Load data and reorder columns
data = pd.read_csv('data/results.csv')    ## xlsx not supported.

column_order = ['Date', 'Joggler', 'Distance', 'Event / Venue','Finish Time', 'IAAF Points', 'Drops',
            'Gender', 'Nationality', 'Notes / Result Links',]
data = data.reindex(columns=column_order)


# Remove relays to get an accurate count of jogglers
num_jogglers = len(data[~data['Distance'].isin(['3b 4x100m','3b 4x200m','3b 4x400m'])]['Joggler'].unique())

# Same for number of nationalities. -1 since 'unknown' is a value in the dataset
num_nationalities = len(data[~data['Distance'].isin(['3b 4x100m','3b 4x200m','3b 4x400m'])]['Nationality'].unique()) - 1

# Summary stats    
col1, col2, col3 = st.columns(3)
col1.metric(label='Total Joggling Race Results', value = len(data),)
col2.metric(label='Total Jogglers', value = num_jogglers,)
col3.metric(label='Joggling Nationalites', value = num_nationalities,)

st.write("See all results below.")
st.divider()

st.write(filter_dataframe(data))
st.write(f'App Updated: {update_date}')
st.write('Compiled by Scott Jenkins & Chris Edwin; 2 jogglers from the United Kingdom')


## To run this code in terminal
## python -m streamlit run home.py