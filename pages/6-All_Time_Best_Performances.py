import streamlit as st
import pandas as pd
from datetime import datetime
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(page_title='All Time Best Performances',
                   page_icon=':rocket:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )
## Start of Page Content
st.markdown('#### All-Time Best Performances')

url = "https://www.worldathletics.org/download/download?filename=b031e933-c722-4d0d-bfb9-9399ff8fb26f.pdf&urlslug=iaaf%20scoring%20tables%20of%20athletics%20-%20outdoor%20"

st.write("""One way to assess the relative strength of joggling performances across genders and event 
         distances is to use the World Athletics Points tables. To download them, [click here](url).
         We have applied them to the Joggling Performances to assess the strongest performances of all times. The tabs below show the performance rank, 
         and the joggler rank (where each athlete appears at most once).
         This does not however, provide a means of comparison across prop types (balls, clubs), or prop numbers (3,4,5,6,7 objects). Why not try Joggling with N+1 for yourself!
         Note that varying degrees of evidence and ratification have been provided for the below, these rankings rely predominantly on the trust of the joggling community. 
         """)

# Define the tabs
perf_tab, joggler_tab = st.tabs(['Performance Rank', 'Joggler Rank'])

with perf_tab:
    st.subheader("Strongest Performances (IAAF Points)")
    st.write(pd.read_csv('data/iaaf_perf_rank.csv'))

with joggler_tab:
    st.subheader("Strongest Jogglers (IAAF Points)")
    st.write(pd.read_csv('data/iaaf_joggler_rank.csv'))

