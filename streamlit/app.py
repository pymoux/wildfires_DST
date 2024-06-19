#main.py
import streamlit as st
from tabs import introduction, wildfires_data, weather_data, us_forests, modeling, conclusion
from data_processing import process_data
from data_visualization import visualize_data
import base64

TABS = {
    introduction.sidebar_name: introduction,
    wildfires_data.sidebar_name: wildfires_data,
    weather_data.sidebar_name: weather_data,
    us_forests.sidebar_name: us_forests,
    modeling.sidebar_name: modeling,
    conclusion.sidebar_name: conclusion
}

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def run():
    
    st.set_page_config(page_title="DataScientest, DA-NOV",
                       layout="wide", # PREFERONS-NOUS UNE DISPOSITION LARGE OU PLUS ETROITE ET CENTREE ???
                       initial_sidebar_state="expanded",
                       )
    
    st.sidebar.image("assets/wildfire.png", use_column_width=True)
    # st.sidebar.image("/mount/src/wildfires_dst/streamlit/assets/wildfire.png",use_column_width=True,)
    
    tab_selection = st.sidebar.radio("", list(TABS.keys()), 0)

    tab = TABS[tab_selection]
    tab.run()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Promotion Continue Data Analyst - Novembre 2023")
    
    linkedin_icon_base64 = get_base64_image("assets/linkedin.png")
    
    st.sidebar.markdown(
        f"""
        #### Joan VIVION <a href="https://www.linkedin.com/in/joan-vivion/" target="_blank"><img src="data:image/png;base64,{linkedin_icon_base64}" width="30" style="margin-left: 10px;"></a>
        #### Michaël DREXLER <a href="https://www.linkedin.com/in/drexlermichael/" target="_blank"><img src="data:image/png;base64,{linkedin_icon_base64}" width="30" style="margin-left: 10px;"></a>
        #### Xavier LOUIS <a href="https://www.linkedin.com/in/xavier-louis/" target="_blank"><img src="data:image/png;base64,{linkedin_icon_base64}" width="30" style="margin-left: 10px;"></a>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()
