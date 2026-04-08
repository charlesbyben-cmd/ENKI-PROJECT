import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION MASTER ---
st.set_page_config(page_title="ENKI v2.5 - Pro Station", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# --- MÉMOIRE DES VERROUS ---
if "locked_data" not in st.session_state:
    st.session_state.locked_data = {
        "Anu": "Homme puissant, barbe majestueuse sumérienne, tiare à 7 paires de cornes dorées.",
        "Ea": "Physique de scientifique royal, regard perçant, symboles techniques.",
        "Ambiance_Nibiru": "Fréquences basses, résonances métalliques, chœurs profonds."
    }

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

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

st.title(f"🏛️ ENKI Master Studio v2.5")
tabs = st.tabs(["📜 Intelligence", "🎨 Studio Image", "🎬 Studio Vidéo", "🎼 Studio Sonore"])

# --- TAB 1 : INTELLIGENCE (TEXTE) ---
with tabs[0]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Analyse ou Question...", height=150)
        submitted = st.form_submit_button("Lancer la Réflexion")
        
        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                model = get_model()
                contexte = f"Mode {mode}. Verrous : {st.session_state.locked_data}"
                response = model.generate_content(f"{contexte}\n\nQuestion : {user_input}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                # ICI : L'erreur précise s'affichera
                st.error(f"⚠️ Alerte Système : {e}")
                st.info("Si l'erreur parle de 'Quota', attendez 30s ou activez le 'Billing' dans Google AI Studio.")

# --- TAB 2, 3, 4 (Conservés pour Nano Banana 2, Veo et Lyria 3) ---
with tabs[1]:
    with st.form("image_pro"):
        prompt_img = st.text_area("Sujet...")
        ratio = st.selectbox("Format", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        esthetique = st.selectbox("Style", ["Photo Réelle Brut", "Illustration Concept Art", "Manga High-Fidelity", "Documentaire NatGeo"])
        if st.form_submit_button("🚀 Générer le Prompt Nano"):
            st.code(f"STYLE: {esthetique}. SCÈNE: {prompt_img}. FORMAT: {ratio}. VERROUS: {st.session_state.locked_data}")

with tabs[2]:
    with st.form("video_pro"):
        prompt_vid = st.text_area("Action...")
        v_format = st.selectbox("Format Vidéo", ["16:9", "9:16"])
        mouvement = st.selectbox("Caméra", ["Drone Shot", "Traveling", "Zoom lent", "Fixe"])
        if st.form_submit_button("🎬 Synchroniser avec Veo"):
            st.code(f"VÉO 4K. Format: {v_format}. Caméra: {mouvement}. Action: {prompt_vid}. Verrous: {st.session_state.locked_data}")

with tabs[3]:
    with st.form("sound_form"):
        type_son = st.selectbox("Type", ["Musique Cinématique", "Ambiance Sonore", "Chant Rituel"])
        instruments = st.text_input("Instruments...")
        description_son = st.text_area("Description...")
        if st.form_submit_button("🎼 Générer le Prompt Lyria 3"):
            st.code(f"LYRIA 3. Type: {type_son}. Instruments: {instruments}. Ambiance: {description_son}. Verrous: {st.session_state.locked_data}")
