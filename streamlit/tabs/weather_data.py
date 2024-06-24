# weather_data.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import os
import gdown

 
title = "Les données météo aux Etats-Unis entre 1992 et 2015"
sidebar_name = "Données météorologiques"

# load datafile from Google drive
st.cache_data()
data_dir = r'data'
os.makedirs(data_dir, exist_ok=True)
file_id = "1jFHa9crQOSGYLrjy22UzCQ5_sEX5drVX"
destination = os.path.join(data_dir, "weather_data-state-june24.csv.gz")

# Télécharger le fichier depuis Google Drive s'il n'existe pas déjà
url="https://drive.google.com/file/d/1Zh3diZn8ycX46zW-xLHrkp4cBZajxO1E/view?usp=share_link"
if not os.path.exists(destination):
    #gdown.download(f"https://drive.google.com/drive/u/0/folders/{file_id}", destination, quiet=False)
    gdown.download(url, destination, quiet=False)


def run():
 
    st.title(title)
    st.markdown("---")
 
    # Contexte
    st.header("Contexte des données météorologiques")
    st.markdown(
        """
        Les données météorologiques sont des données clés pour l'analyse de riques des feux de forêt : températures, précipitations, vent ou impacts de foudre.
        """
        )
   
    # Tabs for different dimensions
    dimension_tabs = st.tabs(["Températures et précipitations", "Impacts de foudre"])
 
    with dimension_tabs[0]:
        st.header("Températures et précipitations")
 
        # Source
        st.subheader("Source")
        st.markdown(
            """
            Les données de températures et de précipitations (entre autres) ont été téléchargées à partir du site de la NOAA (National Oceanic and Atmospheric Administration) :
            - https://www.ncdc.noaa.gov/cdo-web/datasets\n
            Plus précisément, il s'agit des données journalières issues du Global Historical Climatology Network et regroupées par année disponibles à cette adresse :
            - https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/\n
            La liste des 126 000 stations météorologiques du réseau a été parallèlement téléchargée au même endroit puis nettoyée.
            """
            )
   
        # Exploration
        st.subheader("Exploration")
        st.markdown(
            """
            Les données brutes ont tout d'abord été filtrées sur les plus de 72 000 stations météorologiques américaines et portoricaines.\n
            Les données quotidiennes de températures (TMIN, TAVG, TMAX) et de précipitations (PRCP) ont été extraites.
            Ces différentes manipulations ont nécessité des ressources importantes afin d'obtenir le jeu de données final.
            """
            )
                
        df_w = pd.read_csv(destination, compression='gzip', sep=",", index_col=0)
        df_w['date'] = pd.to_datetime(df_w['date'], format='%Y%m%d')
        df_w['year'] = df_w['date'].dt.year
        df_w['month'] = df_w['date'].dt.month
        df_w['season'] = df_w['month'] % 12 // 3 + 1

        df_yearstate = df_w.groupby(by=['year', 'state'], as_index=False).agg({'TMAX_mean':'mean', 'PRCP_mean':'sum'})
        df_yearstate[df_yearstate['state']=='DC']
        
        states = sorted(df_yearstate['state'].unique())
        states_abb = {"Alaska":"AK", "Alabama":"AL", "Arkansas":"AR", "Arizona":"AZ", "California":"CA",
                      "Colorado":"CO", "Connecticut":"CT", "District of Columbia":"DC", "Delaware":"DE",
                      "Florida":"FL", "Georgia":"GA", "Hawaii":"HI", "Iowa":"IA", "Idaho":"ID", "Illinois":"IL",
                      "Indiana":"IN", "Kansas":"KS", "Kentucky":"KY", "Louisiana":"LA", "Massachusetts":"MA",
                      "Maryland":"MD", "Maine":"ME", "Michigan":"MI", "Minnesota":"MN", "Missouri":"MO",
                      "Mississippi":"MS", "Montana":"MT", "North Carolina":"NC", "North Dakota":"ND",
                      "Nebraska":"NE", "New Hampshire":"NH", "New Jersey":"NJ", "New Mexico":"NM", "Nevada":"NV",
                      "New York":"NY", "Ohio":"OH", "Oklahoma":"OK", "Oregon":"OR", "Pennsylvania":"PA",
                      "Puerto Rico":"PR", "Rhode Island":"RI", "South Carolina":"SC", "South Dakota":"SD",
                      "Tennessee":"TN", "Texas":"TX", "Utah":"UT", "Virginia":"VA", "Vermont":"VT", "Washington":"WA",
                      "Wisconsin":"WI", "West Virginia":"WV", "Wyoming":"WY"}


        # choropleths figures
        fig_t1 = px.choropleth(df_yearstate,
                               locations='state',
                               locationmode="USA-states",
                               color="TMAX_mean",
                               scope="usa",
                               color_continuous_scale="YlOrRd",
                               range_color=[df_yearstate['TMAX_mean'].min(),df_yearstate['TMAX_mean'].max()],
                               animation_frame='year',
                              )
        fig_t1.update_layout(title={'text':f'<b>Température moyenne par état entre 1992 et 2015</b>',
                                    'font': {'size': 18},
                                    'x':0.5,
                                    'xanchor': 'center'},
                             coloraxis_showscale=False,
                             height=600,
                            )
        
        fig_p1 = px.scatter_geo(df_yearstate,
                                locations='state',
                                scope="usa",
                                locationmode="USA-states",
                                size='PRCP_mean',
                                size_max=20,
                                animation_frame="year",
                               )

        fig_t1.add_trace(fig_p1.data[0])
        for i, frame in enumerate(fig_t1.frames):
            fig_t1.frames[i].data += (fig_p1.frames[i].data[0],)
        st.plotly_chart(fig_t1)
        
        # bar charts
        selection_state = st.selectbox('', options=list(states_abb.keys()), index=9)
        selected_state = states_abb[selection_state]
        
        fig_t2 = px.bar(df_yearstate.loc[df_yearstate['state']==selected_state],
                        x='year',
                        y='TMAX_mean',
                        color='TMAX_mean',
                        range_color=[df_yearstate['TMAX_mean'].min(),df_yearstate['TMAX_mean'].max()],
                        color_continuous_scale="YlOrRd",
                       )
        fig_t2.update_layout(title={'text': f'<b>Température max moyenne par année ({selected_state})</b>',
                                    'font':{'size':18},
                                    'x':0.5,
                                    'xanchor': 'center'},
                             coloraxis=dict(colorbar_x=0.96, 
                                            colorbar_y=0.5, 
                                            colorbar_len=0.5, 
                                            colorbar_thickness=10,
                                            colorbar_title=None),
                             xaxis_title='',
                             yaxis_title='Temp. max moyenne (°C)',
                             #height=400,
                             #width=600
                            )
        
        fig_p2 = px.bar(df_yearstate.loc[df_yearstate['state']==selected_state],
                        x='year',
                        y='PRCP_mean',
                        color='PRCP_mean',
                        range_color=[df_yearstate['PRCP_mean'].min(),df_yearstate['PRCP_mean'].max()],
                        color_continuous_scale="Blues",
                       )
        fig_p2.update_layout(title={'text': f'<b>Précipitations cumulées par année ({selected_state})</b>',
                                    'font':{'size':18},
                                    'x':0.5,
                                    'xanchor': 'center'},
                             coloraxis=dict(colorbar_x=0.96, 
                                            colorbar_y=0.5, 
                                            colorbar_len=0.5, 
                                            colorbar_thickness=10,
                                            colorbar_title=None),
                             xaxis_title='',
                             yaxis_title='Précip. cumulées (mm)',
                             #height=400,
                             #width=600
                            )
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(fig_t2, use_container_width=True)
        with col4:
            st.plotly_chart(fig_p2, use_container_width=True)

    with dimension_tabs[1]:
        st.header("Impacts de foudre")

        # Source
        st.subheader("Source")
        st.markdown(
            """
            La base de données [Severe Weather Data Inventory (SWDI)](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00773) de la NOAA (National Oceanic and Atmospheric Administration) regroupe les phénomènes météorologiques extrêmes aux Etats-Unis : orages, foudre, grêle, tornade.\n
            Les données relatives aux impacts de foudre récoltées par le [Vaisala National Lightning Detection Network](https://www.vaisala.com/en/products/national-lightning-detection-network-nldn) depuis 1986 ont été téléchargées à l'adresse suivante :
            - https://www.ncei.noaa.gov/pub/data/swdi/database-csv/v2/
            """
            )

        # Exploration
        st.subheader("Exploration")
        st.markdown(
            """
            Les données brutes sont composée de 3 éléments : date, localisation d'un point central (latitude et longitude) et nombre d'impacts.\n
            Dans un premier temps, ces données ont simplement été colocalisées avec les états américains pour leur exploration.
            Tout comme pour les données météo, la manipulation de ce jeu de données de plus de 70 millions d'enregistrements demande des ressources importantes.
            """
            )
