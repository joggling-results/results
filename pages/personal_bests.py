import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Personal Bests',
                   page_icon=':alarm_clock:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

# Use cwd to ensure runs on all machines

st.markdown('#### Joggler Personal Best Times')

data = pd.read_csv('test_results.csv')    ## xlsx not supported.