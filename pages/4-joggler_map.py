import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px


## Example bar chart
data = {'x': ['A', 'B', 'C', 'D'],
        'y': [10, 20, 30, 40]}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Create the bar chart
my_bar = px.bar(df, x='x', y='y')

st.plotly_chart(my_bar)


## Example Map
data = {'country_code': ['GBR', 'USA', 'CAN', 'AUS'],
        'units': [100, 500, 250, 150]}
df = pd.DataFrame(data)

# create map with dot size representing number of units
my_map = px.scatter_geo(df, locations="country_code", size="units",
                     projection="natural earth", hover_name='country_code',size_max = 50)

# Display map in Streamlit app
st.plotly_chart(my_map)


