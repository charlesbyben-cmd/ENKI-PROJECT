import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION v3.2 ---
st.set_page_config(page_title="ENKI v3.2 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des clés
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
    except: pass
    return None, "Lien interrompu"

model_obj, model_name = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", 
                      ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"],
                      help="Le Sage respecte les protocoles de Nibiru.")
    
    st.divider()
    
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour la continuité visuelle.")
    
    # 1. CRÉATION DE SCEAU (RESTAURÉ)
    with st.expander("➕ Créer un Sceau", expanded=False):
        s_name = st.text_input("Nom de l'élément")
        s_desc = st.text_area("Description physique")
        s_type = st.selectbox("Source", ["Upload Image", "Lien URL", "Texte seul"])
        s_img = None
        if s_type == "Upload Image": s_img = st.file_uploader("Fichier", type=["png", "jpg"])
        elif s_type == "Lien URL": s_img = st.text_input("URL Image")
            
        if st.button("Graver le Sceau"):
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_img, "active": True})
            st.rerun()

    # 2. LISTE DES SCEAUX (RESTAURÉ)
    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            seal["active"] = st.checkbox(f"Détails : {seal['name']}", value=seal["active"])
        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.vault.pop(i)
                st.rerun()
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref'] and hasattr(seal['ref'], 'name'):
                st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset)"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v3.2 : The Visual Continuity Revolution")
st.caption(f"Connecté via : {model_name}")

tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse la...", height=100, key="main_input")
        if st.button("🔱 Lancer la Réflexion"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            role_p = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
            full_p = f"Tu es {role_p}. Contexte : {active_context}\n\n{user_input}"
            response = model_obj.generate_content(full_p)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

    if st.session_state.messages:
        st.divider()
        st.subheader("⚡ Manifestation Immédiate")
        m_col1, m_col2 = st.columns([0.4, 0.6])
        with m_col1:
            moteur = st.selectbox("Sceau de Manifestation", ["Nano Banana 2", "DALL-E 3", "Veo 3 (Vidéo)"])
        with m_col2:
            st.write("")
            c1, c2, c3 = st.columns(3)
            with c1: st.button("🎨 Image", use_container_width=True)
            with c2: st.button("🎬 Vidéo", use_container_width=True)
            with c3: st.button("🎼 Audio", use_container_width=True)

# --- TAB 2 : ATELIER (DÉTAILLÉ) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        vision = st.text_area("Vision à matérialiser...")
        f_img = st.selectbox("Format", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        style = st.selectbox("Style", ["Photo-réel Brut", "Concept Art", "Manga High-Fid"])
        if st.form_submit_button("🚀 Graver le Prompt"):
            st.code(f"STYLE: {style}. FORMAT: {f_img}. SCENE: {vision}. CONTEXTE: {active_context}")

# --- TAB 3 : VISIONS (DÉTAILLÉ) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        action = st.text_area("Séquence temporelle...")
        res = st.select_slider("Qualité", ["720p", "1080p", "4K", "8K"])
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.code(f"VEO 3. RES: {res}. ACTION: {action}. PERSISTANCE: {active_context}")

# --- TAB 4 : FRÉQUENCES (DÉTAILLÉ) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        amb = st.text_area("Paysage sonore...")
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.code(f"LYRIA 3. AMBIANCE: {amb}. COHERENCE: {active_context}")
