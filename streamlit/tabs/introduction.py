# introduction.py
import streamlit as st

title = "Feux de Forêt"
sidebar_name = "Introduction"


def run():

    st.title(title)
    st.markdown("---")
    st.header("Exploitation des données des feux de forêts aux Etats-Unis entre 1992 et 2015")

    # Context
    st.subheader("Contexte DataScientest")
    st.markdown(
        """
        *Illud tamen te esse admonitum volo*, primum ut qualis es talem te esse omnes existiment ut, quantum a rerum turpitudine abes,
        tantum te a verborum libertate seiungas; deinde ut ea in alterum ne dicas, quae cum tibi falso responsa sint, erubescas.
        
        **Quis est enim, cui via ista non pateat**, qui isti aetati atque etiam isti dignitati non possit quam velit petulanter, etiamsi
        sine ulla suspicione, at non sine argumento male dicere? Sed istarum partium culpa est eorum, qui te agere voluerunt; laus pudoris
        tui, quod ea te invitum dicere videbamus, ingenii, quod ornate politeque dixisti.
        """
        )
    
    # Objectives
    st.subheader("Objectifs DataScientest")
    st.markdown(
        """
        ***Illud tamen te esse admonitum volo***, primum ut qualis es talem te esse omnes existiment ut, quantum a rerum turpitudine abes,
        tantum te a verborum libertate seiungas; deinde ut ea in alterum ne dicas, quae cum tibi falso responsa sint, erubescas.
        
        ****Quis est enim, cui via ista non pateat****, qui isti aetati atque etiam isti dignitati non possit quam velit petulanter, etiamsi
        sine ulla suspicione, at non sine argumento male dicere? Sed istarum partium culpa est eorum, qui te agere voluerunt; laus pudoris
        tui, quod ea te invitum dicere videbamus, ingenii, quod ornate politeque dixisti.
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
