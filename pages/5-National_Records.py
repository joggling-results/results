import streamlit as st
import polars as pl
import pycountry
from pathlib import Path
import re

st.set_page_config(page_title='National Records',
                   page_icon=':rocket:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
)

DATA_DIR = Path("data")

GENDER_LABELS = {"M": "Male", "F": "Female"}


def country_label(code: str) -> str:
    """e.g. 'DEU' -> 'DEU - Germany'. Falls back to the raw code if unrecognized."""
    country = pycountry.countries.get(alpha_3=code)
    return f"{code} - {country.name}" if country else code

## Start of Page Content
st.markdown('#### National Joggling Records')

st.write("Use the tabs below to see the fastest jogglers from different countries. Varying degrees of evidence has been found for the below, but these rankings rely on the trust of the joggling community. For official verified Guinness World Records, check out their site.")

record_files = sorted(DATA_DIR.glob("records_*_*.csv"))
pattern = re.compile(r"records_([MF])_(.+)\.csv")

parsed = [pattern.match(f.name).groups() for f in record_files if pattern.match(f.name)]
genders = sorted({g for g, _ in parsed})
nationality_codes = sorted({n.replace("_", " ") for _, n in parsed})

# Map display label -> underlying code, for both genders and nationalities
gender_display_to_code = {GENDER_LABELS.get(g, g): g for g in genders}
nationality_display_to_code = {country_label(n): n for n in nationality_codes}

col1, col2 = st.columns(2)
with col1:
    selected_gender_display = st.selectbox("Gender", sorted(gender_display_to_code))
with col2:
    selected_nationality_display = st.selectbox("Nationality", sorted(nationality_display_to_code))

selected_gender = gender_display_to_code[selected_gender_display]
selected_nationality = nationality_display_to_code[selected_nationality_display]

filename = f"records_{selected_gender}_{selected_nationality.replace(' ', '_')}.csv"
filepath = DATA_DIR / filename

if filepath.exists():
    records = pl.read_csv(filepath)
    st.subheader(f"{selected_nationality_display} — {selected_gender_display}")
    if records.height == 0:
        st.info("No records yet for this nationality/gender.")
    else:
        st.dataframe(records.to_pandas(), use_container_width=True, hide_index=True)
else:
    st.info("No records available for this selection.")