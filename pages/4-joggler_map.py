import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Joggler Map',
                   page_icon=':pushpin:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'collapsed'   ## 'auto','collapsed','expanded'
                   )

def record_year(sample_date):
    # Function to produce the year from a date
    try:
        year = datetime.strptime(sample_date, '%d/%m/%Y').year     # If we have the full date, then extract the year
    except:
        year = int(sample_date)                                    # Else, we only have the year. Use this.
    return year

st.markdown('#### Joggler Map')

## Load and clean data
data = pd.read_csv('test_results.csv')
## Apply date -> year function
data['Year'] = data.apply(lambda x: record_year(x['Date']),axis=1)
# st.write(data.head(15))
grouped_df = data[['Joggler','Nationality','Year']].groupby('Joggler').max().reset_index()
grouped_df['Nationality'].replace({'0':'Unknown'}, inplace=True)
# st.write(grouped_df)

pivot_df = pd.pivot_table(grouped_df,values='Joggler',index='Year',columns='Nationality',aggfunc='count').fillna(0).reset_index()
# pivot_df['Year'] = pd.to_numeric(pivot_df['Year'])
# st.write(pivot_df)


min_year = pivot_df['Year'].min()
max_year = pivot_df['Year'].max()
if 'year_val' not in st.session_state:
    st.session_state['year_val'] = int(max_year)
if 'map_df' not in st.session_state:
    st.session_state['map_df'] = pivot_df[pivot_df['Year']>=st.session_state['year_val']].sum().drop('Year').reset_index()

## Use Slider to select year
st.session_state['year_val'] = st.slider('Have Joggled Since',
                                         min_value=int(min_year),
                                         max_value=int(max_year),
                                         value=int(max_year))

st.session_state['map_df'] = pivot_df[pivot_df['Year']>=st.session_state['year_val']].sum().drop('Year').reset_index().rename({0:'Number of Jogglers'},axis=1)
st.write(st.session_state['map_df']) # state

my_map = px.scatter_geo(st.session_state['map_df'],
                        locations="Nationality",
                        locationmode = "ISO-3", # 'country names',
                        size="Number of Jogglers",
                        projection='mercator', #"natural earth",
                        hover_name='Nationality') # size_max = 30

with st.container():
    st.plotly_chart(my_map,use_container_width=True) # Display map in Streamlit app


# ## Example Map
# data = {'country_code': ['GBR', 'USA', 'CAN', 'AUS'],
#         'units': [100, 500, 250, 150]}
# df = pd.DataFrame(data)

# create map with dot size representing number of units
# my_map = px.scatter_geo(df, locations="country_code", size="units",
#                      projection="natural earth", hover_name='country_code',size_max = 50)


