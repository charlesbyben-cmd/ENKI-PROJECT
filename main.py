import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION PRO ---
st.set_page_config(page_title="ENKI v2.6 - Auto-Adaptative", layout="wide", page_icon="🏛️")

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

# --- DÉTECTION DYNAMIQUE DU MODÈLE (Solution au 404) ---
@st.cache_resource
def get_best_model():
    try:
        # On liste tous les modèles disponibles sur ton compte Pro
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # On cherche par priorité : Gemini 2.0, puis 1.5 Flash
        for m in available_models:
            if "gemini-2.0-flash" in m: return genai.GenerativeModel(m), m
        for m in available_models:
            if "gemini-1.5-flash" in m: return genai.GenerativeModel(m), m
            
        # Si rien n'est trouvé, on prend le tout premier de la liste
        return genai.GenerativeModel(available_models[0]), available_models[0]
    except Exception as e:
        st.error(f"Erreur de détection : {e}")
        return None, None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧠 Mémoire Vive")
    mode = st.radio("Mode d'opération :", ["Chercheur Universel", "Sage Anunnaki"])
    st.divider()
    with st.expander("📝 Gérer les Verrous"):
        for k, v in st.session_state.locked_data.items():
            st.session_state.locked_data[k] = st.text_area(f"{k}", v)
    if st.button("🗑️ Reset Discussion"):
        st.session_state.messages = []
        st.rerun()

# Récupération du modèle
model_obj, model_name = get_best_model()

st.title(f"🏛️ ENKI v2.6")
if model_name:
    st.caption(f"📡 Connecté sur la fréquence : {model_name}")

tabs = st.tabs(["📜 Intelligence", "🎨 Studio Image", "🎬 Studio Vidéo", "🎼 Studio Sonore"])

# --- TAB 1 : INTELLIGENCE ---
with tabs[0]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Analyse ou Question...", height=150)
        submitted = st.form_submit_button("Lancer la Réflexion")
        
        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            if model_obj:
                try:
                    contexte = f"Mode {mode}. Verrous : {st.session_state.locked_data}"
                    response = model_obj.generate_content(f"{contexte}\n\nQuestion : {user_input}")
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur de communication : {e}")
            else:
                st.error("Aucun modèle trouvé.")

# --- Garder les autres onglets identiques ---
# (Studio Image, Vidéo, Sonore restent les mêmes que v2.5)
