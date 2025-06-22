import streamlit as st

st.set_page_config(page_title="Joggler's Jottings",
                   page_icon=':📝:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.write("#### Joggler's Jottings")
st.write("""Click the buttons below to download the 'Joggler's Jottings', a quarterly newsletter 
         produced to share some of the joggling highlights from the previous months.
""")

# ADD LATEST JOGGLERS JOTTINGS HERE
with open("Jogglers_Jottings/2025_06.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="June 2025",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2025_06.pdf",
                    mime='application/octet-stream')

with open("Jogglers_Jottings/2025_02.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="February 2025",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2025_02.pdf",
                    mime='application/octet-stream')

with open("Jogglers_Jottings/2024_11.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="November 2024",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2024_11.pdf",
                    mime='application/octet-stream')

with open("Jogglers_Jottings/2024_08.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="August 2024",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2024_08.pdf",
                    mime='application/octet-stream')

with open("Jogglers_Jottings/2024_05.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="May 2024",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/2024_05.pdf",
                    mime='application/octet-stream')


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


###############################################################

st.write("The above files are a revival of the original Joggler's Jottings produced by Bill Giduz in the 1980's. See Bill's reports below:")

# October 1981 - Bill Giduz
with open("Jogglers_Jottings/1981_10.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="October 1981",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1981_10.pdf",
                    mime='application/octet-stream')

# January 1982 - Bill Giduz
with open("Jogglers_Jottings/1982_01.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="January 1982",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1982_01.pdf",
                    mime='application/octet-stream')

# January 1986 - Bill Giduz
with open("Jogglers_Jottings/1986_01.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="January 1986",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1986_01.pdf",
                    mime='application/octet-stream')

# April 1987 - Bill Giduz
with open("Jogglers_Jottings/1987_04.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="April 1987",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1987_04.pdf",
                    mime='application/octet-stream')

# September 1987 - Bill Giduz
with open("Jogglers_Jottings/1987_09.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="September 1987",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1987_09.pdf",
                    mime='application/octet-stream')

# December 1987 - Bill Giduz
with open("Jogglers_Jottings/1987_12.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="December 1987",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/1987_12.pdf",
                    mime='application/octet-stream')

######################################################################################
## Other Media
st.divider()
st.write("Additionally, find guidance on getting started in joggling below:")


# Joggling for Jugglers Workshop Plan - Thom Herzmark
with open("Jogglers_Jottings/Joggling_for_Jugglers_Workshop_Plan.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Jogglers for Jugglers Workshop Plan",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/Joggling_for_Jugglers_Workshop_Plan.pdf",
                    mime='application/octet-stream')

# Joggling for Beginners - Community Contributions
with open("Jogglers_Jottings/Joggling_for_Beginners.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Joggling for Beginners",
                    data=PDFbyte,
                    file_name="Jogglers_Jottings/Joggling_for_Beginners.pdf",
                    mime='application/octet-stream')
