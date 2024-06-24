# introduction.py
import streamlit as st

title = "Projet Feux de Forêt"
sidebar_name = "Introduction"

def run():
    st.title(title)
    st.markdown("---")
    
    # Contenu de l'introduction avec des icônes
    introduction_text = """
    <!-- Lien CDN pour Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

    <style>
    .icon {
        font-size: 24px;
        margin-right: 10px;
        color: #4CAF50; /* Couleur verte */
    }
    </style>

    <h2>Exploitation des données des feux de forêts aux États-Unis entre 1992 et 2015</h2>

    <h3><i class="fas fa-info-circle icon"></i> Contexte</h3>
    <p>
        Les feux de forêt sont souvent un élément naturel et indispensable à l'équilibre des écosystèmes, mais leur combinaison avec le changement climatique, la sécheresse, les modifications des régimes d'incendie et l'urbanisation peut les rendre destructeurs et coûteux. Ces dernières décennies, les incendies aux États-Unis ont pris de l'ampleur, tant en taille, en coût qu’en complexité, survenant désormais tout au long de l'année. Le changement climatique aggrave cette tendance, provoquant des feux plus fréquents et intenses, qui à leur tour émettent des émissions de carbone, alimentant ainsi davantage le changement climatique.
    </p>
    <p>
        Les effets dévastateurs des graves incendies de forêt sont devenus bien réels pour les communautés et les pompiers forestiers de tout le pays. En 2023, le National Interagency Fire Center a enregistré 68 988 incendies aux États-Unis, dévastant 7,5 millions d'acres, des chiffres dépassant la moyenne décennale.
    </p>
    <p>
        Conscient de l'urgence de la situation, le budget du président Biden pour 2024 propose une augmentation financière substantielle dépassant les 4.3 milliards de dollars répartis entre le Département de l’Intérieur (DOI) pour un montant de 1.33 milliards (soit 233 millions de dollars ou 21% supplémentaires par rapport à 2023) et le Département de l’Agriculture (USDA) qui s’élève à 2.97 milliards de dollars (soit 647 millions de dollars ou 28% supplémentaire par rapport à 2023).
    </p>

    <h3><i class="fas fa-bullseye icon"></i> Objectifs</h3>
    <p>
        Dans le cadre de notre formation de Data Analyst, ce projet d'analyse vise à examiner en profondeur les données de plusieurs millions d'incendies de forêt enregistrés aux États-Unis sur la période 1992-2015. En utilisant les outils et méthodes enseignés, notre objectif en tant que non-experts dans le domaine des incendies sera d'identifier les facteurs clés responsables des incendies majeurs et de prédire leurs répercussions.
    </p>
    <p>
        À cet effet, nous étudierons attentivement les données des feux de forêt et nous les croiserons avec d'autres variables telles que les données météo, la densité de population, et les localisations des stations de pompiers. Cette approche nous permettra de déterminer les tendances et les modèles qui pourraient prévoir l'émergence et la propagation des incendies de forêt.
    </p>
    <p>
        En analysant ces données à travers des techniques avancées d'apprentissage automatique et de modélisation statistique, nous chercherons à développer des outils prédictifs précis pour aider les autorités locales et les organismes de lutte contre les incendies à anticiper et à répondre efficacement aux futurs événements.
    </p>

    <h3><i class="fas fa-tasks icon"></i> Classification du Problème</h3>
    <p>
        Ces questions de recherche nous amèneront à utiliser la plupart des compétences acquises au cours de notre formation :
    </p>
    <ul>
        <li>Grâce aux outils de <strong>Data Analyse</strong> et de <strong>Dataviz</strong>, nous allons <strong>acquérir, explorer, nettoyer, fusionner, visualiser et analyser</strong> nos données.</li>
        <li>Les <strong>tests statistiques</strong>, ainsi que les <strong>régressions linéaires et polynomiales</strong>, évaluées par des métriques de performance, nous permettront d'<strong>établir</strong> et d'<strong>analyser ces degrés de corrélations</strong>.</li>
        <li>Grâce au <strong>machine learning</strong>, nous construirons un <strong>modèle prédictif d’évolution des températures</strong>.</li>
    </ul>
    <p>
        Enfin, c’est par un <strong>travail de recherche</strong> que nous nous assurerons de <strong>l’adéquation de nos résultats avec ceux des études courantes</strong>.
    </
        </ul>
    """

    # Afficher le texte formaté
    st.markdown(introduction_text, unsafe_allow_html=True)
