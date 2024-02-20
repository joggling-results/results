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
## Start of Page Content
st.markdown('#### Dev: Nested Tabs')

st.write("Use the tabs below to see the fastest male jogglers in different events. Varying degrees of evidence has been found for the below, but these rankings rely on the trust of the joggling community. For official verified Guinness World Records, check out their site.")

data = pd.read_csv('results.csv')
data = data[data['Gender']=='M']        ## xlsx not supported.

def all_time_list(distance):
    # Function to produce all time list for a given distance (e.g. 3b 5km)
    fastest_times = data[data['Distance']==distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    fastest_times = fastest_times.merge(data,how='left',left_on=['Joggler','Finish Time'],right_on=['Joggler','Finish Time'])
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="min")).astype(int)
    fastest_times['Nationality'] = fastest_times['Nationality'].replace({'0':'Unknown'})  # 0 loaded in as a string
    fastest_times = fastest_times[['Ranking','Finish Time', 'Joggler','Gender','Nationality','Date','Event / Venue','Notes / Result Links']].sort_values('Ranking').reset_index(drop=True)
    return fastest_times

endurance_tab, middle_distance_tab, sprints_tab = st.tabs(['Endurance', 'Middle Distance', 'Sprints'])

with endurance_tab:
    t_5km_3b, t_10km_3b, t_hmar_3b, t_mar_3b, t_5km_5b, t_mar_5b = st.tabs(["3b 5km", "3b 10km", '3b Half Marathon', '3b Marathon', '5b 5km','5b Marathon'])
    with t_5km_3b:
        st.subheader("3 Ball 5km")
        st.write(all_time_list('3b 5km'))
    with t_10km_3b:
        st.subheader("3 Ball 10km")
        st.write(all_time_list('3b 10km'))
    with t_hmar_3b:
        st.subheader("3 Ball Half Marathon")
        st.write(all_time_list('3b Half Marathon'))
    with t_mar_3b:
        st.subheader("3 Ball Marathon")
        st.write(all_time_list('3b Marathon'))
    with t_5km_5b:
        st.subheader("5 Ball 5km")
        st.write(all_time_list('5b 5km'))
    with t_mar_5b:
        st.subheader("5 Ball Marathon")
        st.write(all_time_list('5b Marathon'))
with middle_distance_tab:
    t_800_3b, t_1500_3b, t_mile_3b, t_mile_5b = st.tabs(["3b 800m", "3b 1500m", "3b Mile", "5b Mile"])
    with t_800_3b:
        st.subheader("3 Ball 800m")
        st.write(all_time_list('3b 800m'))
    with t_1500_3b:
        st.subheader("3 Ball 1500m")
        st.write(all_time_list('3b 1500m'))
    with t_mile_3b:
        st.subheader("3 Ball Mile")
        st.write(all_time_list('3b Mile'))
    with t_mile_5b:
        st.subheader("5 Ball Mile")
        st.write(all_time_list('5b Mile'))
with sprints_tab:
    t_100_3b,t_100_5b,t_100_7b,t_200_3b,t_400_3b,t_400_5b,t_4x100_3b = st.tabs(["3b 100m", "5b 100m", "7b 100m", "3b 200m", "3b 400m", "5b 400m","3b 4x100m"])
    with t_100_3b:
        st.subheader("3 Ball 100m")
        st.write(all_time_list('3b 100m'))
    with t_100_5b:
        st.subheader("5 Ball 100m")
        st.write(all_time_list('5b 100m'))
    with t_100_7b:
        st.subheader("7 Ball 100m")
        st.write(all_time_list('7b 100m'))
    with t_200_3b:
        st.subheader("3 Ball 200m")
        st.write(all_time_list('3b 200m'))
    with t_400_3b:
        st.subheader("3 Ball 400m")
        st.write(all_time_list('3b 400m'))
    with t_400_5b:
        st.subheader("5 Ball 400m")
        st.write(all_time_list('5b 400m'))
    with t_4x100_3b:
        st.subheader("3 Ball 4 x 100m Relay")
        st.write(all_time_list('3b 4x100m'))
    