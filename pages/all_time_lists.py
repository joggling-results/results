import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='All Time Lists',
                   page_icon=':car:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

# Use cwd to ensure runs on all machines

st.markdown('#### All Time Lists')

data = pd.read_csv('test_results.csv')    ## xlsx not supported.

def all_time_list(distance):
    fastest_times = data[data['Distance']==distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="dense")).astype(int)
    fastest_times[['Ranking','Joggler','Finish Time']].sort_values('Ranking').reset_index(drop=True)
    return fastest_times

st.write(all_time_list('3b Mile'))

# Then use tabs for the separate distances?