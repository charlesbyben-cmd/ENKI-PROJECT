import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION PRESTIGE 2026 ---
st.set_page_config(page_title="ENKI v2.8 - Total Studio", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- MÉMOIRE DES VERROUS (COHÉRENCE TOTALE) ---
if "locked_data" not in st.session_state:
    st.session_state.locked_data = {
        "Anu": "Homme puissant, barbe majestueuse sumérienne, tiare à 7 paires de cornes dorées.",
        "Ea": "Physique de scientifique royal, regard perçant, symboles techniques.",
        "Ambiance_Nibiru": "Froid, technologie de pierre sombre, lumières bleutées."
    }

# --- DÉTECTION DU MEILLEUR MOTEUR ---
@st.cache_resource
def get_best_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
        return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash'
    except: return None, None

model_obj, model_name = get_best_model()

# --- INTERFACE ---
with st.sidebar:
    st.title("🧠 Mémoire Vive")
    mode = st.radio("Mode d'opération :", ["Chercheur Universel", "Sage Anunnaki"])
    st.divider()
    with st.expander("📝 Éditer les Verrous Pro"):
        for k, v in st.session_state.locked_data.items():
            st.session_state.locked_data[k] = st.text_area(f"{k}", v)
    if st.button("🗑️ Reset Studio"):
        st.session_state.messages = []
        st.rerun()

st.title(f"🏛️ ENKI Master Studio v2.8")
st.caption(f"🚀 Moteur Actif : {model_name} | Statut : Optimisé pour 2026")

tabs = st.tabs(["📜 Script & Analyse", "🎨 Image Studio", "🎬 Vidéo Studio", "🎼 Audio Lyria 3"])

# --- TAB 1 : INTELLIGENCE ---
with tabs[0]:
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]): st.write(msg["content"])
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Analyse de texte ou directive de production...", height=150)
        if st.form_submit_button("Lancer la Réflexion"):
            st.session_state.setdefault("messages", []).append({"role": "user", "content": user_input})
            contexte = f"Tu es {mode}. Verrous : {st.session_state.locked_data}"
            response = model_obj.generate_content(f"{contexte}\n\n{user_input}")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

# --- TAB 2 : IMAGE (NANO BANANA 2 + STANDARDS INDUSTRIE) ---
with tabs[1]:
    st.header("🎨 Générateur Visuel Haute Fidélité")
    with st.form("image_pro"):
        col1, col2, col3 = st.columns(3)
        with col1:
            prompt_img = st.text_area("Sujet de la scène...", placeholder="Ex: Anu observant la Terre...")
            ratio = st.selectbox("Format d'Image (Aspect Ratio)", 
                               ["1:1 (Carré)", "4:5 (Portrait)", "3:4 (Standard)", "4:3 (Photo)", "16:9 (HD)", "21:9 (Cinémascope)", "9:16 (Vertical)"])
        with col2:
            esthetique = st.selectbox("Esthétique Maître", [
                "Photoréalisme Brut (8k, Leica, RAW)", 
                "Documentaire Cinématographique (Grain 35mm)",
                "Concept Art Ultra-réaliste (Unreal Engine 5)", 
                "Manga Haut de Gamme (Modern Seinen)", 
                "Anime Studio Ghibli (Réaliste)",
                "Peinture à l'huile (Maîtres Anciens)",
                "Cyberpunk Néon-Noir"
            ])
        with col3:
            eclairage = st.selectbox("Éclairage", ["Cinématique", "Lumière du jour", "Néon", "Sombre/Mystérieux", "Golden Hour"])
            details = st.multiselect("Détails additionnels", ["Hyper-détaillé", "Textures 8k", "Atmosphère brumeuse", "Reflets Ray-tracing"])
            
        if st.form_submit_button("🚀 Générer le Prompt Maître Nano Banana 2"):
            st.code(f"STYLE: {esthetique}. FORMAT: {ratio}. LIGHT: {eclairage}. SCENE: {prompt_img}. DETAILS: {', '.join(details)}. COHÉRENCE: {st.session_state.locked_data}")

# --- TAB 3 : VIDÉO (VEO PRO) ---
with tabs[2]:
    st.header("🎬 Studio de Production Vidéo Veo")
    with st.form("video_pro"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            prompt_vid = st.text_area("Scénario de l'action...", placeholder="Ex: Le char d'Abgal entre dans l'atmosphère...")
            v_qualite = st.select_slider("Résolution Vidéo", options=["720p", "1080p (FHD)", "2K", "4K (Ultra HD)", "8K (Cinéma)"])
        with col_v2:
            v_format = st.selectbox("Format Vidéo", ["Horizontal 16:9", "Vertical 9:16 (Social)", "Cinéma 2.39:1"])
            mouvement = st.selectbox("Mouvement Caméra", ["Drone Shot", "Traveling Latéral", "Zoom Progressif", "Steadycam", "Fixe"])
            fps = st.radio("Images par seconde", ["24 (Cinéma)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser avec Veo 4K"):
            st.code(f"VEO PRODUCTION. RES: {v_qualite}. FORMAT: {v_format}. FPS: {fps}. CAMERA: {mouvement}. ACTION: {prompt_vid}. SYNC: {st.session_state.locked_data}")

# --- TAB 4 : AUDIO (LYRIA 3 - AMBIANCE COMPLÈTE) ---
with tabs[3]:
    st.header("🎼 Orchestration Sonore Lyria 3")
    with st.form("sound_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            ambiance = st.selectbox("Ambiance Sonore", ["Musique de Film Épique", "Atmosphère Sci-Fi Sombre", "Chant Sacré/Rituel", "Bruitage Environnemental (SFX)"])
            instrus = st.text_input("Instruments / Textures", "Harpe sumérienne, Synthé basses, Chœurs profonds")
        with col_s2:
            intensite = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Héroïque", "Apocalyptique"])
            duree_son = st.slider("Durée (secondes)", 15, 60, 30)
            
        desc_audio = st.text_area("Description détaillée du paysage sonore...", placeholder="Ex: Le vent de Nibiru soufflant sur les structures de pierre...")
        
        if st.form_submit_button("🎼 Générer l'Ambiance Lyria 3"):
            st.code(f"LYRIA 3 AUDIO. TYPE: {ambiance}. MOOD: {intensite}. INSTRUMENTS: {instrus}. DESC: {desc_audio}. DURÉE: {duree_son}s. COHÉRENCE: {st.session_state.locked_data}")
