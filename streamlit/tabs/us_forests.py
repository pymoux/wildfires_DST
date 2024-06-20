# us_forests.py
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import gdown
import os

title = "Le US Forest Service et les forêts nationales"
sidebar_name = "USFS et les forêts nationales"


def run():

    st.title(title)
    st.markdown("---")
    
    SUBTABS = {"US Forest Service": usfs,
           "Les forêts": nat_forests,
          }

    selection = st.sidebar.radio("", list(SUBTABS.keys()), 0)

    subtab = SUBTABS[selection]
    subtab()


def usfs():
    st.header("Présentation de l'US Forest Service")

    # Texte à gauche, image à droite
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            Le US Forest Service (USFS), une agence du département de l’agriculture américain, administre les 154 forêts nationales protégées des Etats-Unis. Ces forêts s’étendent sur près de 190 millions d’acres et sont réparties sur 43 états et Porto Rico. Elles sont désignées comme terres publiques à des fins de préservation, de récréation, de gestion durable des ressources naturelles et de protection de la biodiversité. Elles représentent à ce titre un héritage naturel précieux pour les générations présentes et futures et doivent être préservées, notamment des incendies. Selon l’analyse exploratoire du jeu de données initiales, l’USFS constitue le second organisme le plus impacté par les incendies de forêts en termes de superficie brûlées sur la période d’étude avec une tendance à la hausse au cours du temps. Nous avons donc pris le parti comme objectif de modéliser et de transmettre le risque d'incendie dans ces forêts nationales à l’US Forest Service afin de permettre une coordination adéquate des ressources pour lutter contre les incendies de forêts protégées.
            """
        )

    with col2:
        # Charger et afficher l'image avec une largeur personnalisée
        image_path = "assets/US_Forest.png"
        st.image(image_path, caption="Forêts Nationales des États-Unis", width=500)


def nat_forests():
    st.header('Les différentes forêts nationales')

    # Liste des forêts nationales et leurs descriptions
    forests = {
    "Coconino National Forest": "L'une des forêts nationales les plus diversifiées du pays, avec des paysages et des activités changeants à chaque coin de rue. Explorez les montagnes et les canyons, pêchez dans les petits lacs et pataugez dans les ruisseaux et les ruisseaux tranquilles.",
    "Deschutes National Forest": "La forêt nationale de Deschutes s'étend sur près de 1,6 million d'acres et offre des possibilités de loisirs toute l'année.",
    "Ouachita National Forest": "Située en Arkansas et en Oklahoma, la forêt nationale d'Ouachita abrite des collines, des lacs immaculés, des merveilles géologiques et une vaste gamme d'aventures à chaque tournant !",
    "Chattahoochee-Oconee National Forest": "La forêt nationale de Chattahoochee-Oconee offre les meilleures possibilités de loisirs de plein air et les meilleures ressources naturelles de Géorgie. Comprenant près de 867 000 acres répartis dans 26 comtés, des milliers de kilomètres de ruisseaux et de rivières aux eaux claires, environ 850 milles de sentiers récréatifs et des dizaines de terrains de camping, d'aires de pique-nique et d'autres possibilités d'activités récréatives, ces terres sont riches en paysages naturels, en histoire et en culture.",
    "Lolo National Forest": "La forêt nationale de Lolo est une destination idéale pour les habitants et les visiteurs qui souhaitent jouer. Il y a tellement de choses à explorer avec des opportunités telles que la randonnée, l'équitation en VHR, le camping, la location de chalets et de tours d'observation, les sports d'hiver et deux centres d'accueil.",
    "San Bernardino National Forest": "À seulement quelques kilomètres de l'Inland Empire, du Haut Désert et de la vallée de Coachella, nous sommes situés à la fois à San Bernardino et dans le comté de Riverside. Faites de la randonnée, du vélo, du camping, de la raquette, conduisez votre VHR ou découvrez les ruisseaux, les ruisseaux et les cascades."
    }
    
    forests_of_interest = ["Chattahoochee National Forest",
                           "Coconino National Forest",
                           "Deschutes National Forest",
                           "Lolo National Forest",
                           "Oconee National Forest",
                           "Ouachita National Forest",
                           "San Bernardino National Forest",
                          ]
    
    
    # Load datasets
    @st.cache_data
    def load_data(path1, path2, path3):
        df = pd.read_csv(path1,
                         sep='\t',
                         header=None,
                         names=['id_station', 'lat', 'long', 'unk', 'state'],
                        )
        df.drop(columns=['unk'], inplace=True)
        gdf1 = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.long, df.lat), crs="EPSG:4269")
        
        gdf2 = gpd.read_file(path2)
        gdf3 = gpd.read_file(path3)
        
        joined_gdf = gpd.sjoin(gdf1, gdf3[['PROCLAIMED', 'geometry']], how='left')
        filt_joined_gdf = joined_gdf.loc[joined_gdf['PROCLAIMED'].notnull()].drop('index_right', axis=1)
        
        return gdf2, gdf3, joined_gdf
        
    gdf_forest, gdf_forest_ext, joined_gdf_ext = load_data('data/ghcnd-stations_cleaned.tsv',
                                                           'data/forests_shape/S_USA.ProclaimedForest.shp',
                                                           'data/forests_extended_shape_5km/us_forests_ext_d5.shp')
    
    
    def forest_plotting(forest):
        # forests polygone
        polygon_ori = gdf_forest.loc[gdf_forest['FORESTNAME']==forest, 'geometry']
        polygon_ext = gdf_forest_ext.loc[gdf_forest_ext['FORESTNAME']==forest, 'geometry']
        polygons = pd.concat([polygon_ext, polygon_ori])
 
        # stations point
        proc = gdf_forest.loc[gdf_forest['FORESTNAME']==forest, 'PROCLAIMED'].to_string(index=False)
        stations = joined_gdf_ext.loc[joined_gdf_ext['PROCLAIMED']==proc, 'geometry']
        
        # plotting
        base = polygons.plot(figsize=(10,10), color=['greenyellow', 'green'])
        cx.add_basemap(base, crs="EPSG:4269")
        stations.plot(ax=base, marker='x', color='black', markersize=50)
        plt.title(forest)
        plt.axis('off')
        st.pyplot(plt)
   
    st.markdown(
        """
        Le US Forest Service gère 154 Forêts Nationales. Parfois administrativement regroupées pour la gestion, ces forêts sont ici considérées individuellement.\n
        Les données relatives aux Forêts Nationales ont été récoltées à partir de plusieurs sources mais les aires géographiques (shapes) ont été téléchargées à partir du site dédié de l'[US Department of Agriculture](https://data.fs.usda.gov/geodata/edw/datasets.php). Le jeu de données utilisé est le [**Original Proclaimed National Forests**](https://data.fs.usda.gov/geodata/edw/edw_resources/shp/S_USA.ProclaimedForest.zip).\n
        L'aire stricte de chaque forêt a été étendue de 5 km pour l'identification des stations météorologiques correspondantes.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        # Sélection de la forêt dans la liste déroulante
        #selected_forest = st.selectbox("Sélectionnez une forêt nationale", forests_of_interest, index=1)
        selected_forest = st.selectbox("Sélectionnez une forêt nationale", gdf_forest['FORESTNAME'], index=26)
        
        # Affichage de la description de la forêt sélectionnée
        st.markdown(f"**{selected_forest}**")
        st.markdown(f"{forests[selected_forest]}")
    
    with col2:
        forest_plotting(selected_forest)

        
if __name__ == "__main__":
    run()
