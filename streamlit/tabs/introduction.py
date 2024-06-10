# introduction.py
import streamlit as st

title = "Feux de Forêt"
sidebar_name = "Introduction"


def run():

    st.title(title)
    st.markdown("---")
    st.header("Exploitation des données des feux de forêts aux Etats-Unis entre 1992 et 2015")

    # Context
    st.subheader("Contexte")
    st.markdown(
        """
        Les feux de forêt sont souvent un élément naturel et indispensable à l'équilibre des écosystèmes, mais leur combinaison avec le changement climatique, la sécheresse, les modifications des régimes d'incendie et l'urbanisation peut les rendre destructeurs et coûteux. Ces dernières décennies, les incendies aux États-Unis ont pris de l'ampleur, tant en taille, en coût qu’en complexité, survenant désormais tout au long de l'année. Le changement climatique aggrave cette tendance, provoquant des feux plus fréquents et intenses, qui à leur tour émettent des émissions de carbone, alimentant ainsi davantage le changement climatique.
        
        Les effets dévastateurs des graves incendies de forêt sont devenus bien réels pour les communautés et les pompiers forestiers de tout le pays. En 2023, le National Interagency Fire Center a enregistré 68 988 incendies aux États-Unis, dévastant 7,5 millions d'acres, des chiffres dépassant la moyenne décennale.
        
        Conscient de l'urgence de la situation, le budget du président Biden pour 2024 propose une augmentation financière substantielle dépassant les 4.3 milliards de dollars répartis entre le Département de l’Intérieur (DOI) pour un montant de 1.33 milliards (soit 233 millions de dollars ou 21% supplémentaires par rapport à 2023) et le Département de l’Agriculture (USDA) qui s’élève à 2.97 milliards de dollars (soit 647 millions de dollars ou 28% supplémentaire par rapport à 2023).
        
        Bien que ces augmentations soient principalement dédiés à réformer la rémunération de la main d’oeuvre, les demandes budgétaires prévoit également des augmentations significatives pour les moyens de préparation aux incendies incluant entre autres le traitement proactifs des surfaces à risque, le financement de systèmes aériens ou encore le développement d’intelligence artificielle et l’automatisation pour identifier les domaines clés permettant de réduire les besoins en personnel et risques pour les pompiers forestiers.

        """
        )
    
    # Objectives
    st.subheader("Objectifs")
    st.markdown(
        """
        Dans le cadre de notre formation de Data Analyst, ce projet d'analyse vise à examiner en profondeur les données de plusieurs millions d'incendies de forêt enregistrés aux États-Unis sur la période 1992-2015. En utilisant les outils et méthodes enseignés, notre objectif en tant que non-experts dans le domaine des incendies sera d'identifier les facteurs clés responsables des incendies majeurs et de prédire leurs répercussions.
        
        À cet effet, nous étudierons attentivement les données des feux de forêt et nous les croiserons avec d'autres variables telles que les données météo, la densité de population, et les localisations des stations de pompiers. Cette approche nous permettra de déterminer les tendances et les modèles qui pourraient prévoir l'émergence et la propagation des incendies de forêt. 
        
        En analysant ces données à travers des techniques avancées d'apprentissage automatique et de modélisation statistique, nous chercherons à développer des outils prédictifs précis pour aider les autorités locales et les organismes de lutte contre les incendies à anticiper et à répondre efficacement aux futurs événements.

        """
        )
    
    # Classification
    st.subheader("Classification du problème") 
    st.markdown(
        """
        Ces questions de recherche nous amèneront à utiliser la plupart des compétences acquises au cours de notre formation :

        1. Grâce aux outils de **Data Analyse** et de **Dataviz**, nous allons **acquérir, explorer, nettoyer, fusionner, visualiser et 
            analyser** nos données.
        2. Les **tests statistiques**, ainsi que les **régressions linéaire et polynomiale**, évaluées par des métriques de performance,
            nous permettront d'**établir** et d'**analyser ces degrés de corrélations**.
        3. Grâce au **machine learning**, nous construirons un **modèle prédictif d’évolution des températures**.
        
        Enfin, c’est par un **travail de recherche** que nous nous assurerons de **l’adéquation de nos résultats avec ceux des
        études courantes**. 
        """
        )
