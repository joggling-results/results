import streamlit as st
import pandas as pd
from datetime import datetime
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(page_title='All Time Lists',
                   page_icon=':rocket:',
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
st.markdown('#### All-Time Lists (Male)')

st.write("Use the tabs below to see the fastest male jogglers in different events")

data = pd.read_csv('test_results.csv')
data = data[data['Gender']=='M']        ## xlsx not supported.

def all_time_list(distance):
    # Function to produce all time list for a given distance (e.g. 3b 5km)
    fastest_times = data[data['Distance']==distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    fastest_times = fastest_times.merge(data,how='left',left_on=['Joggler','Finish Time'],right_on=['Joggler','Finish Time'])
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="min")).astype(int)
    fastest_times['Nationality'] = fastest_times['Nationality'].replace({'0':'Unknown'})  # 0 loaded in as a string
    fastest_times = fastest_times[['Ranking','Joggler','Gender','Nationality','Date','Event / Venue','Finish Time']].sort_values('Ranking').reset_index(drop=True)
    return fastest_times

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["3b Mile", "3b 5km", "3b 10km",'3b Half Marathon', '3b Marathon', '5b Mile', '5b 5km','5b Marathon'])

with tab1:
   st.subheader("3 Ball Mile")
   st.write(all_time_list('3b Mile'))
with tab2:
   st.subheader("3 Ball 5km")
   st.write(all_time_list('3b 5km'))
with tab3:
   st.subheader("3 Ball 10km")
   st.write(all_time_list('3b 10km'))
with tab4:
   st.subheader("3 Ball Half Marathon")
   st.write(all_time_list('3b Half Marathon'))
with tab5:
   st.subheader("3 Ball Marathon")
   st.write(all_time_list('3b Marathon'))
with tab6:
   st.subheader("5 Ball Mile")
   st.write(all_time_list('5b Mile'))
with tab7:
   st.subheader("5 Ball 5km")
   st.write(all_time_list('5b 5km'))
with tab8:
   st.subheader("5 Ball Marathon")
   st.write(all_time_list('5b Marathon'))
 
 # Looks like you can only filter 1 df in sny given .py file