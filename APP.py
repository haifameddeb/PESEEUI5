import streamlit as st
import pandas as pd
from database import init_db, get_all_pesees, get_dashboard_metrics

st.set_page_config(page_title="Medigrain - UI5 Portal", layout="wide", initial_sidebar_state="collapsed")
init_db()

# --- CSS UI5 / FIORI STYLE ---
st.markdown("""
<style>
    /* Background général style Fiori */
    .stApp { background-color: #edeff0; }
    
    /* Shell Header */
    .ui5-shell-header {
        background-color: #354a5f;
        padding: 10px 20px;
        color: white;
        font-family: "72", Arial, Helvetica, sans-serif;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 4px solid #427cac;
    }
    
    /* Tiles UI5 */
    .ui5-tile {
        background: white;
        border-radius: 4px;
        border: 1px solid #d8d8d8;
        padding: 1rem;
        box-shadow: 0 0 0.125rem 0 rgba(0,0,0,0.1);
        transition: transform 0.2s;
        height: 120px;
        cursor: pointer;
    }
    .ui5-tile:hover { transform: scale(1.02); border-color: #427cac; }
    .ui5-tile-title { color: #6a6d70; font-size: 0.875rem; }
    .ui5-tile-value { color: #427cac; font-size: 2rem; font-weight: bold; margin-top: 10px; }
    
    /* Custom Table */
    .ui5-table-container { background: white; padding: 15px; border-radius: 4px; border: 1px solid #d8d8d8; }
</style>
""", unsafe_allow_html=True)

# Header HTML5
st.markdown("""
<div class="ui5-shell-header">
    <div style="font-weight: bold; font-size: 1.2rem;">MEDIGRAIN | Pont Bascule Portal</div>
    <div style="font-size: 0.9rem;">Utilisateur: Agent Admin</div>
</div>
""", unsafe_allow_html=True)

# Login simple intégré (style dialog)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.container():
        _, col, _ = st.columns([1,1,1])
        with col:
            st.markdown("### Connexion")
            u = st.text_input("ID")
            p = st.text_input("Pass", type="password")
            if st.button("Se connecter", use_container_width=True):
                if u == "admin" and p == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
    st.stop()

# --- TABLEAU DE BORD ---
metrics = get_dashboard_metrics()

# Tiles SAP Fiori
c1, c2, c3, c4 = st.columns(4)
tiles = [
    ("Tare Prise", metrics["tare_prise"], "#427cac"),
    ("En Chargement", metrics["en_cours"], "#e69a00"),
    ("Terminés", metrics["termine"], "#2b7d2b"),
    ("Total Jour", metrics["total"], "#354a5f")
]

for i, col in enumerate([c1, c2, c3, c4]):
    with col:
        st.markdown(f"""
        <div class="ui5-tile">
            <div class="ui5-tile-title">{tiles[i][0]}</div>
            <div class="ui5-tile-value" style="color: {tiles[i][2]}">{tiles[i][1]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Table de données UI5
st.markdown('<div class="ui5-table-container">', unsafe_allow_html=True)
st.subheader("📋 Liste des Mouvements (Logs)")
df = get_all_pesees()
if not df.empty:
    st.dataframe(df[["matricule_camion", "produit", "statut", "date_heure_entree"]], use_container_width=True, hide_index=True)
else:
    st.info("Aucun mouvement enregistré.")
st.markdown('</div>', unsafe_allow_html=True)
