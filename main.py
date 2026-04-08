import streamlit as st
import google.generativeai as genai
import os

# Configuration de la page
st.set_page_config(page_title="ENKI v1.4", layout="wide")

# Configuration de l'API (Utilise le Secret de Streamlit)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets !")

# --- TITRE ---
st.title("🏛️ ENKI : Master Archive v1.4")
st.subheader("⚙️ Centre d'Opérations")

# --- INITIALISATION DE LA VARIABLE CIBLE ---
# On définit 'target' ici pour éviter l'erreur que tu as eue
target = "(Choisir)" 

# --- INTERFACE DE SÉLECTION ---
with st.expander("🔍 Sélectionner une Tablette ou une Entité", expanded=True):
    target = st.selectbox(
        "Sur quel sujet le Sage doit-il concentrer son analyse ?",
        ["(Choisir)", "Ea (Enki)", "Enlil", "Anu", "4ème Tablette", "Livre d'Enki (Complet)"]
    )

# --- LOGIQUE D'ANALYSE ---
if target != "(Choisir)":
    st.info(f"Analyse en cours pour : **{target}**")
    
    # Zone de chat pour l'IA
    user_input = st.chat_input(f"Posez une question sur {target}...")
    
    if user_input:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # On ajoute le contexte Anunnaki au prompt
        full_prompt = f"Tu es le Sage Numérique ENKI. En te basant sur les Chroniques de Zecharia Sitchin, réponds à ceci concernant {target} : {user_input}"
        
        with st.spinner("Consultation des archives de Nibiru..."):
            response = model.generate_content(full_prompt)
            st.chat_message("assistant").write(response.text)
else:
    st.warning("Veuillez sélectionner une cible dans le menu ci-dessus pour activer le Sage.")
