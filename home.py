import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title='Joggling', 
                   page_icon=':zap:', 
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.title('Joggling Results Archive')
st.subheader('Compiled by Scott Jenkins & Chris Edwin, 2 jogglers from the UK')

st.write("""Joggling (that is, the hybrid sport of running whilst juggling) is certainly a niche. But it is more popular than you might think. 
This web app aims to present an archive of joggling achievements from around the world.

Please submit joggling results, and other feedback/suggestions to jogglingresults@gmail.com
""")

data = pd.read_csv('test_results.csv')    ## xlsx not supported.
st.write("{} joggling results from {} jogglers discovered so far...".format(len(data),len(data['Joggler'].unique())))
st.write(data)
st.write('App Updated: 6th May 2022')


## Ideas
## Filter Dataframe: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
## Map of Jogglers
## Personal Best by Jogglers