import streamlit as st
import pandas as pd
from datetime import datetime


# import plotly.express as px     # Streamlit won't recognise it!
# import altair as alt

from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider

# Sample data
df = pd.DataFrame({
    'country_code': ['GBR', 'USA', 'CAN', 'FRA', 'AUS', 'GER'],
    'units': [200, 500, 300, 150, 400, 250],
})

# Convert country codes to lat/lon coordinates
coords = {
    'GBR': (54.0269, -2.4769),
    'USA': (37.0902, -95.7129),
    'CAN': (56.1304, -106.3468),
    'FRA': (46.2276, 2.2137),
    'AUS': (-25.2744, 133.7751),
    'GER': (51.1657, 10.4515),
}
df['lat'] = df['country_code'].apply(lambda x: coords[x][0])
df['lon'] = df['country_code'].apply(lambda x: coords[x][1])

# Create ColumnDataSource
source = ColumnDataSource(data=df)

# Define color mapper
color_mapper = LogColorMapper(palette=Viridis256)

# Define tooltips
tooltips = [
    ('Country', '@country_code'),
    ('Units', '@units'),
]

# Create figure
p = figure(
    x_range=(df['lon'].min(), df['lon'].max()),
    y_range=(df['lat'].min(), df['lat'].max()),
    x_axis_type='mercator',
    y_axis_type='mercator',
    tooltips=tooltips,
    width=800,
    height=500,
)

# Add tile provider
p.add_tile(get_provider(CARTODBPOSITRON))

# Add circle glyphs
p.circle(
    x='lon',
    y='lat',
    size='units',
    source=source,
    fill_color={'field': 'units', 'transform': color_mapper},
    line_color=None,
)

# Add hover tool
hover = HoverTool(tooltips=tooltips)
p.add_tools(hover)

# Display plot in Streamlit
st.bokeh_chart(p, use_container_width=True)




# # Create sample data
# data = pd.DataFrame({
#     'country_code': ['GBR', 'USA', 'CAN', 'AUS', 'NZL'],
#     'units': [100, 200, 150, 75, 50],
# })

# data['units'] = pd.to_numeric(data['units'])

# # Load GeoJSON map data for world countries
# world_map = alt.topo_feature('https://vega.github.io/vega-datasets/data/world-110m.json', 'countries')

# # Create Altair chart
# chart = alt.Chart(world_map).mark_geoshape(
#     fill='lightgray',
#     stroke='white'
# ).encode(
#     tooltip=['id:N', 'units:Q'],
#     color=alt.Color('units:Q', scale=alt.Scale(scheme='reds'), legend=alt.Legend(title='Units'))
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(data, 'country_code', 'units')
# ).project(
#     type='mercator'
# ).properties(
#     width=700,
#     height=400
# )

# # Show the chart in Streamlit
# st.altair_chart(chart, use_container_width=True)



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


