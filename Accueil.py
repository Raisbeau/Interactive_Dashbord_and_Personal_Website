import streamlit as st
from st_functions import st_button

st.set_page_config(page_title="Accueil", page_icon="♻",layout="wide")
icon_size = 20
col1, col2, col3 = st.columns(3,gap="small")
with col1:
  st_button('newsletter', 'mailto:raisbeau@hotmail.com', 'Envoyer un Email', icon_size)
with col2:
  st_button('linkedin', 'https://www.linkedin.com/in/rdanchi/', 'Me suivre sur LinkedIn', icon_size)
with col3:
  st_button('github', 'https://github.com/Raisbeau', 'GitHub repo', icon_size)
st.divider()
st.subheader("A propos de Rais Beaurel")

st.markdown(
    """
    Rais Beaurel DANCHI FEUJIO est un étudiant en master 2 de **Capteurs, Instrumentation et Mesures** 
    à **sorbonne Université**. À titre personnel, il travail sur des protocoles de transfert de données 
    de capteurs, les méthodes d'acquisitions et d'analyse de données. Il travaille aussi sur divers 
    types de capteurs, notamment sur les capteurs de surveillance de la qualité d'air. Il a conçu un 
    capteur de surveillance de la qualité d'air qui permet de mesurer la concentration des différents
    polluants de l'air (O3, NO2, CO2, COV, CO, les particules (PM)). Les données en temps réel de ces 
    capteurs peuvent être consultées sur le menu Pollution temps réel.\n
    Il travaille actuellement sur un capteur de mesure de concentration d'ozone basé sur le principe 
    d'absorption UV. Ce type de capteur est plus stable, précis et rapide que les capteurs électrochimiques 
    utilisés dans le précèdent projet. 
    """
)

st.subheader("Expérience")
st.markdown("""
#### Laboratoire Atmosphères, Milieux, Observations Spatiales (LATMOS) (10.05.2023 - 10.07.2023)
##### **Stagiaire Ingénieur Métrologue**
- Test de validation de capteurs miniaturisés de particules et de gaz en laboratoire et sur la tour
- Traitement des données de capteur en Python
- Étalonnage des capteurs à l'aide des valeures de référence des capteurs d'ozone (POM) et de
particules (OSIRIS)
#### Expérience académique, Projets / travaux pratiques (01.09.2022 - 03.05.2023)
 - **Sorbonne Université (Travaux pratiques et projets)**
   - Conditionnement et étalonnage de capteurs (8h)
   - Conception d'une alimentation à découpage (4h)
   - Conception d'un modulateur et démodulateur FSK et AM (Projet 20h)
   - Commande d'un capteur de force de type MEMS (8h)
- **Shijiazhuang Tiedao University (Projets d'un an)**
  - Conception d'un palier magnétique hybride
    - Simulation des circuits magnétiques sur COMSOL et ANSYS MAXWELL
    - Analyse des pertes par courant de Foucault et la distribution du champ magnétique
    - Rédaction et présentation d'un article de recherche à une conférence internationale
#### PANO INDUSCAM (29.07.2018 - 29.08.2019)
##### **Électricien**
- Installation électrique : tuyauterie, câblage des boites des coffrets, installation des
équipements de sécurité
- Maintenance des installations électriques
#### COMPÉTENCES
- Techniques
  - Mesure électrique
  - Etalonnage de capteurs
  - Traitement des données en Python
  - Programmation C/C++ et Python
- Outils/Méthodes
  - MATLAB/Simulink, Cadence Virtuoso
  - Excel/Word
- Savoir-être - Savoir-faire
  - Sens de travail en équipe
  - Innovateur
  - Rigoureux
""", unsafe_allow_html=True)

f = open("main.css")
st.markdown(f"""<style>{f.read()}</style>""",unsafe_allow_html=True)
f.close()
# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)