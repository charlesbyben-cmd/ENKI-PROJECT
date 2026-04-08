import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ENKI v1.4", layout="wide", page_icon="🏛️")

# Connexion API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante")
    st.stop()

st.title("🏛️ ENKI : Master Archive")

try:
    # --- LE SAGE CHERCHE SA PROPRE FRÉQUENCE ---
    # On liste les modèles qui acceptent de générer du contenu
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # On prend le premier modèle 'flash' ou 'pro' disponible
    model_name = models[0] if models else None
    
    if model_name:
        target = st.selectbox("Cible de l'analyse", ["(Choisir)", "4ème Tablette", "Ea (Enki)"])
        
        if target != "(Choisir)":
            st.success(f"✅ Sage connecté sur la fréquence : {model_name}")
            prompt = st.chat_input("Posez votre question...")
            
            if prompt:
                model = genai.GenerativeModel(model_name)
                # On force le contexte Anunnaki
                full_prompt = f"Tu es le Sage ENKI. Basé sur Sitchin. Sujet : {target}. Question : {prompt}"
                res = model.generate_content(full_prompt)
                st.chat_message("assistant").write(res.text)
    else:
        st.error("Aucun modèle trouvé sur votre compte Google.")

except Exception as e:
    st.error(f"Erreur de synchronisation : {e}")
    st.info("Astuce : Allez dans 'Manage app' -> 'Reboot app' si ce message persiste.")
