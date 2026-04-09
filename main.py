import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION v3.4 ---
st.set_page_config(page_title="ENKI v3.4 : Manifestation Divine", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DES ÉTATS ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "active_tab" not in st.session_state: st.session_state.active_tab = "📜 Scribe"
if "last_response" not in st.session_state: st.session_state.last_response = ""

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
    except: pass
    return None, "Signal Faible"

model_obj, model_name = get_sage_engine()

# --- FONCTION DE TÉLÉPORTATION ---
def teleport_to(target):
    st.session_state.active_tab = target
    st.rerun()

# --- SIDEBAR (ARCHIVES D'ABZU) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel", "Le Sage Anunnaki"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Créer un Sceau", expanded=False):
        s_name = st.text_input("Nom")
        s_desc = st.text_area("Physique")
        s_ref = st.file_uploader("Image Réf", type=["png", "jpg"])
        if st.button("Graver"):
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
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Reset System"):
        st.session_state.messages = []
        st.session_state.active_tab = "📜 Scribe"
        st.rerun()

# --- NAVIGATION SUPÉRIEURE (SYNCHRONISÉE) ---
c_nav = st.columns(4)
if c_nav[0].button("📜 Scribe de Destinée", use_container_width=True, type="primary" if st.session_state.active_tab == "📜 Scribe" else "secondary"):
    st.session_state.active_tab = "📜 Scribe"
if c_nav[1].button("🎨 Atelier de Ninharsag", use_container_width=True, type="primary" if st.session_state.active_tab == "🎨 Atelier" else "secondary"):
    st.session_state.active_tab = "🎨 Atelier"
if c_nav[2].button("🎬 Visions de Veo 3", use_container_width=True, type="primary" if st.session_state.active_tab == "🎬 Visions" else "secondary"):
    st.session_state.active_tab = "🎬 Visions"
if c_nav[3].button("🎼 Fréquences de Lyria", use_container_width=True, type="primary" if st.session_state.active_tab == "🎼 Fréquences" else "secondary"):
    st.session_state.active_tab = "🎼 Fréquences"

st.divider()

# --- LOGIQUE D'AFFICHAGE ---

# 1. SCRIBE DE DESTINÉE
if st.session_state.active_tab == "📜 Scribe":
    st.title("📜 Scribe de Destinée")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        
        # LES BOUTONS DOUBLES (HAUT ET BAS)
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                resp = model_obj.generate_content(f"Tu es {role}. Contexte : {active_context}\n\n{user_input}")
                st.session_state.last_response = resp.text
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.rerun()
        
        # BOUTONS DE NAVIGATION DIRECTE
        with col_b2:
            if st.button("🎨 Atelier de Ninharsag ", use_container_width=True): teleport_to("🎨 Atelier")
        with col_b3:
            if st.button("🎬 Visions de Veo 3 ", use_container_width=True): teleport_to("🎬 Visions")
        with col_b4:
            if st.button("🎼 Fréquences de Lyria ", use_container_width=True): teleport_to("🎼 Fréquences")

# 2. ATELIER DE NINHARSAG (MANIFESTATION IMAGE)
elif st.session_state.active_tab == "🎨 Atelier":
    st.title("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_response, height=150)
            ratio = st.selectbox("Format", ["1:1", "16:9", "21:9", "9:16"])
        with col_a2:
            moteur = st.selectbox("Moteur", ["Nano Banana 2", "DALL-E 3"])
            style = st.selectbox("Esthétique", ["Photo-réel Brut", "Concept Art", "Manga"])
            if st.form_submit_button("🚀 Graver & Manifester"):
                st.info(f"Manifestation en cours via {moteur}...")
                # Ici l'appel API Nano Banana 2 ou DALL-E 3
                st.image("https://via.placeholder.com/800x450.png?text=Manifestation+Directe+Active", caption="Manifestation en temps réel")

# 3. VISIONS DE VEO 3 (MANIFESTATION VIDÉO)
elif st.session_state.active_tab == "🎬 Visions":
    st.title("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence...", value=st.session_state.last_response, height=150)
            res = st.select_slider("Qualité", ["1080p", "4K", "8K"])
        with col_v2:
            cam = st.selectbox("Caméra", ["Drone", "Traveling", "Fixe"])
            if st.form_submit_button("🎬 Synchroniser & Visionner"):
                st.warning("Génération Veo 3 en cours (30-60s)...")
                st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Placeholder vidéo direct

# 4. FRÉQUENCES DE LYRIA (MANIFESTATION AUDIO)
elif st.session_state.active_tab == "🎼 Fréquences":
    st.title("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore...", value=st.session_state.last_response, height=150)
            duree = st.slider("Durée", 10, 60, 30)
        with col_s2:
            nrj = st.select_slider("Énergie", ["Calme", "Tension", "Épique"])
            if st.form_submit_button("🎼 Générer l'Harmonique"):
                st.audio("https://www.w3schools.com/html/horse.ogg") # Placeholder audio direct
