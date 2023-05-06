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
    fastest_times = data[data['Distance']==distance][['Joggler','Finish Time']].groupby(['Joggler']).min().reset_index()
    fastest_times = fastest_times.merge(data,how='left',left_on=['Joggler','Finish Time'],right_on=['Joggler','Finish Time'])
    fastest_times['Ranking'] = pd.to_numeric(fastest_times['Finish Time'].rank(method="min")).astype(int)
    fastest_times = fastest_times[['Ranking','Joggler','Gender','Nationality','Date','Event / Venue','Finish Time']].sort_values('Ranking').reset_index(drop=True)
    return fastest_times

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



# st.write(all_time_list('3b Mile'))

# Then use tabs for the separate distances?