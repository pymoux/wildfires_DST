# widfires_data.py
import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px

# POSSIBILITE DE FAIRE 2 SOUS-PARTIES POUR SEPARER intro/contexte/source DE l'exploration/viz

title = "Les feux de forêt aux Etats-Unis entre 1992 et 2015"
sidebar_name = "Données de feux de forêt"


def run():

    st.title(title)
    st.markdown("---")
    
    # Contexte
    st.header("Contexte des données")
    st.markdown(
        """
        *Illud tamen te esse admonitum volo*, primum ut qualis es talem te esse omnes existiment ut, quantum a rerum turpitudine abes,
        tantum te a verborum libertate seiungas; deinde ut ea in alterum ne dicas, quae cum tibi falso responsa sint, erubescas.
        
        **Quis est enim, cui via ista non pateat**, qui isti aetati atque etiam isti dignitati non possit quam velit petulanter, etiamsi
        sine ulla suspicione, at non sine argumento male dicere? Sed istarum partium culpa est eorum, qui te agere voluerunt; laus pudoris
        tui, quod ea te invitum dicere videbamus, ingenii, quod ornate politeque dixisti.
        """
        )
    
    # Source
    st.header("Source des données")
    st.markdown(
        """
        *Illud tamen te esse admonitum volo*, primum ut qualis es talem te esse omnes existiment ut, quantum a rerum turpitudine abes,
        tantum te a verborum libertate seiungas; deinde ut ea in alterum ne dicas, quae cum tibi falso responsa sint, erubescas.
        
        **Quis est enim, cui via ista non pateat**, qui isti aetati atque etiam isti dignitati non possit quam velit petulanter, etiamsi
        sine ulla suspicione, at non sine argumento male dicere? Sed istarum partium culpa est eorum, qui te agere voluerunt; laus pudoris
        tui, quod ea te invitum dicere videbamus, ingenii, quod ornate politeque dixisti.
        """
        )
    
    # Exploration
    st.header("Exploration des données")
    st.markdown(
        """
        *Illud tamen te esse admonitum volo*, primum ut qualis es talem te esse omnes existiment ut, quantum a rerum turpitudine abes,
        tantum te a verborum libertate seiungas; deinde ut ea in alterum ne dicas, quae cum tibi falso responsa sint, erubescas.
        
        **Quis est enim, cui via ista non pateat**, qui isti aetati atque etiam isti dignitati non possit quam velit petulanter, etiamsi
        sine ulla suspicione, at non sine argumento male dicere? Sed istarum partium culpa est eorum, qui te agere voluerunt; laus pudoris
        tui, quod ea te invitum dicere videbamus, ingenii, quod ornate politeque dixisti.
        """
        )