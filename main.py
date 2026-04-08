import streamlit as st
import google.generativeai as genai

# Configuration minimale
st.set_page_config(page_title="ENKI", layout="wide")

# Connexion à la clé
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API introuvable")
    st.stop()

st.title("🏛️ ENKI : Master Archive")

# On utilise le modèle le plus standard
target = st.selectbox("Cible", ["(Choisir)", "4ème Tablette", "Ea (Enki)", "Enlil"])

if target != "(Choisir)":
    st.info(f"Analyse de : {target}")
    
    prompt = st.chat_input("Posez votre question au Sage...")
    
    if prompt:
        try:
            # On change pour 'gemini-pro', c'est le plus stable sur iPad/Streamlit
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Sujet : {target}. Question : {prompt}")
            st.chat_message("assistant").write(response.text)
        except Exception as e:
            st.error(f"Erreur : {e}")
