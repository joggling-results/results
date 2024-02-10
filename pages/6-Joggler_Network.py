import streamlit as st
import streamlit.components.v1 as components

## Start of Page Content
st.markdown('#### Joggler Network')

st.write('''
         Every Joggler in the archive is represented with a dot in the network below. Hover over the dots and zoom in to see who is who. 
         A line is drawn between jogglers if they have joggled together i.e. Same Event & Same Day.
         The more shaded the dot, the more different jogglers they have joggled with.
         ''')

# Open html file
HtmlFile = open("joggler_network.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 

# set the height equal to the plotly figure height
st.components.v1.html(source_code, width=800, height=500, scrolling=False)