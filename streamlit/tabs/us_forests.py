# us_forests.py
import streamlit as st
from data_loading import load_df


title = "Le US Forest Service et les forêts nationales"
sidebar_name = "USFS et les forêts nationales"


def run():

    st.title(title)
    st.markdown("---")

    SUBTABS = {
        "US Forest Service": usfs,
        "Les forêts": nat_forests,
    }

    #st.sidebar.title('US Forest Service')
    selection = st.sidebar.radio("", list(SUBTABS.keys()), 0)

    subtab = SUBTABS[selection]
    subtab()

    gdf_forests = load_df("data/forests_shape/S_USA.ProclaimedForest.sbx")


def usfs():
    st.header("Présentation de l'US Forest Service")
    st.markdown(
        """
        Le Service des forêts des États-Unis (United States Forest Service, USFS) est une agence du département de l'Agriculture des États-Unis
        qui gère les forêts nationales du pays (United States National Forest).
        """
        )
    st.markdown("(Wikipedia)")


def nat_forests():
    st.header('Les différentes forêts nationales')

    # Créer un menu déroulant pour sélectionner la forêt
    visualization_type = st.selectbox('Forêt Nationale', ['Coconino', 'Tongass', 'White Mountain'])
    st.dataframe(gdf_forests)

    ## Charger les données
    #data = load_data("data.csv")

    ## Prétraiter les données
    #processed_data = process_data(data)

    ## Visualiser les données en fonction du type de visualisation choisi
    #if visualization_type == 'Histogramme':
    #    visualize_histogram(processed_data)
    #elif visualization_type == 'Diagramme à barres':
    #    visualize_bar_chart(processed_data)
    #elif visualization_type == 'Nuage de points':
    #    visualize_scatter_plot(processed_data)
