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
    fastest_times = data[data['Distance']==distance].groupby(['Joggler'])['Finish Time'].min().reset_index(drop=True)
    fastest_times['Ranking'] = fastest_times['Finish Time'].rank(method="dense")
    return fastest_times

st.write(all_time_list('3b Mile'))