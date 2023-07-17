import streamlit as st

st.set_page_config(page_title='Results Submission',
                   page_icon=':trophy:',
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
with st.container():
    st.components.v1.html(html,
                          width=None,
                          height=600,
                          scrolling=True,
                          use_container_width=True)

