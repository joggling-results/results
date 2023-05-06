import streamlit as st
import pandas as pd
import os
# import openpyxl


# set up app
st.set_page_config(page_title='Joggling', page_icon=':zap:')
st.title('Joggling Results Archive')
st.subtitle('Scott Jenkins & Chris Edwin')

cwd = os.getcwd()
print(cwd)


# data = pd.read_excel('joggling_backup_300423.xlsx')
# print(data.head())

