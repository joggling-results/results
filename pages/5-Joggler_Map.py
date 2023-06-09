import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Joggler Map',
                   page_icon=':pushpin:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )
## To Try:
## pivot_df melted, so can use animation_frame within the plotly geo scatter instead of the slider.
## This should bring more consistency with dot sizes.

def record_year(sample_date):
    # Function to produce the year from a date
    try:
        year = datetime.strptime(sample_date, '%d/%m/%Y').year     # If we have the full date, then extract the year
    except:
        year = int(sample_date)                                    # Else, we only have the year. Use this.
    return year

st.markdown('#### Joggler Map')

st.write('The map shows the number of jogglers from each country, active since the year selected with the slider.')

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


# projections = ['equirectangular', 'mercator', 'orthographic', 'natural earth',
#                        'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area',
#                        'azimuthal equidistant', 'conic equal area', 'conic conformal',
#                        'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer',
#                        'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff']:
with st.container():
    ## Use Slider to select year
    st.session_state['year_val'] = st.slider('Have Joggled Since',
                                             min_value=int(min_year),
                                             max_value=int(max_year),
                                             value=int(min_year))

    st.session_state['map_df'] = pivot_df[pivot_df['Year'] >= st.session_state['year_val']].sum().drop(
        'Year').reset_index().rename({0: 'Number of Jogglers'}, axis=1)
    # st.write(st.session_state['map_df']) # state

    my_map = px.scatter_geo(st.session_state['map_df'],
                            locations="Nationality",
                            locationmode="ISO-3",  # 'country names',
                            size="Number of Jogglers",
                            projection='equirectangular',  # "natural earth",
                            hover_name='Nationality',
                            size_max=100)
    my_map.update_layout(height=800)
    st.plotly_chart(my_map,use_container_width=True,height=800) # Display map in Streamlit app


# ## Example Map
# data = {'country_code': ['GBR', 'USA', 'CAN', 'AUS'],
#         'units': [100, 500, 250, 150]}
# df = pd.DataFrame(data)

# create map with dot size representing number of units
# my_map = px.scatter_geo(df, locations="country_code", size="units",
#                      projection="natural earth", hover_name='country_code',size_max = 50)


