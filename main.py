import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="ENKI v2.1", layout="wide", page_icon="🚀")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

# --- MÉMOIRE DES VERROUS ---
if "locked_data" not in st.session_state:
    st.session_state.locked_data = {
        "Anu": "Homme puissant, barbe majestueuse, tiare à 7 cornes.",
        "Ea": "Scientifique royal, regard perçant, symboles techniques."
    }

# --- INITIALISATION DU MODÈLE (FIXE) ---
@st.cache_resource
def get_model():
    # On fixe le modèle pour éviter l'appel API 'list_models' qui consomme du quota
    return genai.GenerativeModel('gemini-1.5-flash')

# --- INTERFACE ---
with st.sidebar:
    st.title("🧠 Mémoire")
    mode = st.radio("Mode :", ["Chercheur Universel", "Sage Anunnaki"])
    st.divider()
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

st.title(f"🚀 ENKI v2.1 : {mode}")
tabs = st.tabs(["💬 Intelligence", "🎨 Studio Image"])

# --- ONGLET TEXTE AVEC FORMULAIRE (Anti-Quota) ---
with tabs[0]:
    # Affichage des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # LE FORMULAIRE : C'est le secret pour ne pas bloquer
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Entrez votre texte ou question ici...")
        submitted = st.form_submit_button("Envoyer au Sage")
        
        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            try:
                model = get_model()
                contexte = f"Tu es {mode}. Données verrouillées : {st.session_state.locked_data}"
                response = model.generate_content(f"{contexte}\n\nQuestion : {user_input}")
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun() # On relance pour afficher la réponse
            except Exception as e:
                st.error("Le serveur est occupé. Attendez 30 secondes.")

# --- ONGLET IMAGE ---
with tabs[1]:
    with st.form("image_form"):
        sujet = st.text_input("Sujet de l'image...")
        generate = st.form_submit_button("Préparer le Prompt")
        
        if generate:
            # On utilise les verrous pour créer le prompt parfait
            prompt_sec = f"Réalisme froid, cinématique. Sujet : {sujet}. Détails verrouillés : {st.session_state.locked_data}"
            st.code(prompt_sec)
            st.info("Copiez ce code pour Nano Banana 2.")
