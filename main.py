import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION v3.3 ---
st.set_page_config(page_title="ENKI v3.0 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""

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

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO VALIDÉE) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", 
                      ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'élément")
        s_desc = st.text_area("Description physique précise")
        s_type = st.selectbox("Source visuelle", ["Upload Image", "Lien URL", "Texte seul"])
        s_img = None
        if s_type == "Upload Image": s_img = st.file_uploader("Fichier", type=["png", "jpg", "jpeg"])
        elif s_type == "Lien URL": s_img = st.text_input("URL Image")
        if st.button("Graver le Sceau"):
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_img, "active": True})
            st.rerun()

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
            if seal['ref'] and hasattr(seal['ref'], 'name'): st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset)"):
        st.session_state.messages = []
        st.session_state.last_sage_response = ""
        st.rerun()

# --- INTERFACE PRINCIPALE (UI PHOTO VALIDÉE) ---
st.title("🏛️ ENKI v3.0 : The Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {model_name} | Statut : Optimisé pour 2026")

tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        
        # LIGNE DE BOUTONS (EXACTEMENT COMME LA PHOTO)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                response = model_obj.generate_content(f"Tu es {role}. Contexte : {active_context}\n\n{user_input}")
                st.session_state.last_sage_response = response.text
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
        
        with c2:
            if st.button("🎨 Image Directe", use_container_width=True, help="Ouvrir l'Atelier"):
                st.toast("🎨 Vision transmise à l'Atelier de Ninharsag !")
        with c3:
            if st.button("🎬 Vidéo Directe", use_container_width=True, help="Ouvrir Veo 3"):
                st.toast("🎬 Séquence envoyée aux Visions de Veo 3 !")
        with c4:
            if st.button("🎼 Audio Direct", use_container_width=True, help="Ouvrir Lyria 3"):
                st.toast("🎼 Harmoniques prêtes dans les Fréquences de Lyria !")

# --- TAB 2 : ATELIER DE NINHARSAG (IMAGE PRO RESTAURÉ) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_sage_response, height=150)
            ratio = st.selectbox("Géométrie Sacrée (Format)", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        with col_a2:
            style = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Manga High-Fid", "Bas-relief Royal"])
            finish = st.multiselect("Finition", ["Hyper-détaillé", "8k textures", "Ray-tracing", "Atmosphère brumeuse"], default=["8k textures"])
        if st.form_submit_button("🚀 Graver le Prompt Image"):
            st.code(f"STYLE: {style}. FORMAT: {ratio}. SCENE: {vision}. SCEAUX: {active_context}. --cref")

# --- TAB 3 : VISIONS DE VEO 3 (VIDÉO PRO RESTAURÉ) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence temporelle...", value=st.session_state.last_sage_response, height=150)
            res = st.select_slider("Résolution", options=["720p", "1080p", "4K", "8K"], value="4K")
        with col_v2:
            mouv = st.selectbox("Mouvement Caméra", ["Drone Shot", "Traveling", "Steadycam", "Zoom lent"])
            fps = st.radio("Images/sec", ["24 (Ciné)", "30 (TV)", "60 (Action)"], horizontal=True)
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.code(f"VEO 3. RES: {res}. FPS: {fps}. CAM: {mouv}. ACTION: {action}. PERSISTANCE: {active_context}")

# --- TAB 4 : FRÉQUENCES DE LYRIA (AUDIO PRO RESTAURÉ) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            ambiance = st.text_area("Paysage sonore...", value=st.session_state.last_sage_response, height=150)
            type_s = st.selectbox("Type d'Harmonique", ["Musique Épique", "Ambiance Sombre", "Chant Rituel"])
        with col_s2:
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Héroïque"], value="Mystérieux")
            duree = st.slider("Durée (sec)", 10, 60, 30)
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.code(f"LYRIA 3. TYPE: {type_s}. MOOD: {nrj}. DURÉE: {duree}s. DESC: {ambiance}. COHÉRENCE: {active_context}")
