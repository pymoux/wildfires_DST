# conclusion.py
import streamlit as st

# Définir le titre et le nom de la barre latérale
title = "Conclusion"
sidebar_name = "Conclusion"

def run():
    # Afficher le titre principal
    st.title(title)

    # Contenu de la conclusion avec des icônes
    conclusion_text = """
    <!-- Lien CDN pour Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

    <style>
    .icon {
        font-size: 24px;
        margin-right: 10px;
        color: #4CAF50;
    }
    </style>

    <h2><i class="fas fa-project-diagram icon"></i> Résumé du Projet</h2>
    <p>
        Ce projet de données autour des feux de forêt a permis de développer une compréhension approfondie des dynamiques et des facteurs influençant ces incidents, en manipulant diverses sources de données.
    </p>

    <h2><i class="fas fa-database icon"></i> Exploration des Données</h2>
    <p>
        La phase d’exploration des jeux de données a révélé la richesse et la complexité des informations disponibles, allant des données météorologiques aux caractéristiques géographiques et aux historiques d'incendies. La transformation et la préparation des données ont été des étapes cruciales pour garantir la qualité et la pertinence des analyses suivantes.
    </p>
    <p>
        La dimension temporelle a permis de mettre en évidence des tendances saisonnières et annuelles, tandis que la dimension spatiale a montré la répartition géographique des feux, révélant des zones particulièrement à risque.
    </p>

    <h2><i class="fas fa-chart-line icon"></i> Modélisation et Défis</h2>
    <p>
        La phase de modélisation a consisté en une série d'étapes allant du prétraitement et de l'ingénierie des caractéristiques à l'optimisation des modèles. Une des principales difficultés rencontrées a été le déséquilibre des classes dans les données, avec une forte prédominance de cas sans incendie par rapport aux cas d'incendies. Ce déséquilibre a impacté la performance initiale des modèles prédictifs, rendant difficile la détection précise des incendies.
    </p>
    <p>
        Pour remédier à cela, nous avons testé plusieurs techniques de rééquilibrage des données qui n’auront malheureusement pas suffi à obtenir des résultats satisfaisants. Ces difficultés de modélisation nous ont également orientés vers notre seconde problématique centrée sur les forêts nationales protégées de l'US Forest Service. En se concentrant sur cette sous-population spécifique, nous avons pu affiner notre approche et développer des modèles plus pertinents pour les contextes particuliers des forêts protégées.
    </p>
    <p>
        Cette approche a ajouté une couche supplémentaire de complexité et de spécificité au projet. Les résultats de cette partie ont montré des différences significatives dans les facteurs de risque en fonction des forêts et ont permis de développer des modèles adaptés aux contextes spécifiques des forêts protégées.
    </p>

    <h2><i class="fas fa-leaf icon"></i> Conclusion et Implications</h2>
    <p>
        En conclusion, ce projet a démontré l'importance de l'analyse de données dans la compréhension et la gestion des feux de forêt. Les outils et techniques employés ont permis de transformer des données brutes en insights exploitables, fournissant des bases solides pour des actions préventives et des interventions ciblées.
    </p>
    <p>
        À terme, les résultats obtenus peuvent servir de support à la prise de décision pour les autorités et les gestionnaires de forêt, contribuant ainsi à la préservation des écosystèmes forestiers et à la protection des communautés humaines.
    </p>
    """

    # Afficher le texte formaté
    st.markdown(conclusion_text, unsafe_allow_html=True)

# Exécuter la fonction
if __name__ == "__main__":
    run()