# us_forests.py
import streamlit as st
import pandas as pd
import gdown
import os

title = "Le US Forest Service et les forêts nationales"
sidebar_name = "USFS et les forêts nationales"


def run():

    st.title(title)
    st.markdown("---")

    # Définir les fonctions avant de les utiliser dans le dictionnaire SUBTABS
    def usfs():
        st.header("Présentation de l'US Forest Service")

        # Texte à gauche, image à droite
        col1, col2 = st.columns([1, 1])

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
        "Forêt nationale de Coconino": "L'une des forêts nationales les plus diversifiées du pays, avec des paysages et des activités changeants à chaque coin de rue. Explorez les montagnes et les canyons, pêchez dans les petits lacs et pataugez dans les ruisseaux et les ruisseaux tranquilles.",
        "Forêt nationale de Deschutes": "La forêt nationale de Deschutes s'étend sur près de 1,6 million d'acres et offre des possibilités de loisirs toute l'année.",
        "Forêt nationale d'Ouachita": "Située en Arkansas et en Oklahoma, la forêt nationale d'Ouachita abrite des collines, des lacs immaculés, des merveilles géologiques et une vaste gamme d'aventures à chaque tournant !",
        "Forêt nationale de Chattahoochee-Oconee": "La forêt nationale de Chattahoochee-Oconee offre les meilleures possibilités de loisirs de plein air et les meilleures ressources naturelles de Géorgie. Comprenant près de 867 000 acres répartis dans 26 comtés, des milliers de kilomètres de ruisseaux et de rivières aux eaux claires, environ 850 milles de sentiers récréatifs et des dizaines de terrains de camping, d'aires de pique-nique et d'autres possibilités d'activités récréatives, ces terres sont riches en paysages naturels, en histoire et en culture.",
        "Forêt nationale de Lolo": "La forêt nationale de Lolo est une destination idéale pour les habitants et les visiteurs qui souhaitent jouer. Il y a tellement de choses à explorer avec des opportunités telles que la randonnée, l'équitation en VHR, le camping, la location de chalets et de tours d'observation, les sports d'hiver et deux centres d'accueil.",
        "Forêt nationale de San Bernardino": "À seulement quelques kilomètres de l'Inland Empire, du Haut Désert et de la vallée de Coachella, nous sommes situés à la fois à San Bernardino et dans le comté de Riverside. Faites de la randonnée, du vélo, du camping, de la raquette, conduisez votre VHR ou découvrez les ruisseaux, les ruisseaux et les cascades."
        }

        # Sélection de la forêt dans la liste déroulante
        selected_forest = st.selectbox("Sélectionnez une forêt nationale", list(forests.keys()))

        # Affichage de la description de la forêt sélectionnée
        st.write(f"**{selected_forest}** : {forests[selected_forest]}")

    SUBTABS = {
        "US Forest Service": usfs,
        "Les forêts": nat_forests,
    }

    selection = st.sidebar.radio("", list(SUBTABS.keys()), 0)

    subtab = SUBTABS[selection]
    subtab()

    # Chemin vers le dossier où vous souhaitez télécharger et enregistrer les données
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    # Charger les données une seule fois au chargement de l'application
    @st.cache
    def load_data():
        # URL du fichier Google Drive
        file_id = '1IsYymZWjWAJDKvLaXHIDcSnrfjQvHNdj'
        destination = os.path.join(data_dir, 'preprocessed_data.csv')

        # Télécharger le fichier depuis Google Drive s'il n'existe pas déjà
        if not os.path.exists(destination):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", destination, quiet=False)

        # Charger les données
        gdf_forests = pd.read_csv(destination)
        return gdf_forests


if __name__ == "__main__":
    run()
