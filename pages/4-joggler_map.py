import streamlit as st
import pandas as pd
from datetime import datetime


# import plotly.express as px
import altair as alt

# Create sample data
data = pd.DataFrame({
    'country_code': ['GBR', 'USA', 'CAN', 'AUS', 'NZL'],
    'units': [100, 200, 150, 75, 50],
})

# Load GeoJSON map data for world countries
world_map = alt.topo_feature('https://vega.github.io/vega-datasets/data/world-110m.json', 'countries')

# Create Altair chart
chart = alt.Chart(world_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).encode(
    tooltip=['id:N', 'units:Q'],
    color=alt.Color('units:Q', scale=alt.Scale(scheme='reds'), legend=alt.Legend(title='Units'))
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data, 'country_code', 'units')
).project(
    type='mercator'
).properties(
    width=700,
    height=400
)

# Show the chart in Streamlit
st.altair_chart(chart, use_container_width=True)



# ## Example bar chart
# data = {'x': ['A', 'B', 'C', 'D'],
#         'y': [10, 20, 30, 40]}

# # Convert data to DataFrame
# df = pd.DataFrame(data)

# # Create the bar chart
# my_bar = px.bar(df, x='x', y='y')

# st.plotly_chart(my_bar)


# ## Example Map
# data = {'country_code': ['GBR', 'USA', 'CAN', 'AUS'],
#         'units': [100, 500, 250, 150]}
# df = pd.DataFrame(data)

# # create map with dot size representing number of units
# my_map = px.scatter_geo(df, locations="country_code", size="units",
#                      projection="natural earth", hover_name='country_code',size_max = 50)

# # Display map in Streamlit app
# st.plotly_chart(my_map)


