import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ULTIME 2026 ---
st.set_page_config(page_title="ENKI v3.3 : Abzu Command Center", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- INITIALISATION ÉVOLUÉE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "active_tab" not in st.session_state: st.session_state.active_tab = "📜 Scribe"
if "prefill_prompt" not in st.session_state: st.session_state.prefill_prompt = ""

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
    except: pass
    return None, "Signal Interrompu"

model_obj, model_name = get_sage_engine()

# --- FONCTION DE NAVIGATION ---
def navigate_to(tab_name):
    st.session_state.active_tab = tab_name
    # Capturer la dernière réponse pour le pre-fill
    if st.session_state.messages:
        st.session_state.prefill_prompt = st.session_state.messages[-1]["content"]
    st.rerun()

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel", "Le Sage Anunnaki"])
    
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Créer un Sceau", expanded=False):
        s_name = st.text_input("Nom")
        s_desc = st.text_area("Description physique")
        s_type = st.selectbox("Source", ["Upload Image", "Lien URL", "Texte"])
        s_ref = None
        if s_type == "Upload Image": s_ref = st.file_uploader("Fichier", type=["png", "jpg"])
        elif s_type == "Lien URL": s_ref = st.text_input("URL")
        if st.button("Graver le Sceau"):
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_ref, "active": True})
            st.rerun()

    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"])
        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.vault.pop(i)
                st.rerun()
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref'] and hasattr(seal['ref'], 'name'): st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Reset System"):
        st.session_state.messages = []
        st.session_state.active_tab = "📜 Scribe"
        st.rerun()

# --- NAVIGATION STYLE TABS ---
nav_cols = st.columns(4)
tabs_list = ["📜 Scribe", "🎨 Atelier", "🎬 Visions", "🎼 Fréquences"]
for i, tab in enumerate(tabs_list):
    if nav_cols[i].button(tab, use_container_width=True, type="primary" if st.session_state.active_tab == tab else "secondary"):
        st.session_state.active_tab = tab
        st.rerun()

st.divider()

# --- CONTENU DYNAMIQUE ---

# --- 📜 SCRIBE DE DESTINÉE ---
if st.session_state.active_tab == "📜 Scribe":
    st.title("📜 Scribe de Destinée")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="main_input")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                response = model_obj.generate_content(f"Tu es {role}. Contexte : {active_context}\n\n{user_input}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
        
        # BOUTONS DE NAVIGATION DIRECTE FONCTIONNELS
        with c2: 
            if st.button("🎨 Image Directe", use_container_width=True): navigate_to("🎨 Atelier")
        with c3: 
            if st.button("🎬 Vidéo Directe", use_container_width=True): navigate_to("🎬 Visions")
        with c4: 
            if st.button("🎼 Audio Direct", use_container_width=True): navigate_to("🎼 Fréquences")

# --- 🎨 ATELIER DE NINHARSAG ---
elif st.session_state.active_tab == "🎨 Atelier":
    st.title("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.prefill_prompt, height=150)
            ratio = st.selectbox("Format", ["1:1", "4:5", "16:9", "21:9", "9:16"])
        with col_a2:
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art", "Manga High-Fid"])
            light = st.selectbox("Lumière", ["Cinématique", "Divine", "Néon Noir"])
            finish = st.multiselect("Finition", ["Hyper-détaillé", "Ray-tracing", "Atmosphère"])
        if st.form_submit_button("🚀 Graver le Prompt Image"):
            st.code(f"STYLE: {style}. FORMAT: {ratio}. LIGHT: {light}. SCENE: {vision}. SCEAUX: {active_context}")

# --- 🎬 VISIONS DE VEO 3 ---
elif st.session_state.active_tab == "🎬 Visions":
    st.title("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        sequence = st.text_area("Action de la vision...", value=st.session_state.prefill_prompt, height=150)
        res = st.select_slider("Résolution", options=["720p", "1080p", "4K", "8K"])
        mouv = st.selectbox("Mouvement", ["Drone Shot", "Traveling", "Steadycam"])
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.code(f"VEO 3 PRODUCTION. RES: {res}. CAM: {mouv}. ACTION: {sequence}. PERSISTANCE: {active_context}")

# --- 🎼 FRÉQUENCES DE LYRIA ---
elif st.session_state.active_tab == "🎼 Fréquences":
    st.title("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        paysage = st.text_area("Paysage sonore...", value=st.session_state.prefill_prompt, height=150)
        type_s = st.selectbox("Type", ["Musique Épique", "Ambiance Sombre", "Chant Rituel"])
        nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Héroïque"])
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.code(f"LYRIA 3. TYPE: {type_s}. MOOD: {nrj}. DESC: {paysage}. COHÉRENCE: {active_context}")
