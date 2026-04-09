import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION 2026 ---
st.set_page_config(page_title="ENKI v2.7 - Gen 3 Edition", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- MÉMOIRE DES VERROUS ---
if "locked_data" not in st.session_state:
    st.session_state.locked_data = {
        "Anu": "Homme puissant, barbe majestueuse sumérienne, tiare à 7 paires de cornes dorées.",
        "Ea": "Physique de scientifique royal, regard perçant, symboles techniques.",
        "Ambiance_Nibiru": "Fréquences basses, résonances métalliques, chœurs profonds."
    }

# --- DÉTECTION DYNAMIQUE (MAJ 2026) ---
@st.cache_resource
def get_best_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priorité 2026 : On cherche Gemini 3 en priorité
        for m in available_models:
            if "gemini-3-flash" in m: return genai.GenerativeModel(m), m
        for m in available_models:
            if "gemini-1.5-flash" in m: return genai.GenerativeModel(m), m
            
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash'
    except Exception as e:
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash'

# Initialisation
model_obj, model_name = get_best_model()

# --- SIDEBAR & INTERFACE ---
with st.sidebar:
    st.title("🧠 Mémoire Vive")
    mode = st.radio("Mode :", ["Chercheur Universel", "Sage Anunnaki"])
    st.divider()
    if st.button("🗑️ Reset Discussion"):
        st.session_state.messages = []
        st.rerun()

st.title(f"🏛️ ENKI v2.7")
st.caption(f"📡 Signal stabilisé sur : {model_name}")

tabs = st.tabs(["📜 Intelligence", "🎨 Studio Image", "🎬 Studio Vidéo", "🎼 Studio Sonore"])

# --- TAB 1 : INTELLIGENCE ---
with tabs[0]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Analyse ou Question...", height=150)
        if st.form_submit_button("Lancer la Réflexion"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                contexte = f"Tu es {mode}. Verrous : {st.session_state.locked_data}"
                response = model_obj.generate_content(f"{contexte}\n\n{user_input}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"Erreur de communication : {e}")

# (Les autres onglets Image, Vidéo, Sonore restent identiques)
