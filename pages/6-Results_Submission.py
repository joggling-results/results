import streamlit as st

st.set_page_config(page_title='Results Submission',
                   page_icon=':trophy:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )


# st.markdown('#### Joggler Results Submission Form')
#
# st.write('Use the form below to share your joggling results.')

# Bug. Streamlit doesn't allow html components to be responsively sized (for phones and laptops)
# So, have left it so it works well on laptop.
# Can always send people the link to the form if they would like to use it on phone.

html = """
<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSekhuhhZKzYHdS-hN9owER17PPRgxAfC_DODLKGuwZyXHPkOQ/viewform?embedded=true" 
width="900" 
height="1845" 
frameborder="0" 
marginheight="0" 
marginwidth="0">Loading…</iframe>
"""
with st.container():
    st.components.v1.html(html,
                          width=None,
                          height=800,
                          scrolling=True)

