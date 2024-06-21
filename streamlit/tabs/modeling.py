# modeling.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import make_classification
from sklearn.metrics import roc_curve, auc
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve
import joblib
import os
from datetime import datetime
import numpy as np

# Chemin vers le répertoire des données prétraitées
preprocessed_data_dir = r"data/modeling_data"

# Fonction pour charger les données prétraitées
@st.cache_data()
def load_data(forest_name):
    file_path = os.path.join(preprocessed_data_dir, f"{forest_name}_preprocessed.csv")
    return pd.read_csv(file_path)

# Fonction pour charger le modèle entraîné
@st.cache_resource()
def load_model(forest_name, use_smote):
    if use_smote:
        model_path = os.path.join(preprocessed_data_dir, f"{forest_name}_smote_model.pkl")
    else:
        model_path = os.path.join(preprocessed_data_dir, f"{forest_name}_base_model.pkl")
    return joblib.load(model_path)


title = "Modeling des incendies dans les forêts nationales"
sidebar_name = "Modeling"

def run():
    SUBPAGES = {
        "Le modèle": subpage1,
        "Prédiction": subpage2,
    }
    st.sidebar.title('Prédiction')
    selection = st.sidebar.radio("", list(SUBPAGES.keys()))
    subpage = SUBPAGES[selection]
    subpage()

def subpage1():
    st.header('Présentation du modèle')
    st.markdown("---")
    
    # Sélection du modèle
    st.markdown(
        """
        <h4>1. Sélection du modèle de prédiction du risque d'incendie de forêt</h4>
        <p>
        Dans le cadre de notre projet de prédiction du risque d'incendie, nous avons exploré diverses problématiques avant de nous concentrer sur les incendies dans les forêts nationales. Comme mentionné précédemment, ces forêts sont des espaces vitaux, symbolisant notre capacité à protéger la faune et la flore face au dérèglement climatique. Pour garantir la fiabilité de nos prédictions et venir en soutien à l'USFS, nous avons évalué plusieurs algorithmes de machine learning : Random Forest Classifier, Logistic Regression, Multi-Layer Perceptron, Support Vector Machine ou encore Gradient Boosting Classifier.
        
        Le choix du modèle final a été guidé par plusieurs critères : la capacité à gérer le déséquilibre des classes, la précision des prédictions et la facilité d'interprétation des résultats. Après une évaluation approfondie et une optimisation des hyperparamètres, le Gradient Boosting Classifier s'est démarqué comme le modèle le plus performant pour cette tâche de prédiction.
        </p>
        """,
        unsafe_allow_html=True
        )
    
    # Présentation du Gradient Boosting Classifier
    st.markdown(
        """
        <h4>2. Présentation du Gradient Boosting Classifier</h4>
        <p>
        Le Gradient Boosting Classifier (GBC) est un algorithme d'apprentissage supervisé qui construit un modèle prédictif en combinant de manière itérative plusieurs modèles d'arbre de décision faibles. À chaque itération, un nouveau modèle est entraîné sur les erreurs du modèle précédent, permettant ainsi de corriger progressivement les erreurs de prédiction. 
        
        Le GBC est particulièrement efficace pour gérer les problèmes de classification déséquilibrés, où une classe est sous-représentée par rapport à l'autre. Dans le contexte de la prédiction du risque d'incendie, cette capacité à traiter les déséquilibres de classes est cruciale, car les incendies de forêt sont des événements relativement rares par rapport aux situations sans incendie.</p>
        """,
        unsafe_allow_html=True
        )
    
    # Préparation des données
    st.markdown(
        """
        <h4>3. Préparation des données</h4>
        <p>
        Avant d'entraîner le modèle, les données brutes ont été soigneusement prétraitées. Cela comprend le nettoyage des valeurs manquantes ou aberrantes, la normalisation des variables numériques et le codage des variables catégorielles. 
        
        Une étape cruciale a été l'application de techniques d'échantillonnage pour équilibrer les classes, telles que SMOTE (Synthetic Minority Over-sampling Technique). Cette approche consiste à synthétiser de nouvelles instances appartenant à la classe minoritaire (incendies de forêt) afin d'équilibrer la répartition des classes dans l'ensemble d'entraînement.""",
        unsafe_allow_html=True
        )

    # Sélectionner la forêt
    forest_list = [f.rsplit("_preprocessed.csv", 1)[0] for f in os.listdir(preprocessed_data_dir) if f.endswith("preprocessed.csv")]
    selected_forest = st.selectbox("", forest_list)

    # Charger les données prétraitées pour la forêt sélectionnée
    forest_df = load_data(selected_forest)
    
    
    # Couleur personnalisée pour les graphiques
    custom_color = '#FF8C00'  # Un ton de beige pour le feu
    
    
    
    '''# Calculer le taux de valeurs manquantes par variable
    missing_rate = forest_df.isna().sum() / len(forest_df)
    
    # Créer un graphique à barres
    fig, ax = plt.subplots(figsize=(12, 6))
    missing_rate.plot(kind='bar', ax=ax)
    ax.set_title('Taux de valeurs manquantes par variable')
    ax.set_xlabel('Variables')
    ax.set_ylabel('Taux de valeurs manquantes')
    
    # Rotation des étiquettes de l'axe x pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Afficher le graphique dans Streamlit
    st.subheader('Taux de valeurs manquantes par variable')
    st.pyplot(fig)
    '''
    model = load_model(selected_forest, use_smote=False)
    
    
    # Répartition des classes
    st.subheader("Répartition des classes")
    class_counts = forest_df['target'].value_counts().reset_index()
    class_counts.columns = ['Classe', 'Nombre']
    class_counts['Classe'] = class_counts['Classe'].map({0: "Pas d'incendie", 1: "Incendie"})
    
    col1, col2 = st.columns([1, 1])

    with col1:
        fig = px.bar(class_counts, x='Classe', y='Nombre', title='Répartition des classes (jours avec et sans incendies)',
                 labels={'Classe': 'Classe', 'Nombre': 'Nombre'}, color_discrete_sequence=[custom_color])
        fig.update_layout(title={'text': '<b>Répartition des classes</b>', 'x':0.5, 'xanchor': 'center'})
    
        # Réduire la largeur du graphique
        fig.update_layout(width=800)  # Ajustez la largeur selon vos besoins
        st.plotly_chart(fig)
    with col2:
        st.markdown("""
        **Description :**
        
        La répartition des classes montre la distribution du nombre de jours avec et sans incendies dans la forêt sélectionnée. Cette visualisation est cruciale pour comprendre l'équilibre ou le déséquilibre entre les deux classes, ce qui impacte directement la capacité du modèle à prédire correctement les incendies.
    
        **Interprétation :**
        - Le graphique montre deux barres représentant respectivement les jours sans incendie et les jours avec incendie.
        - Une répartition équilibrée ou déséquilibrée peut influencer la performance du modèle. Par exemple, un déséquilibre peut nécessiter des techniques spécifiques comme le sur-échantillonnage (SMOTE) pour améliorer les prédictions sur la classe minoritaire.
        """)
    
       
    # Visualisation de la distribution des caractéristiques
    st.subheader("Distribution des caractéristiques")
    feature = st.selectbox("Sélectionnez une caractéristique", forest_df.columns[:-1], index=2)
    
    # Définir la couleur personnalisée
    custom_color = "#FF8C00"
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Créer une figure et un axe
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Tracer l'histogramme et la courbe de densité
        sns.histplot(data=forest_df, x=feature, kde=True, color=custom_color, ax=ax)
        
        # Personnaliser le graphique
        ax.set_title(f"Distribution de {feature}", fontweight="bold", fontsize=16)
        ax.set_xlabel(feature, fontsize=8)
        ax.set_ylabel("Nombre", fontsize=8)
        ax.tick_params(axis="both", which="major", labelsize=12)
        
        # Ajouter une grille
        ax.grid(True, alpha=0.3)
        
        # Centrer le titre
        ax.set_title(ax.get_title(), loc="center")
        
        # Afficher le graphique dans Streamlit
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **Description :** 
        
        Ce graphique illustre la distribution d'une caractéristique spécifique : par exemple, température, précipitation enregistrée dans ou à proximité dans la forêt sélectionnée moyennée sur 1 jours, 10 jours ou 30 jours. Comprendre la distribution des caractéristiques permet de détecter des patterns ou des comportements qui pourraient être corrélés avec les incendies.
    
        **Interprétation :**
        - L'axe horizontal représente les valeurs de la caractéristique sélectionnée.
        - L'axe vertical montre le nombre d'occurrences de chaque valeur ou la densité de la distribution.
        - Les pics ou les tendances dans la distribution peuvent indiquer des conditions météorologiques ou environnementales favorisant les incendies.
        """)
                
    
    # Courbe ROC pour le modèle sélectionné
    st.subheader("Courbe ROC")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        y_true = forest_df['target']
        y_pred = model.predict_proba(forest_df.drop(columns=['target']))[:, 1]
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC curve (area = {roc_auc:.2f})', line=dict(color=custom_color, width=2)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(color='gray', width=2, dash='dash')))
        fig.update_layout(title={'text': f'<b>Receiver Operating Characteristic (ROC Curve)</b> (area = {roc_auc:.2f})', 'x':0.5, 'xanchor': 'center'},
                          xaxis_title='False Positive Rate',
                          yaxis_title='True Positive Rate')
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Description :** 
        
        La courbe ROC évalue la performance du modèle de prédiction en fonction de ses taux de vrais positifs et de faux positifs. Elle représente la sensibilité (True Positive Rate) en fonction de la spécificité (1 - False Positive Rate) à différents seuils de classification.
    
        **Interprétation :**
        - La courbe montre la capacité du modèle à discriminer entre les jours avec incendie et sans incendie.
        - Plus la courbe ROC est proche du coin supérieur gauche, meilleure est la performance du modèle.
        - L'aire sous la courbe (AUC) est un indicateur de la performance globale du modèle, où une valeur proche de 1 indique une meilleure capacité prédictive.
        """)
        
    
    # Histogramme des Prédictions
    st.subheader("Histogramme des Prédictions")
    
    col1, col2 = st.columns([1, 1])
    
    with col1: 
        predictions = model.predict(forest_df.drop(columns=['target']))
    
        fig = px.histogram(predictions, x=predictions, title='Distribution des prédictions', labels={'x': 'Prédiction'}, color_discrete_sequence=['#FF8C00'])
        fig.update_layout(title={'text': '<b>Histogramme des Prédictions</b>', 'x': 0.5, 'xanchor': 'center'})
        
        # Centrer le graphique dans la colonne
        fig.update_layout(width=600)  # Ajustez la largeur selon vos besoins
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Description :** 
        
        Cet histogramme représente la distribution des prédictions du modèle pour la probabilité ou la classe prédite des jours dans la forêt.    

        **Interprétation :**
        - L'axe horizontal représente les valeurs prédites (probabilité ou classe).
        - L'axe vertical montre le nombre de jours prédits à chaque valeur.
        - Un histogramme bien calibré montre une répartition équilibrée des prédictions entre les deux classes (incendie vs. pas d'incendie).
        """)


    # Matrice de Confusion
    st.subheader("Matrice de Confusion")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        y_true = forest_df['target']
        y_pred = model.predict(forest_df.drop(columns=['target']))
        cm = confusion_matrix(y_true, y_pred)
        
        fig = px.imshow(cm, labels=dict(x="Prédit", y="Vrai"), x=['Pas d\'incendie', 'Incendie'], y=['Pas d\'incendie', 'Incendie'], 
                        title='Matrice de Confusion')
        fig.update_layout(title={'text': '<b>Matrice de Confusion</b>', 'x': 0.5, 'xanchor': 'center'})
        
        # Centrer le graphique dans la colonne
        fig.update_layout(width=600)  # Ajustez la largeur selon vos besoins
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Description :** 
        
        La matrice de confusion présente un tableau qui compare les prédictions du modèle avec les valeurs réelles (vrai positif, faux positif, vrai négatif, faux négatif).

        **Interprétation :**
        - Les éléments diagonaux de la matrice représentent les prédictions correctes.
        - Les autres cellules indiquent les erreurs de classification (faux positifs et faux négatifs).
        - Une matrice bien équilibrée montre une bonne performance du modèle avec un nombre élevé de vrais positifs et vrais négatifs.
        """)


    # Courbe Precision-Recall
    st.subheader("Courbe Precision-Recall")

    col1, col2 = st.columns([1,1])
    
    with col1:
        precision, recall, _ = precision_recall_curve(y_true, y_pred)
    
        fig = px.line(x=recall, y=precision, title='Courbe Precision-Recall', labels={'x': 'Recall', 'y': 'Precision'})
        fig.update_layout(title={'text': '<b>Courbe Precision-Recall</b>', 'x': 0.5, 'xanchor': 'center'})
        
        # Centrer le graphique dans la colonne
        fig.update_layout(width=600)  # Ajustez la largeur selon vos besoins
        st.plotly_chart(fig)

    with col2:
        st.markdown("""
        **Description :** 
        
        La courbe Precision-Recall évalue la précision et le rappel du modèle à différents seuils de classification.

        **Interprétation :**
        - Le rappel (Recall) mesure la capacité du modèle à trouver tous les exemples positifs.
        - La précision mesure la proportion d'exemples positifs correctement prédits parmi toutes les prédictions positives.
        - Une courbe qui monte rapidement vers des valeurs élevées de précision et de rappel indique une meilleure performance du modèle.
        """)
        
    
    # Importances des caractéristiques
    st.subheader("Importances des caractéristiques")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        feature_importances = pd.DataFrame(model.feature_importances_, index=forest_df.columns[:-1], columns=['Importance'])
        feature_importances = feature_importances.sort_values(by='Importance', ascending=False).reset_index()
        feature_importances.columns = ['Caractéristique', 'Importance']
        
        fig = px.bar(feature_importances, x='Caractéristique', y='Importance', title='Importances des caractéristiques',
                     labels={'Caractéristique': 'Caractéristique', 'Importance': 'Importance'}, color_discrete_sequence=[custom_color])
        fig.update_layout(title={'text': '<b>Importances des caractéristiques</b>', 'x':0.5, 'xanchor': 'center'},
                          xaxis_tickangle=-45)
        fig.update_layout(width=600)  # Ajustez la largeur selon vos besoins
        st.plotly_chart(fig)   
    
    with col2:
        st.markdown("""
        **Description :** 
        
        Ce graphique montre l'importance relative des différentes caractéristiques utilisées par le modèle pour prendre ses décisions de prédiction.

        **Interprétation :**
        - Les caractéristiques avec une plus grande importance ont un impact plus significatif sur les prédictions du modèle.
        - Ce graphique aide à identifier quelles variables sont les plus pertinentes pour prédire le risque d'incendie de forêt, ce qui peut orienter les efforts de gestion et de prévention.
        """)
                

                                   

def subpage2():
    st.header('Prédiction des Risques d\'Incendie dans une Forêt Nationale')
    st.markdown("---")
    
    st.markdown(
        """
        <h4>Préambule</h4>
        <p>
        Bienvenue dans l'outil de prédiction des risques d'incendie dans une forêt nationale. Cet outil utilise comme modèle prédictif l'algorithme "Gradient Boosting Classifier" basés sur les données historiques pour estimer le niveau de risque d'incendie en fonction des conditions météorologiques et d'autres variables révélées pertinentes dans la précédente partie sur la modélisation .
        </p>
        """,
        unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <h4>Sélection de la forêt</h4>
        <p>
        Commencez par sélectionner l'une des forêts nationales pour laquelle vous souhaitez obtenir une prédiction. L'application prend en charge plusieurs forêts nationales, chacune avec ses propres données prétraitées et modèles de prédiction.
        </p>
        """,
        unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <h4>Caractéristiques des Conditions Environnementales</h4>
        <p>
        Pour obtenir une prédiction précise, vous pouvez spécifier les caractéristiques suivantes :
        <ul>
            <li> <strong>Année</strong> : Choisissez l'année pour laquelle vous souhaitez faire la prédiction, entre 2024 et 2026</li>
            <li> <strong>Jour de l\'année</strong> : Sélectionnez le jour de l'année correspondant à la date pour laquelle vous voulez prédire le risque d'incendie</li>
            <li> <strong>Conditions météorologiques</strong> : Utilisez les sliders pour ajuster les températures maximales moyennes et les précipitations moyennes sur différentes périodes (moyenne, 10 jours, 30 jours)</li>
            <li> <strong>Activités naturelles</strong> : Indiquez la présence d'éclairs (Oui/Non) et le nombre d'incendies sur différentes périodes (1 jour, 10 jours, 30 jours)</li>
        NB : Les sliders pour chaque caractéristique sont fixés par défaut aux valeurs moyennes observées dans les données historiques
        </ul>
        </p>
        """,
        unsafe_allow_html=True
        )
        
    # Sélectionner la forêt
    forest_list = [f.rsplit("_preprocessed.csv", 1)[0] for f in os.listdir(preprocessed_data_dir) if f.endswith("preprocessed.csv")]
    selected_forest = st.selectbox("", forest_list)

    # Charger les données prétraitées pour la forêt sélectionnée
    forest_df = load_data(selected_forest)
    
    # Sélectionner les caractéristiques
    features = forest_df.drop(['target'], axis=1).columns
    
    # Définir les traductions des caractéristiques en français
    feature_translations = {
        'year': 'Année',
        'day_of_year': 'Jour de l\'année',
        'TMAX_mean': 'Température maximale moyenne le jour de la prédiction',
        'TMAX_mean_10D': 'Température maximale moyenne sur 10 jours',
        'TMAX_mean_30D': 'Température maximale moyenne sur 30 jours',
        'PRCP_mean': 'Précipitations moyennes le jour de la prédiction',
        'PRCP_mean_10D': 'Précipitations moyennes sur 10 jours',
        'PRCP_mean_30D': 'Précipitations moyennes sur 30 jours',
        'lightnings': 'Présence d\'éclairs le jour de la prédiction',
        '#wildfires_1D': 'Nombre d\'incendies constatée la veille',
        '#wildfires_10D': 'Nombre d\'incendies sur 10 jours',
        '#wildfires_30D': 'Nombre d\'incendies sur 30 jours'
    }
    
    # Saisir les valeurs des caractéristiques
    feature_values = {}
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            if feature == 'year':
                feature_values[feature] = st.selectbox(
                    feature_translations[feature], 
                    options=range(2024, 2027),  # Plage de 2024 à 2027
                    index=0,  # Index par défaut (2024)
                    key=f"{feature}_selectbox"
                )
            elif feature == 'day_of_year':
                selected_year = feature_values.get('year', int(forest_df['year'].mean()))
                min_date = datetime(selected_year, 1, 1)
                max_date = datetime(selected_year, 12, 31)
                selected_date = st.date_input(
                    feature_translations[feature],
                    value=None, 
                    min_value=min_date, 
                    max_value=max_date,
                    key=f"{feature}_date_input"
                )
                if selected_date:
                    feature_values[feature] = selected_date.timetuple().tm_yday
                else:
                    feature_values[feature] = int((min_date + (max_date - min_date) / 2).timetuple().tm_yday)
            elif 'TMAX' in feature or 'PRCP' in feature:
                feature_values[feature] = st.slider(
                    feature_translations[feature],
                    float(forest_df[feature].min()),
                    float(forest_df[feature].max()),
                    float(forest_df[feature].mean()),
                    format="%.1f"
                )
            elif feature == 'lightnings':
                feature_values[feature] = st.radio(
                    feature_translations[feature],
                    options=["Non", "Oui"],
                    index=0 if int(forest_df[feature].mean()) == 0 else 1,
                    key=feature  # Ajout d'une clé unique pour éviter les problèmes de duplication
                )
                feature_values[feature] = 1 if feature_values[feature] == "Oui" else 0
            elif feature in ['#wildfires_1D', '#wildfires_10D', '#wildfires_30D']:
                feature_values[feature] = st.slider(
                    feature_translations[feature],
                    int(forest_df[feature].min()),
                    int(forest_df[feature].max()),
                    int(forest_df[feature].mean())
                )
            else:
                feature_values[feature] = st.number_input(
                    feature_translations[feature], 
                    value=float(forest_df[feature].mean()), 
                    step=1.0
                )

    # Créer un DataFrame avec les valeurs saisies
    input_data = pd.DataFrame([feature_values])
    
    st.markdown(
        """
        <h4>Utilisation de SMOTE</h4>
        <p>
        Pour améliorer la capacité du modèle à prédire les incendies, vous avez la possibilité d'utiliser la technique SMOTE (Synthetic Minority Over-sampling Technique). Cochez la case correspondante si vous souhaitez appliquer cette méthode.
        </p>
        """,
        unsafe_allow_html=True
        )
    
    # Option pour utiliser SMOTE
    use_smote = st.checkbox("Utiliser SMOTE", value=False)
    
    # Charger le modèle entraîné
    model = load_model(selected_forest, use_smote)

    # Charger les données de test et les prédictions
    X_test = forest_df.drop('target', axis=1)
    y_test = forest_df['target']
    y_pred = model.predict(X_test)

    # Effectuer la prédiction
    if st.button("Prédire"):
        prediction = model.predict(input_data)
        if prediction[0] == 0:
            st.markdown("""
                <div style="background-color: lightgreen; padding: 10px; border-radius: 5px; text-align: center;">
                    <span style="color: green; font-weight: bold;">PAS DE RISQUE DE FEU</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: red; padding: 10px; border-radius: 5px; text-align: center;">
                    <span style="color: white; font-weight: bold; animation: blinker 1s linear infinite;">ATTENTION - RISQUE DE FEU</span>
                </div>
                <style>
                    @keyframes blinker {
                        50% { opacity: 0; }
                    }
                </style>
                """, unsafe_allow_html=True)

