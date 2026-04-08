import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ULTIME ---
st.set_page_config(page_title="ENKI v2.4 - Studio Intégral", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

# --- MÉMOIRE ET IDENTITÉ ---
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

st.title(f"🏛️ ENKI Master Studio v2.4")
tabs = st.tabs(["📜 Intelligence", "🎨 Studio Image", "🎬 Studio Vidéo", "🎼 Studio Sonore"])

# --- TAB 1, 2, 3 (Texte, Image, Vidéo conservés et optimisés) ---
with tabs[0]: # Intelligence
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Question ou Analyse...", height=100)
        if st.form_submit_button("Lancer la Réflexion"):
            try:
                model = get_model()
                contexte = f"Mode {mode}. Verrous : {st.session_state.locked_data}"
                response = model.generate_content(f"{contexte}\n\nQuestion : {user_input}")
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception: st.error("Pause quota (30s).")

with tabs[1]: # Image
    with st.form("image_pro"):
        col1, col2 = st.columns(2)
        with col1:
            prompt_img = st.text_area("Sujet...")
            ratio = st.selectbox("Format", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        with col2:
            esthetique = st.selectbox("Style", ["Photo Réelle Brut", "Illustration Concept Art", "Manga High-Fidelity", "Documentaire NatGeo"])
        if st.form_submit_button("🚀 Générer le Prompt Nano Banana 2"):
            st.code(f"STYLE: {esthetique}. SCÈNE: {prompt_img}. FORMAT: {ratio}. VERROUS: {st.session_state.locked_data}")

with tabs[2]: # Vidéo
    with st.form("video_pro"):
        prompt_vid = st.text_area("Action...")
        v_format = st.selectbox("Format Vidéo", ["16:9", "9:16"])
        mouvement = st.selectbox("Caméra", ["Drone Shot", "Traveling", "Zoom lent", "Fixe"])
        if st.form_submit_button("🎬 Synchroniser avec Veo"):
            st.code(f"VÉO 4K. Format: {v_format}. Caméra: {mouvement}. Action: {prompt_vid}. Verrous: {st.session_state.locked_data}")

# --- TAB 4 : STUDIO SONORE (LYRIA 3) ---
with tabs[3]:
    st.header("🎼 Création Sonore & Ambiance Lyria 3")
    with st.form("sound_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            type_son = st.selectbox("Type de création", ["Musique Cinématique", "Ambiance Sonore (ASMR)", "Chant Rituel", "Effets Spéciaux (SFX)"])
            instruments = st.text_input("Instruments dominants...", placeholder="Ex: Harpe sumérienne, synthétiseur sombre, percussions rituelles...")
        with col_s2:
            emotion = st.select_slider("Intensité Émotionnelle", options=["Calme", "Mystérieux", "Épique", "Dramatique", "Divin"])
            duree = st.slider("Durée estimée (secondes)", 10, 60, 30)
            
        description_son = st.text_area("Description de l'ambiance sonore...", placeholder="Ex: Le bruit sourd des propulseurs mêlé à un chant sacré lors du passage de la Lune...")
        
        prep_sound = st.form_submit_button("🎼 Générer le Prompt Lyria 3")
        
        if prep_sound:
            st.write("### 🎼 Script de Manifestation Sonore :")
            lyria_prompt = f"LYRIA 3 AUDIO. Type: {type_son}. Instruments: {instruments}. Émotion: {emotion}. Durée: {duree}s. Ambiance: {description_son}. Cohérence: {st.session_state.locked_data}"
            st.code(lyria_prompt)
            st.success("Configuration audio prête pour l'injection Lyria.")
