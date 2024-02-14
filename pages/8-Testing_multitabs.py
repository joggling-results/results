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
    st.subheader("Endurance Events will sit under this nested tab...")
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
with middle_distance_tab:
    st.subheader('Will move the middle distance events here')
with sprints_tab:
    st.subheader('And Sprints (and relays) will live here')
    