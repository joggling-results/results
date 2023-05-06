import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='All Time Lists',
                   page_icon=':rocket:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

# Use cwd to ensure runs on all machines

st.markdown('#### All-Time Lists')

st.write("Use the tabs below to see the fastest jogglers in different events")

data = pd.read_csv('test_results.csv')    ## xlsx not supported.

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
 