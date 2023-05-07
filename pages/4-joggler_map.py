import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

data = {'country_code': ['GBR', 'USA', 'CAN', 'AUS'],
        'units': [100, 500, 250, 150]}
df = pd.DataFrame(data)

# create map with dot size representing number of units
fig = px.scatter_geo(df, locations="country_code", size="units",
                     projection="natural earth", hover_name='country_code',size_max = 50)

# Display map in Streamlit app
st.plotly_chart(fig)


