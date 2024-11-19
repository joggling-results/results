import streamlit as st
import pandas as pd

st.set_page_config(page_title='All Time Lists',
                   page_icon=':rocket:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )
## Start of Page Content
st.markdown('#### All-Time Lists (Male)')

st.write("Use the tabs below to see the fastest male jogglers in different events. Varying degrees of evidence has been found for the below, but these rankings rely on the trust of the joggling community. For official verified Guinness World Records, check out their site.")

# Define the tabs
endurance_tab, middle_distance_tab, sprints_tab = st.tabs(['Endurance', 'Middle Distance', 'Sprints'])

with endurance_tab:
    t_5km_3b, t_10km_3b, t_hmar_3b, t_mar_3b, t_5km_4b, t_10km_4b, t_hmar_4b, t_5km_5b, t_mar_5b = st.tabs(["3b 5km", 
                                                                            "3b 10km", 
                                                                            '3b Half Marathon', 
                                                                            '3b Marathon', 
                                                                            '4b 5km',
                                                                            '4b 10km',
                                                                            '4b Half Marathon',
                                                                            '5b 5km',
                                                                            '5b Marathon'])
    with t_5km_3b:
        st.subheader("3 Ball 5km")
        st.write(pd.read_csv('data/ranking_M_3b_5km.csv'))
    with t_10km_3b:
        st.subheader("3 Ball 10km")
        st.write(pd.read_csv('data/ranking_M_3b_10km.csv'))
    with t_hmar_3b:
        st.subheader("3 Ball Half Marathon")
        st.write(pd.read_csv('data/ranking_M_3b_Half_Marathon.csv'))
    with t_mar_3b:
        st.subheader("3 Ball Marathon")
        st.write(pd.read_csv('data/ranking_M_3b_Marathon.csv'))
    with t_5km_4b:
        st.subheader("4 Ball 5km")
        st.write(pd.read_csv('data/ranking_M_4b_5km.csv'))
    with t_10km_4b:
        st.subheader("4 Ball 10km")
        st.write(pd.read_csv('data/ranking_M_4b_10km.csv'))
    with t_hmar_4b:
        st.subheader("4 Ball Half Marathon")
        st.write(pd.read_csv('data/ranking_M_4b_Half_Marathon.csv'))
    with t_5km_5b:
        st.subheader("5 Ball 5km")
        st.write(pd.read_csv('data/ranking_M_5b_5km.csv'))
    with t_mar_5b:
        st.subheader("5 Ball Marathon")
        st.write(pd.read_csv('data/ranking_M_5b_Marathon.csv'))
with middle_distance_tab:
    t_800_3b, t_1500_3b, t_mile_3b, t_mile_4b, t_mile_5b = st.tabs(["3b 800m", "3b 1500m", "3b Mile", "4b Mile", "5b Mile"])
    with t_800_3b:
        st.subheader("3 Ball 800m")
        st.write(pd.read_csv('data/ranking_M_3b_800m.csv'))
    with t_1500_3b:
        st.subheader("3 Ball 1500m")
        st.write(pd.read_csv('data/ranking_M_3b_1500m.csv'))
    with t_mile_3b:
        st.subheader("3 Ball Mile")
        st.write(pd.read_csv('data/ranking_M_3b_Mile.csv'))
    with t_mile_4b:
        st.subheader("4 Ball Mile")
        st.write(pd.read_csv('data/ranking_M_4b_Mile.csv'))
    with t_mile_5b:
        st.subheader("5 Ball Mile")
        st.write(pd.read_csv('data/ranking_M_5b_Mile.csv'))
with sprints_tab:
    t_100_3b,t_100_4b,t_100_5b,t_100_7b,t_200_3b,t_200_4b,t_200_5b,t_400_3b,t_400_4b,t_400_5b,t_4x100_3b,t_4x400_3b = st.tabs(["3b 100m", 
                                                                                           "4b 100m",
                                                                                           "5b 100m", 
                                                                                           "7b 100m", 
                                                                                           "3b 200m", 
                                                                                           "4b 200m",
                                                                                           "5b 200m",
                                                                                           "3b 400m",
                                                                                           "4b 400m", 
                                                                                           "5b 400m",
                                                                                           "3b 4x100m",
                                                                                           "3b 4x400m"])
    with t_100_3b:
        st.subheader("3 Ball 100m")
        st.write(pd.read_csv('data/ranking_M_3b_100m.csv'))
    with t_100_4b:
        st.subheader("4 Ball 100m")
        st.write(pd.read_csv('data/ranking_M_4b_100m.csv'))
    with t_100_5b:
        st.subheader("5 Ball 100m")
        st.write(pd.read_csv('data/ranking_M_5b_100m.csv'))
    with t_100_7b:
        st.subheader("7 Ball 100m")
        st.write(pd.read_csv('data/ranking_M_7b_100m.csv'))
    with t_200_3b:
        st.subheader("3 Ball 200m")
        st.write(pd.read_csv('data/ranking_M_3b_200m.csv'))
    with t_200_4b:
        st.subheader("4 Ball 200m")
        st.write(pd.read_csv('data/ranking_M_4b_200m.csv'))
    with t_200_5b:
        st.subheader("5 Ball 200m")
        st.write(pd.read_csv('data/ranking_M_5b_200m.csv'))
    with t_400_3b:
        st.subheader("3 Ball 400m")
        st.write(pd.read_csv('data/ranking_M_3b_400m.csv'))
    with t_400_4b:
        st.subheader("4 Ball 400m")
        st.write(pd.read_csv('data/ranking_M_4b_400m.csv'))
    with t_400_5b:
        st.subheader("5 Ball 400m")
        st.write(pd.read_csv('data/ranking_M_5b_400m.csv'))
    with t_4x100_3b:
        st.subheader("3 Ball 4 x 100m Relay")
        st.write(pd.read_csv('data/ranking_M_3b_4x100m.csv'))
    with t_4x400_3b:
        st.subheader("3 Ball 4 x 400m Relay")
        st.write(pd.read_csv('data/ranking_M_3b_4x400m.csv'))
    