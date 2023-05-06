import pandas as pd
import os
import streamlit

print('all loaded')



# st.set_page_config(page_title='Joggling', page_icon=':zap:')

cwd = os.getcwd()
print(cwd)
data = pd.read_excel('joggling_backup_300423.xlsx')

print(data.head())

