import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Joggler Network",
                   page_icon=':🕸️:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )


## Function to allow dataframe filtering
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()
    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 20:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = int(df[column].min())  # float(df[column].min())
                _max = int(df[column].max()) # float(df[column].max())
                step = 1   # (_max - _min) / 100                          # Want integer step sizes
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
## End of dataframe filtering function

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



## Now include the Bill Giduz Number Dataframe

st.write('''
         Bill Giduz is credited as discovering and naming the sport of Joggling. 
         And so, to pay tribute, we assign each joggler in the archive a **Giduz Number**: 
         the length of the shortest path linking them back to Bill.
         Bill himself as a Giduz number of 0. 
         Any joggler who joggled at an event with Bill has a Giduz number of 1.
         Any joggler who didn't joggle with Bill, but joggled with someone who did has a Giduz number of 2.
         And so it continues. Of course, many jogglers will have an infinite Giduz number - 
         there is no line of jogglers linking them back to Bill - for now!
         
         ''')

giduz_df = pd.read_csv('giduz_df.csv')    ## xlsx not supported.

all_jogglers = len(giduz_df)
no_path = len(giduz_df[giduz_df['Giduz_Path']=='No Connection to Bill Giduz'])

st.write(f'{all_jogglers - no_path} out of {all_jogglers} documented jogglers currently have a finite Giduz Number.')
st.write(filter_dataframe(giduz_df))