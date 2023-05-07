import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Jogglers',
                   page_icon=':book:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.markdown('#### Joggler Personal Best Times')

data = pd.read_csv('test_results.csv')    ## xlsx not supported.

def record_year(sample_date):
    # Function to clean up the date field, and return only the year as an integer
    try:
        year = datetime.strptime(sample_date, '%d/%m/%Y').year     # If we have the full date, then extract the year
    except:
        year = int(sample_date)                                    # Else, we only have the year. Use this.
    return year

## Apply this function to all dates
data['Year'] = data.apply(lambda x: record_year(x['Date']),axis=1)

nationality_df = data[['Joggler','Nationality']].drop_duplicates().reset_index(drop=True).replace({'0':'Unknown'})
recency_df = data.groupby('Joggler')['Year'].max().reset_index().rename({'Year':'Year Most Recently Active'},axis=1)
pivot_df = pd.pivot_table(data,
                          values='Finish Time',
                          index='Joggler', 
                          columns='Distance', 
                          aggfunc='min')
pivot_df = pivot_df[['3b Mile','3b 5km','3b 10km','3b Half Marathon','3b Marathon','5b Mile']].reset_index().fillna('-')

## Join all dfs on joggler
joggler_df = nationality_df.merge(recency_df,on='Joggler').merge(pivot_df,on='Joggler')
joggler_df = joggler_df.style.format({"Year Most Recently Active": lambda x : str(x)})

st.write(joggler_df)