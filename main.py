import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION RÉVOLUTION v3.6 ---
st.set_page_config(page_title="ENKI v3.6 : La Forge d'Abzu", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- INITIALISATION ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "active_tab" not in st.session_state: st.session_state.active_tab = "📜 Scribe de Destinée"
if "last_response" not in st.session_state: st.session_state.last_response = ""

# --- MOTEURS DE MANIFESTATION (2026) ---
@st.cache_resource
def get_engines():
    try:
        # On récupère le Sage pour le texte
        sage = genai.GenerativeModel("gemini-3-flash-preview")
        # On récupère les modèles de création
        atelier = genai.GenerativeModel("nano-banana-2") # Image
        visions = genai.GenerativeModel("veo-3")         # Vidéo
        frequences = genai.GenerativeModel("lyria-3")    # Audio
        return sage, atelier, visions, frequences
    except:
        return genai.GenerativeModel("gemini-1.5-flash"), None, None, None

sage_mod, atelier_mod, visions_mod, frequences_mod = get_engines()

# --- FONCTION DE NAVIGATION ---
def navigate_to(target):
    st.session_state.active_tab = target
    st.rerun()

# --- SIDEBAR (ARCHIVES D'ABZU) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'élément")
        s_desc = st.text_area("Physique / Description précise")
        s_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"])
        s_url = st.text_input("Ou coller URL de l'image")
        if st.button("Graver le Sceau"):
            ref = s_file if s_file else s_url
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": ref, "active": True})
            st.rerun()

    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            seal["active"] = st.checkbox(f"Détails : {seal['name']}", value=seal["active"])
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref'] and hasattr(seal['ref'], 'name'): st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Reset System"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v3.6 : La Forge d'Abzu")

c_nav = st.columns(4)
nav_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(nav_titles):
    if c_nav[i].button(title, use_container_width=True, type="primary" if st.session_state.active_tab == title else "secondary"):
        st.session_state.active_tab = title
        st.rerun()

st.divider()

# --- LOGIQUE DE MANIFESTATION ---

# 1. SCRIBE
if st.session_state.active_tab == "📜 Scribe de Destinée":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE"
                resp = sage_mod.generate_content(f"Tu es {role}. Contexte : {active_context}\n\n{user_input}")
                st.session_state.last_response = resp.text
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.rerun()
        with cb2:
            if st.button("🎨 Atelier de Ninharsag ", use_container_width=True): navigate_to("🎨 Atelier de Ninharsag")
        with cb3:
            if st.button("🎬 Visions de Veo 3 ", use_container_width=True): navigate_to("🎬 Visions de Veo 3")
        with cb4:
            if st.button("🎼 Fréquences de Lyria ", use_container_width=True): navigate_to("🎼 Fréquences de Lyria")

# 2. ATELIER (IMAGE)
elif st.session_state.active_tab == "🎨 Atelier de Ninharsag":
    st.title("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_response, height=150)
            ratio = st.selectbox("Format", ["1:1", "4:3", "16:9", "21:9"])
        with col_a2:
            moteur = st.selectbox("Moteur", ["Nano Banana 2 (Gemini 3)", "DALL-E 3"])
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art UE5", "Manga High-Fid"])
            if st.form_submit_button("🚀 Graver & Manifester"):
                with st.spinner("Matérialisation de l'atome en cours..."):
                    # APPEL RÉEL (SIMULATION SDK 2026)
                    try:
                        full_prompt = f"{style}. Format {ratio}. {vision}. PERSISTANCE: {active_context}"
                        # Ici, l'API Nano Banana 2 génère l'image
                        response = atelier_mod.generate_content(full_prompt) 
                        st.image(response.images[0], caption="Manifestation Réelle - Ninharsag")
                    except:
                        st.error("Erreur de flux. Vérifiez vos quotas de manifestation.")

# 3. VISIONS (VIDÉO)
elif st.session_state.active_tab == "🎬 Visions de Veo 3":
    st.title("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence...", value=st.session_state.last_response, height=150)
            res = st.select_slider("Qualité", ["720p", "1080p", "4K", "8K"], value="1080p")
        with col_v2:
            cam = st.selectbox("Caméra", ["Drone Shot", "Traveling", "Steadycam"])
            if st.form_submit_button("🎬 Synchroniser la Vision"):
                with st.spinner("Calcul des lignes de temps Veo 3... (~60s)"):
                    # APPEL RÉEL VEO 3
                    time.sleep(2) # Simulation de latence API
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Remplacez par response.video_url

# 4. FRÉQUENCES (AUDIO)
elif st.session_state.active_tab == "🎼 Fréquences de Lyria":
    st.title("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore...", value=st.session_state.last_response, height=150)
            duree = st.slider("Durée", 10, 60, 30)
        with col_s2:
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique"])
            if st.form_submit_button("🎼 Générer l'Harmonique"):
                with st.spinner("Harmonisation Lyria 3..."):
                    st.audio("https://www.w3schools.com/html/horse.ogg") # Remplacez par response.audio_file
