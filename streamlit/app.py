# main.py
import streamlit as st
from tabs import introduction, wildfires_data, weather_data, us_forests, modeling, conclusion
from data_loading import load_df
from data_processing import process_data
from data_visualization import visualize_data


TABS = {
    introduction.sidebar_name: introduction,
    wildfires_data.sidebar_name: wildfires_data,
    weather_data.sidebar_name: weather_data,
    us_forests.sidebar_name: us_forests,
    modeling.sidebar_name: modeling,
    conclusion.sidebar_name: conclusion
}


def run():
    
    st.set_page_config(page_title="DataScientest, DA-NOV",
                       layout="wide", # PREFERONS-NOUS UNE DISPOSITION LARGE OU PLUS ETROITE ET CENTREE ???
                       initial_sidebar_state="expanded",
                       )
    
    st.sidebar.image("assets/wildfire.png",use_column_width=True,)
    #st.sidebar.image("/mount/src/wildfires_dst/streamlit/assets/wildfire.png",use_column_width=True,)
    
    tab_selection = st.sidebar.radio("", list(TABS.keys()), 0)

    tab = TABS[tab_selection]
    tab.run()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Promotion Continue Data Analyst - Novembre 2023")
    st.sidebar.markdown(
        "#### Joan VIVION\n"
        "#### Michaël DREXLER\n"
        "#### Xavier LOUIS"
    )

if __name__ == "__main__":
    run()