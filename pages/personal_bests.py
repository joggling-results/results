import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Personal Bests',
                   page_icon=':alarm_clock:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.markdown('#### Joggler Personal Best Times')

data = pd.read_csv('test_results.csv')    ## xlsx not supported.

pivot_df = pd.pivot_table(data,
                          values='Finish Time',
                          index='Joggler', 
                          columns='Distance', 
                          aggfunc='min')
pivot_df = pivot_df[['3b Mile','3b 5km','3b 10km','3b Half Marathon','3b Marathon','5b Mile']].reset_index().fillna('-')


st.write(pivot_df)