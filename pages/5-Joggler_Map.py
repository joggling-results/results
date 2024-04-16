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

# def record_year(sample_date):
#     # Function to produce the year from a date
#     try:
#         year = datetime.strptime(sample_date, '%d/%m/%Y').year     # If we have the full date, then extract the year
#     except:
#         year = int(sample_date)                                    # Else, we only have the year. Use this.
#     return year

st.markdown('#### Joggler Map')

st.write('The map shows the number of jogglers from each country, active since the year selected with the slider.')


@st.cache_data
def make_country_year_pivot() -> pd.DataFrame:
    '''
    Source the results data, group by joggler to get the year of their latest result, and pivot by nationality

    Return:
        pivot_df: pd.DataFrame
    '''
    data = pd.read_csv('data/results.csv')

    grouped_df = (data[['Joggler','Nationality','Year']].groupby('Joggler')
                                                        .max()
                                                        .reset_index())
    grouped_df['Nationality'].replace({'0':'Unknown'}, 
                                      inplace=True)
    
    pivot_df = (pd.pivot_table(grouped_df,
                              values='Joggler',
                              index='Year',
                              columns='Nationality',
                              aggfunc='count')
                  .fillna(0)
                  .reset_index())
    
    return pivot_df



pivot_df = make_country_year_pivot()

# For some reason, swapping to this df breaks it!
# pivot_df = pd.read_csv('data/map_pivot.csv')
# st.write(pivot_df.dtypes)

min_year = pivot_df['Year'].min()
max_year = pivot_df['Year'].max()

if 'year_val' not in st.session_state:
    st.session_state['year_val'] = 1981
if 'map_df' not in st.session_state:
    st.session_state['map_df'] = pivot_df[pivot_df['Year']>=st.session_state['year_val']].sum().drop('Year').reset_index()


with st.container():
    ## Create the map in it's own container
    st.session_state['map_df'] = pivot_df[pivot_df['Year'] >= st.session_state['year_val']].sum().drop('Year').reset_index().rename({0: 'Number of Jogglers'}, axis=1)
    my_map = px.scatter_geo(st.session_state['map_df'],
                            locations="Nationality",
                            locationmode="ISO-3",  # 'country names',
                            size="Number of Jogglers",
                            projection='equirectangular',  # "natural earth",
                            hover_name='Nationality',
                            size_max=100)
    my_map.update_layout(height=800)
    st.plotly_chart(my_map,use_container_width=True,height=800) # Display map in Streamlit app

    ## Use Slider to select year
    st.session_state['year_val'] = st.slider('Have Joggled Since',
                                             min_value=int(min_year),
                                             max_value=int(max_year),
                                             value=int(min_year))


# projections = ['equirectangular', 'mercator', 'orthographic', 'natural earth',
#                        'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area',
#                        'azimuthal equidistant', 'conic equal area', 'conic conformal',
#                        'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer',
#                        'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff']: