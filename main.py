import streamlit as st
import os
import urllib.parse
import google.generativeai as genai

# --- CONFIGURATION SÉCURISÉE ---
st.set_page_config(page_title="ENKI v1.4 - Neural Sage", layout="wide")

# Connexion au cerveau Gemini via le Secret Replit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    ai_active = True
except:
    ai_active = False

DB_PATH = "database/assets"
os.makedirs(DB_PATH, exist_ok=True)

# ... (Garder AESTHETICS, FORMATS et DNA_MASKS des versions précédentes) ...

st.title("🏛️ ENKI : Master Archive v1.4")

col_sidebar, col_main, col_prod = st.columns([1, 2, 1])

# --- COLONNE CENTRALE : LES ONGLETS ---
with col_main:
    st.header("⚙️ Centre d'Opérations")
    if target != "(Choisir)":
        t1, t2, t3, t4 = st.tabs(["📝 Scénario", "🎨 Esthétique", "📐 Format", "🧠 Sage Analytique"])
        
        with t1:
            action = st.text_area("Scène :", "He examines a crystal tablet...")
            
        with t4:
            st.subheader("📚 Analyse de la 4ème Tablette")
            if not ai_active:
                st.error("⚠️ Clé API non détectée. Configure le Secret 'GEMINI_API_KEY' dans Replit.")
            
            tablet_text = st.text_area("Colle le texte à étudier ici :", height=200, placeholder="Texte de la 4ème tablette...")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔍 ANALYSER LE TEXTE"):
                    prompt_analyse = f"En tant qu'expert en mythologie sumérienne et conseiller visuel pour le projet ENKI, analyse ce texte : '{tablet_text}'. Extraits les éléments visuels clés, l'ambiance et les détails technologiques pour une scène de film."
                    response = model.generate_content(prompt_analyse)
                    st.session_state['analysis'] = response.text
            
            with col_b:
                if st.button("🎨 SUGGÉRER PROMPT"):
                    prompt_suggestion = f"Basé sur ce texte : '{tablet_text}', génère un prompt descriptif ultra-réaliste pour Ea (Enki) au format 35mm."
                    response = model.generate_content(prompt_suggestion)
                    st.session_state['suggestion'] = response.text

            if 'analysis' in st.session_state:
                st.info(st.session_state['analysis'])
            if 'suggestion' in st.session_state:
                st.success(f"**Suggestion de prompt :** {st.session_state['suggestion']}")
    else:
        st.info("Sélectionnez un sujet.")

# --- COLONNE DROITE : PRODUCTION ---
with col_prod:
    st.header("🎬 Rendu & Chat")
    # ... (Garder le bouton GÉNÉRER IMAGE de la v1.2) ...
    
    st.divider()
    st.subheader("💬 Chat avec ENKI")
    if ai_active:
        user_msg = st.text_input("Question au Sage :")
        if user_msg:
            chat_response = model.generate_content(f"Réponds en tant qu'IA ENKI experte du projet : {user_msg}")
            st.write(f"**Sage ENKI :** {chat_response.text}")
