import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='All Time Lists',
                   page_icon=':car:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

# Use cwd to ensure runs on all machines

st.markdown('#### Minimising Total Cost of Charging Stations')