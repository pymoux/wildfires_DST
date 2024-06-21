import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import gdown
import os
import statsmodels.api
import statsmodels.formula.api as smf

title = "Les feux de forêt aux États-Unis entre 1992 et 2015"
sidebar_name = "Données de feux de forêt"

# Chemin vers le dossier où vous souhaitez télécharger et enregistrer les données
data_dir = r'data'
os.makedirs(data_dir, exist_ok=True)

# Charger les données une seule fois au chargement de l'application
@st.cache_data()
def load_data():
    # URL du fichier Google Drive
    file_id = '1LnR8--iqjqsk-B15Rcgf-Le4zuo3HqCn'
    destination = os.path.join(data_dir, 'wildfires15_db.csv')
    
    # Télécharger le fichier depuis Google Drive s'il n'existe pas déjà
    if not os.path.exists(destination):
        gdown.download(f"https://drive.google.com/uc?id={file_id}", destination, quiet=False)
    
    # Charger les données
    df = pd.read_csv(destination)
    
    return df

def run():
    # Inclure le lien CDN pour Font Awesome
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
        .icon {
            font-size: 24px;
            margin-right: 10px;
            color: #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title(title)
    st.markdown("---")
    
    # Contexte
    st.markdown(
        """
        <h2><i class="fas fa-info-circle icon"></i> Contexte des données</h2>
        <p>
        Pour notre étude, nous avons à disposition un jeu de données principal mis à disposition pour notre projet, celui-ci est disponible sur le site <a href="https://www.kaggle.com">Kaggle</a> :
        <strong>1.88 Million US Wildfires, 24 years of geo-referenced wildfire records</strong>.
        Ce jeu de données contient une base de données spatiales des incendies de forêt recensés aux États-Unis à partir de rapport d'organismes de lutte contre les incendies fédérales, étatiques et locales sur une période s'étalant de 1992 à 2015. Ces données ont été collectées grâce au financement du gouvernement américain et sont libres de tout droit pour utilisation.
        </p>
        """,
        unsafe_allow_html=True
    )
    
     # Source
    st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
    .icon {
        font-size: 24px;
        margin-right: 10px;
    }
    .icon-common { color: #FFA500; } /* Couleur orange */
    </style>
    <h2><i class="fas fa-database icon icon-common"></i> Source des données</h2>
    <p>
    Ce dataset contient globalement des données :
    <ul>
        <li><i class="fas fa-id-card icon icon-common"></i> <strong>d’identification</strong> selon différents référentiels ;</li>
        <li><i class="fas fa-clock icon icon-common"></i> <strong>temporelles</strong> concernant à la fois la découverte de l’incendie et sa maîtrise ;</li>
        <li><i class="fas fa-map-marker-alt icon icon-common"></i> <strong>géographiques</strong> avec les latitudes et longitudes ainsi que l’état et le comté de découverte ;</li>
        <li><i class="fas fa-ruler-combined icon icon-common"></i> <strong>relatives à la taille de l’incendie</strong> avec la surface en acres et la classe correspondante ;</li>
        <li><i class="fas fa-fire icon icon-common"></i> <strong>relatives à la cause identifiée de l’incendie</strong>, code et description.</li>
    </ul>
    </p>
    """,
    unsafe_allow_html=True
    )
    
    # Charger les données
    df = load_data()
    
    # Ajouter un volet pour afficher/masquer les données et les statistiques
    with st.expander("**Afficher/Masquer les données et les statistiques**"):
        # Afficher les premières lignes du dataset
        st.subheader("Aperçu des données")
        st.write(df.head())
        
        # Statistiques descriptives
        st.subheader("Statistiques descriptives")
        st.write(df.describe())
    
    # Tabs for different dimensions
    dimension_tabs = st.tabs(["Dimension temporelle", "Dimension spatiale", "Dimension cause des incendies"])
    
    with dimension_tabs[0]:
        st.header("Dimension temporelle")
        
        # Charger les données une seule fois au début
        df = load_data()

        # Préparer les données pour le premier graphique
        df['DISCO_DATE'] = pd.to_datetime(df['DISCO_DATE'])
        df['MONTH'] = df['DISCO_DATE'].dt.month
        fire_year_counts = df['FIRE_YEAR'].value_counts().sort_index()
        data = {'Year': fire_year_counts.index, 'Fires': fire_year_counts.values}
        df_plotly = pd.DataFrame(data)

        # Créer le premier graphique avec Plotly
        fig = px.bar(df_plotly,
                     x='Year',
                     y='Fires',
                     labels={'Fires': 'Nombre de feux'})

        # Ajouter une ligne de régression linéaire
        m, b = np.polyfit(df_plotly['Year'], df_plotly['Fires'], 1)
        fig.add_scatter(x=df_plotly['Year'], y=m*df_plotly['Year'] + b, mode='lines', name='Régression linéaire', line=dict(color='red', dash='dash'))

        # Utiliser une couleur unique pour toutes les barres (couleur évoquant la nature et le feu)
        custom_color = '#FF8C00'  # Un ton de beige pour le feu
        fig.update_traces(marker_color=custom_color)

        # Mettre en forme le titre en gras et le centrer
        fig.update_layout(title={'text':'<b>Distribution des feux de forêt au fil des années</b>',
                                 'font': {'size': 18},
                                 'x':0.5,
                                 'xanchor': 'center'},
                          legend={'font':{'size':11},
                                  'x':0.01,
                                  'xanchor':'left',
                                  'y':0.99,
                                  'yanchor':'top'},
                          height=400, width=600)

        # Afficher le premier graphique
        st.plotly_chart(fig)

        # Analyse du premier graphique
        st.markdown(
            """
            On constate une légère augmentation du nombre d’incendies à travers le temps grâce à la droite de régression linéaire. Il semble également y avoir un phénomène de vagues cycliques environ tous les 5 ans qui pourrait être en lien avec le phénomène climatique encore mal connu d’El Niño qui perturbe la façon dont l’air et l’humidité se déplacent dans le monde et qui peut avoir une incidence sur les précipitations et les températures à l’échelle planétaire.
            """
        )

        # Transition entre les graphiques
        st.markdown("---")
        st.markdown("Passons maintenant à l'analyse du nombre d'incendies par mois au fil des années.")

        # Création du dataframe pour le boxplot
        df_boxplot = df.groupby(['FIRE_YEAR', 'MONTH']).size().unstack(fill_value=0)

        # Tracer le boxplot avec Plotly
        fig_boxplot = px.box(df_boxplot, color_discrete_sequence=['#FF8C00'])
        fig_boxplot.update_traces(boxmean='sd')

        # Centrer le titre en gras
        fig_boxplot.update_layout(title={'text':'<b>Nombre d\'incendies par mois au fil des années</b>',
                                         'font': {'size': 18},
                                         'x':0.5,
                                         'xanchor':'center'},
                                  height=400, width=600)

        # Ajouter les étiquettes sur l'axe des x pour les mois
        fig_boxplot.update_xaxes(title='Mois', tickvals=list(range(1, 13)), ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])

        # Afficher le deuxième graphique
        st.plotly_chart(fig_boxplot)

        # Analyse du deuxième graphique
        st.markdown(
            """
            La distribution du nombre d’incendies au cours de l’année met effectivement en évidence une période propice aux feux de forêt allant de février à septembre avec 2 pics :
            - au printemps, la végétation du sous-bois morte en hiver sèche rapidement lors d’épisodes de redoux et favorise la propagation des incendies de forêt, notamment dans le sud du pays ;
            - en été, les conditions de sécheresse et la fréquentation accrue en forêt accentuent très fortement le risque d’éclosion des feux de forêt.
            """
        )

        # Transition vers le troisième graphique
        st.markdown("---")
        st.markdown("Analysons maintenant le nombre d'incendies par jour de la semaine au fil des années.")

        # Extraire le jour de la semaine (0 pour lundi, 1 pour mardi, ..., 6 pour dimanche)
        df['DAY_OF_WEEK'] = df['DISCO_DATE'].dt.dayofweek

        # Création du dataframe pour le boxplot
        df_boxplot2 = df.groupby(['FIRE_YEAR', 'DAY_OF_WEEK']).size().unstack(fill_value=0)

        # Tracer le boxplot avec Plotly
        fig_boxplot2 = px.box(df_boxplot2, color_discrete_sequence=['#FF8C00'])
        fig_boxplot2.update_traces(boxmean='sd')

        # Centrer le titre en gras
        fig_boxplot2.update_layout(title={'text':'<b>Nombre d\'incendies par jour de la semaine au fil des années</b>',
                                          'font':{'size':18},
                                          'x':0.5,
                                          'xanchor':'center'},
                                   height=400, width=600)

        # Ajouter les étiquettes sur l'axe des x pour les jours de la semaine
        fig_boxplot2.update_xaxes(title='Jour', tickvals=list(range(7)), ticktext=['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'])

        # Afficher le troisième graphique
        st.plotly_chart(fig_boxplot2)

        # Analyse du troisième graphique
        st.markdown(
            """
            On constate que la valeur médiane est supérieure le week-end, du samedi au lundi, par rapport aux autres jours de la semaine. Un lien avec les activités humaines notamment les loisirs en plein air (promenade, barbecue) est facile à imaginer.
            
            Cette première analyse met donc dors et déjà en évidence des liens de corrélations entre le nombre de feux et la dimension temporelle.</b>
            </div>
            """, unsafe_allow_html=True
        )
        # Transition vers l'analyse ANOVA
        st.markdown("---")
        st.markdown("Analysons maintenant les résultats du test ANOVA entre le mois et le nombre d'incendies.")

        # Test ANOVA ('MONTH' <-> Number of fires)
        result = smf.ols(formula='FOD_ID ~ MONTH', data=df).fit()
        table = statsmodels.api.stats.anova_lm(result)
        st.write(table)

        # Analyse des résultats du test ANOVA
        st.markdown(
        """
        ### Résultats du test ANOVA

        Les résultats de l'ANOVA montrent une valeur F de 871.508747 et une valeur p associée de 1.696398e-191. Ces résultats suggèrent une différence statistiquement significative entre les mois en termes de nombre d'incendies.

        - **F-statistique (F)** : La valeur F est très élevée, ce qui indique que les variations entre les mois expliquent une part importante de la variation totale des incendies.
        - **P-valeur (PR(>F))** : La valeur p est extrêmement faible (bien inférieure à 0.05), ce qui signifie que la probabilité que ces résultats soient dus au hasard est quasi nulle. Cela confirme que le mois a un impact significatif sur le nombre d'incendies.

        En résumé, le test ANOVA confirme que le mois de l'année influence de manière significative le nombre d'incendies, soutenant les observations visuelles faites à partir des graphiques.
        """
        )

    with dimension_tabs[1]:
        st.header("Dimension spatiale")
        st.markdown(
        """
        La répartition des feux sur le territoire est un facteur clé dans leur analyse, directement liée à d’autres variables comme le climat, chaud et sec dans le sud par exemple, et la densité de population, plus de surface à brûler dans les régions peu peuplées ou plus de déclenchement liées aux activités humaines dans les régions densément peuplées.

        Le jeu de données contient finalement 3 niveaux géographiques : les grandes régions GACC (Geographic Area Coordination Centers), les États et les Comtés. Au niveau le plus élevé, la figure suivante présente la distribution du nombre de feux par grande région.
        """
        )

        # Créer deux colonnes
        col1, col2 = st.columns([2, 2])  # Vous pouvez ajuster les proportions

        with col1:
            # Compter le nombre de feux par région GACC
            count_by_gacc = df.groupby('GACC_area').size()

            # Trier par ordre décroissant
            count_by_gacc_sorted = count_by_gacc.sort_values(ascending=False)

            # Création du graphique avec Plotly
            fig = go.Figure()

            # Ajout des barres avec la couleur spécifique
            fig.add_trace(go.Bar(x=count_by_gacc_sorted.index, y=count_by_gacc_sorted.values, marker_color='#FF8C00'))

            # Personnalisation de l'axe x et de l'axe y
            fig.update_xaxes(title='Région GACC')
            fig.update_yaxes(title='Nombre de feux')

            # Personnalisation du titre centré en gras
            fig.update_layout(title={'text':'Nombre de feux par région GACC',
                                     'font':{'size':18},
                                     'x':0.5,  # Centrer le titre
                                     'xanchor':'center'},  # Ancrer le titre au centre
                              height=400, width=500)

            # Affichage du graphique
            st.plotly_chart(fig)

        with col2:
          # Convertir en GeoDataFrame
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE))
            
           # Échantillonnage pour réduire la taille des données affichées
            sample_gdf = gdf.sample(n=10000, random_state=42) if len(gdf) > 10000 else gdf

            # Création de la carte avec Plotly Express
            fig_map = px.scatter_geo(sample_gdf, lat=sample_gdf.geometry.y, lon=sample_gdf.geometry.x,
                                 title='Répartition géographique des feux',
                                 scope='usa',
                                 opacity=0.6)

            # Mettre à jour les paramètres de la carte pour un fond transparent et des points orange
            fig_map.update_geos(showcountries=False,
                                showcoastlines=False,
                                showland=False,
                                fitbounds="locations")

            fig_map.update_traces(marker=dict(color='#FF8C00', size=5))

            fig_map.update_layout(title={'text':'Répartition géographique des incendies',
                                         'font':{'size':18},
                                         'x':0.5,  # Centrer le titre
                                         'xanchor':'center'},  # Ancrer le titre au centre
                                  geo=dict(bgcolor='rgba(0,0,0,0)'),
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  height=400, width=500)

            # Affichage de la carte
            st.plotly_chart(fig_map)
        
        # Analyse des graphs
        st.markdown(
        """
        La région Southern est nettement la plus représentée en termes de nombre d’incendies. Avec les régions Southwest et Southern California, le sud du pays est clairement plus touché par les incendies que le nord.
        """
        )
        
        st.markdown("---")

        # Compter le nombre de feux par état
        count_by_state = df.groupby('STATENAME').size()

        # Trier par ordre décroissant
        count_by_state_sorted = count_by_state.sort_values(ascending=False)

        # Création du graphique avec Plotly
        fig = go.Figure()

        # Ajout des barres avec la couleur spécifique
        fig.add_trace(go.Bar(x=count_by_state_sorted.index, y=count_by_state_sorted.values, marker_color='#FF8C00'))

        # Personnalisation de l'axe x et de l'axe y
        fig.update_xaxes(title='Etat')
        fig.update_yaxes(title='Nombre de feux')

        # Personnalisation du titre centré en gras
        fig.update_layout(title={'text':'<b>Nombre de feux par état</b>',
                                 'font':{'size':18},
                                 'x':0.5,
                                 'xanchor':'center'},
                         height=400, width=600)

        # Affichage du graphique
        st.plotly_chart(fig)

        # Analyse du graphique par état
        st.markdown(
        """
        En analysant le nombre de feux par état, on remarque que certains états sont beaucoup plus touchés que d’autres, ce qui peut s’expliquer par des facteurs géographiques, climatiques et démographiques variés.
        """
        )
        # Analyse avec test ANOVA pour 'GACC_area'
        st.markdown("---")
        st.markdown("Analysons maintenant les résultats du test ANOVA entre les régions GACC et le nombre d'incendies.")

        # Test ANOVA ('GACC_area' <-> Number of fires)
        result_gacc = smf.ols(formula='FOD_ID ~ GACC_area', data=df).fit()
        table_gacc = statsmodels.api.stats.anova_lm(result_gacc)
        st.write(table_gacc)

        # Analyse des résultats du test ANOVA pour 'GACC_area'
        st.markdown(
        """
        ### Résultats du test ANOVA pour les régions GACC

        Les résultats de l'ANOVA montrent une valeur F de {} et une valeur p associée de {}. Ces résultats suggèrent une différence statistiquement significative entre les régions GACC en termes de nombre d'incendies.

        - **F-statistique (F)** : La valeur F indique dans quelle mesure les moyennes des groupes sont différentes. Plus la valeur de F est grande, plus il est improbable que les moyennes des groupes soient égales.
        - **P-valeur (PR(>F))** : La valeur p est très faible (bien inférieure à 0.05), ce qui signifie que la probabilité que ces résultats soient dus au hasard est quasi nulle. Cela confirme que la région GACC a un impact significatif sur le nombre d'incendies.

        En résumé, le test ANOVA confirme que la région GACC influence de manière significative le nombre d'incendies, soutenant les observations visuelles faites à partir des graphiques.
        """.format(table_gacc.loc['GACC_area', 'F'], table_gacc.loc['GACC_area', 'PR(>F)'])
        )

    with dimension_tabs[2]:
        st.header("Dimension cause des incendies")
        st.markdown(
            """
            Les causes des incendies de forêt sont variées et peuvent être d'origine naturelle ou humaine. Le jeu de données contient des informations détaillées sur les causes des incendies permettant d'analyser les tendances et les corrélations.
            """
        )

        # Calcul du nombre d'incendies par cause
        fires_by_cause = df['STAT_CAUSE_DESCR'].value_counts().sort_values()

        # Création du graphique avec Plotly en utilisant la palette Turbo
        fig = px.bar(x=fires_by_cause.values,
                     y=fires_by_cause.index,
                     orientation='h',
                     labels={'x':'Nombre d\'incendies', 'y':'Cause'},
                     color=fires_by_cause.values,
                     color_continuous_scale='turbo')

        # Mise à jour de la mise en page pour centrer et mettre en gras le titre
        fig.update_layout(title={'text': '<b>Répartition des incendies par cause</b>',
                                 'font':{'size':18},
                                 'x':0.5,
                                 'xanchor': 'center'},
                         height=400, width=600)

        # Affichage du graphique
        st.plotly_chart(fig)

        # Analyse du graphique par cause
        st.markdown(
            """
            La cause principale des feux de forêt est d’origine humaine puisque liée à des activités de brûlages de débris résidentiels ou industriels. Pour mettre en évidence ce phénomène, les causes des incendies ont été catégorisées en 2 classes : les feux d’origine naturelle et d'origine humaine.
            
            """
        )

        st.markdown("---")

        # Calcul du nombre d'incendies par cause
        fire_cause = df['STAT_CAUSE_DESCR'].value_counts()

        # Filtre des sources d'allumage
        human_induced = ['Equipment Use', 'Smoking', 'Campfire', 'Debris Burning', 'Railroad', 'Arson', 'Children', 'Fireworks', 'Powerline', 'Structure', 'Miscellaneous']
        natural_cause = ['Lightning']

        # Calcul du pourcentage des sources d'allumage
        human_fire = (fire_cause.loc[human_induced].sum() / df.shape[0]) * 100
        natural_fire = (fire_cause.loc[natural_cause].sum() / df.shape[0]) * 100

        # Création du graphique avec Plotly
        fig = go.Figure()

        # Ajout des barres
        fig.add_trace(go.Bar(x=['Human-induced', 'Natural cause'], y=[human_fire, natural_fire], marker_color=['#aa5042', '#d8bd8a']))

        # Personnalisation de l'axe y
        fig.update_yaxes(range=[0, 100], title='Pourcentage des incendies')

        # Personnalisation du titre
        fig.update_layout(title={'text':'<b>Répartition des incendies par source d\'allumage</b>',
                                 'font':{'size':18},
                                 'x':0.5,
                                 'xanchor':'center'},
                         height=400, width=600)

        # Affichage du graphique
        st.plotly_chart(fig)

        # Analyse du graphique par cause
        st.markdown(
            """
            On constate que plus de 3 feux de forêt sur 4 ont pour origine une action humaine.
            """
        )

        st.markdown("---")

        # Calcul de la taille moyenne des incendies par cause
        size_cause = df.groupby('STAT_CAUSE_DESCR')['FIRE_SIZE'].mean().sort_values()

        # Création du graphique avec Plotly en utilisant la palette Turbo
        fig = px.bar(x=size_cause.values,
                     y=size_cause.index,
                     orientation='h',
                     labels={'x':'Taille moyenne des incendies (acres)', 'y':'Cause'},
                     color=size_cause.values,
                     color_continuous_scale='turbo')

        # Mise à jour de la mise en page pour centrer et mettre en gras le titre
        fig.update_layout(title={'text': '<b>Taille moyenne des incendies par cause</b>',
                                 'font':{'size':18},
                                 'x':0.5,
                                 'xanchor':'center'},
                         height=400, width=600)

        # Affichage du graphique
        st.plotly_chart(fig)

        # Analyse du graphique de la taille moyenne des incendies par cause
        st.markdown(
            """
            La taille des incendies est significativement plus importante lorsque la cause est la foudre. Cela conforte l’hypothèse que les méga feux sont majoritairement d’origine naturelle. Une analyse détaillée de la localisation géographique des points de départ permettra de mettre en évidence la relation entre la distance des zones d’habitation, l’accessibilité du terrain et la durée des incendies.

            PS : Selon une étude, les feux d’origine humaine se situent généralement dans un rayon de 50 m d’une zone d’habitation (résidentielle ou industrielle). En cas de départ, le feu est rapidement constaté et les moyens de défense rapidement mis en œuvre eu égard à l’accessibilité. En cas de cause naturelle : foudre (ou lignes électriques qui touchent la végétation par vent fort par exemple), il y a rarement une présence humaine à proximité directe et la topographie peut accentuer les difficultés d’accès.
            """
        )
        
         # Analyse avec test ANOVA pour 'STAT_CAUSE_DESCR'
        st.markdown("---")
        st.markdown("Analysons maintenant les résultats du test ANOVA entre la cause des incendies et leur taille moyenne.")

        # Test ANOVA ('STAT_CAUSE_DESCR' <-> Fire size)
        result_cause_size = smf.ols(formula='FIRE_SIZE ~ STAT_CAUSE_DESCR', data=df).fit()
        table_cause_size = statsmodels.api.stats.anova_lm(result_cause_size)
        st.write(table_cause_size)

        # Analyse des résultats du test ANOVA pour 'STAT_CAUSE_DESCR'
        st.markdown(
        """
        ### Résultats du test ANOVA pour la cause des incendies et leur taille moyenne

        Les résultats de l'ANOVA montrent une valeur F de {} et une valeur p associée de {}. Ces résultats suggèrent une différence statistiquement significative entre les causes des incendies en termes de taille moyenne.

        - **F-statistique (F)** : La valeur F est élevée, ce qui indique que les variations entre les causes d'incendies expliquent une part importante de la variation totale de la taille des incendies.
        - **P-valeur (PR(>F))** : La valeur p est très faible (bien inférieure à 0.05), ce qui signifie que la probabilité que ces résultats soient dus au hasard est quasi nulle. Cela confirme que la cause des incendies a un impact significatif sur la taille moyenne des incendies.

        En résumé, le test ANOVA confirme que la cause des incendies influence de manière significative la taille moyenne des incendies, soutenant les observations visuelles faites à partir des graphiques.
        """.format(table_cause_size.loc['STAT_CAUSE_DESCR', 'F'], table_cause_size.loc['STAT_CAUSE_DESCR', 'PR(>F)'])
        )

if __name__ == "__main__":
    run()