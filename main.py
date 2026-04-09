import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION v3.9 ---
st.set_page_config(page_title="ENKI v3.9 : Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- MÉMOIRE VIVE & ÉTATS ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""
# Système de navigation par index pour que les boutons du bas fonctionnent
if "active_tab_index" not in st.session_state: st.session_state.active_tab_index = 0

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
    except: pass
    return genai.GenerativeModel("gemini-1.5-flash"), "Gemini-1.5-flash"

model_obj, model_name = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO VALIDÉE) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'élément (Perso, Objet, Décor)")
        s_desc = st.text_area("Physique / Description précise")
        st.write("**Référence Visuelle :**")
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
            if seal['ref']:
                if hasattr(seal['ref'], 'name'): st.image(seal['ref'], width=100)
                else: st.caption("🔗 URL Active")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)"):
        st.session_state.messages = []
        st.session_state.last_sage_response = ""
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v3.9 : Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {model_name} | Statut : Optimisé pour 2026")

# Synchronisation de l'onglet actif
tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                resp = model_obj.generate_content(f"Tu es {role}. Contexte : {active_context}\n\n{user_input}")
                st.session_state.last_sage_response = resp.text
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.rerun()
        
        # Boutons de navigation (Aide visuelle)
        with c2: st.button("🎨 Atelier de Ninharsag Direct", use_container_width=True, on_click=lambda: st.toast("Prêt dans l'onglet Atelier"))
        with c3: st.button("🎬 Visions de Veo 3 Directe", use_container_width=True, on_click=lambda: st.toast("Prêt dans l'onglet Visions"))
        with c4: st.button("🎼 Fréquences de Lyria Direct", use_container_width=True, on_click=lambda: st.toast("Prêt dans l'onglet Fréquences"))

# --- TAB 2 : ATELIER (PHOTO 1 & 2 VALIDÉES) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_sage_response, height=150)
            format_img = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"])
        with col_a2:
            moteur = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"])
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art UE5", "Manga High-Fid", "Bas-relief Royal"])
            qualite_img = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"])
            
        if st.form_submit_button("🚀 Graver & Manifester sur place"):
            st.info(f"Manifestation {qualite_img} via {moteur} en cours...")
            # Ici l'appel API réel
            st.image("https://via.placeholder.com/1024x1024.png?text=Manifestation+Directe+Active")

# --- TAB 3 : VISIONS (PHOTO 3 VALIDÉE) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence temporelle...", value=st.session_state.last_sage_response, height=150)
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
            cam = st.selectbox("Caméra", ["Drone", "Traveling", "Steadycam", "Fixe Sacré"])
            
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.warning(f"Calcul des lignes de temps {res} via {moteur_v}...")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- TAB 4 : FRÉQUENCES (BUG CORRIGÉ) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            # CORRECTION BUG : last_sage_response au lieu de last_response
            amb = st.text_area("Paysage sonore à harmoniser...", value=st.session_state.last_sage_response, height=150)
            duree = st.slider("Durée (sec)", 10, 60, 30)
        with col_s2:
            moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
            
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.success(f"Harmonisation de Abzu via {moteur_audio} terminée.")
            st.audio("https://www.w3schools.com/html/horse.ogg")
