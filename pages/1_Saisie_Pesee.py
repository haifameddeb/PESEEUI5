import streamlit as st
from database import add_tare
from datetime import datetime

st.set_page_config(page_title="Saisie Pesée - UI5", layout="wide")

st.markdown("""
<style>
    .ui5-form-header {
        background: white;
        padding: 1.5rem;
        border-bottom: 1px solid #d8d8d8;
        margin-bottom: 2rem;
    }
    .ui5-form-card {
        background: white;
        padding: 2rem;
        border-radius: 4px;
        border: 1px solid #d8d8d8;
        max-width: 800px;
        margin: auto;
    }
    .stButton > button {
        background-color: #427cac !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ui5-form-header">
    <h2 style="color: #354a5f; margin: 0;">Entrée Camion : Saisie de la Tare</h2>
    <p style="color: #6a6d70; margin: 0;">Remplissez les informations pour générer le ticket d'entrée.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ui5-form-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Données Documentaires**")
        no_q = st.text_input("N° Quittance (STAM)")
        no_p = st.text_input("N° Pesée")
    
    with col2:
        st.markdown("**Données Véhicule**")
        mat = st.text_input("Matricule")
        poids = st.number_input("Poids Tare (KG)", step=10)
    
    prod = st.selectbox("Produit à charger", ["BLÉ TENDRE", "MAÏS", "SOJA", "ORGE"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ENREGISTRER TARE (SAVE)", use_container_width=True):
        if mat and poids > 0:
            add_tare(no_q, no_p, mat, "TRANSPORT", prod, poids, datetime.now())
            st.toast("✅ Document enregistré avec succès", icon="💾")
            st.success("Synchronisation Sage X3 en attente...")
        else:
            st.error("Veuillez renseigner tous les champs obligatoires.")
    
    st.markdown('</div>', unsafe_allow_html=True)
