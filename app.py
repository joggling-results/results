import streamlit as st
import pandas as pd
import os
# import openpyxl


# set up app
st.set_page_config(page_title='Joggling', page_icon=':zap:')
st.title('Joggling Results Archive')
st.subheader('Curated by Scott Jenkins & Chris Edwin')

st.write("""Joggling (that is, the hybrid sport of running whilst juggling) is certainly a niche.
This web app aims to present an archive of 500+ joggling results, achieved by 200+ jogglers.
Feedback and Suggestions to jogglingresults@gmail.com
""")


cwd = os.getcwd()
print(cwd)

data = pd.read_excel('joggling_backup_300423.xlsx')
st.write(data)

