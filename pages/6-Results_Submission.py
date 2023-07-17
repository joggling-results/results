import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Results Submission',
                   page_icon=':pushpin:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )


# st.markdown('#### Joggler Results Submission Form')
#
# st.write('Use the form below to share your joggling results.')

html = """
<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSekhuhhZKzYHdS-hN9owER17PPRgxAfC_DODLKGuwZyXHPkOQ/viewform?embedded=true" 
width="640" 
height="1845" 
frameborder="0" 
marginheight="0" 
marginwidth="0">Loading…</iframe>
"""

st.components.v1.html(html, width=None, height=600, scrolling=True)

