# modeling.py
import streamlit as st


title = "Modeling des incendies dans les forêts nationales"
sidebar_name = "Modeling"


def run():

    st.title(title)

    SUBPAGES = {
        "Le modèle": subpage1,
        "Prédiction": subpage2,
    }

    st.sidebar.title('Prédiction')
    selection = st.sidebar.radio("Aller à", list(SUBPAGES.keys()))

    subpage = SUBPAGES[selection]

    subpage()


def subpage1():
    st.header('Présentation du modèle')
    st.write('Bienvenue sur la sous-page 1.')


def subpage2():
    st.header('Prédiction')
    st.write('Bienvenue sur la sous-page 2.')

