import streamlit as st

st.set_page_config(page_title='Jogglers',
                   page_icon=':book:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.write("#### Joggler's Jottings")
st.write("""Click the buttons below to download the 'Joggler's Jottings', a quarterly newsletter 
         produced to share some of the joggling highlights from the past few months.
""")

with open("Jogglers_Jottings/2024_02.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="February 2024",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2024_02.pdf",
                    mime='application/octet-stream')

with open("Jogglers_Jottings/2023_10.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="October 2023",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2023_10.pdf",
                    mime='application/octet-stream')



link = '[GitHub](https://github.com)'
st.markdown(link, unsafe_allow_html=True)


# st.link_button("October 1981", "Jogglers_Jottings/1981_10.html")
