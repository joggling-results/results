import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='All Time Lists',
                   page_icon=':car:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

# Use cwd to ensure runs on all machines

st.markdown('#### All-Time Lists')

st.write("Use the tabs below to see the fastest jogglers in different events")

data = pd.read_csv('test_results.csv')    ## xlsx not supported.

def all_time_list(distance):
    fastest_times = data[data['Distance']==distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    fastest_times = fastest_times.merge(data,how='left',left_on=['Joggler','Finish Time'],right_on=['Joggler','Finish Time'])
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="min")).astype(int)
    fastest_times = fastest_times[['Ranking','Joggler','Gender','Nationality','Date','Event / Venue','Finish Time']].sort_values('Ranking').reset_index(drop=True)
    return fastest_times

tab1, tab2, tab3 = st.tabs(["3b Mile", "3b 5km", "3b 10km"])

with tab1:
   st.header("3 Ball Mile")
   st.write(all_time_list('3b Mile'))
   
with tab2:
   st.header("3 Ball 5km")
   st.write(all_time_list('3b 5km'))

with tab3:
   st.header("3 Ball 10km")
   st.write(all_time_list('3b 10km'))




# st.write(all_time_list('3b Mile'))

# Then use tabs for the separate distances?