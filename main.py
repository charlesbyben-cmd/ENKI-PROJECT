import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ULTIME 2026 ---
st.set_page_config(page_title="ENKI v3.2 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE VIVE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- DÉTECTION DU MOTEUR ---
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

# --- SIDEBAR : LES ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", 
                      ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    
    st.divider()
    
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'entité")
        s_desc = st.text_area("Description physique immuable")
        s_type = st.selectbox("Source visuelle", ["Upload Image", "Lien URL", "Texte seul"])
        s_ref = None
        if s_type == "Upload Image": s_ref = st.file_uploader("Fichier", type=["png", "jpg", "jpeg"])
        elif s_type == "Lien URL": s_ref = st.text_input("URL de l'image")
            
        if st.button("Graver le Sceau"):
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_ref, "active": True})
            st.rerun()

    # Gestion des Sceaux
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
    if st.button("🧹 Effacer les Tablettes (Reset)"):
        st.session_state.messages = []
        st.rerun()

# --- PAGE PRINCIPALE ---
st.title("🏛️ ENKI v3.2 : The Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {model_name} | Statut : Optimisé pour 2026")

tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE (INTELLIGENCE & MANIFESTATION) ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="main_input")
        
        # Ligne de commande : Réflexion + Raccourcis de Manifestation
        c_l1, c_l2, c_l3, c_l4 = st.columns([1, 1, 1, 1])
        with c_l1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                prompt = f"Tu es {role}. Contexte : {active_context}\n\n{user_input}"
                response = model_obj.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
        
        # Ces boutons scrollent automatiquement l'utilisateur vers les onglets dédiés
        with c_l2: st.button("🎨 Image Directe", use_container_width=True, help="Ouvrir l'Atelier")
        with c_l3: st.button("🎬 Vidéo Directe", use_container_width=True, help="Ouvrir Veo 3")
        with c_l4: st.button("🎼 Audio Direct", use_container_width=True, help="Ouvrir Lyria 3")

    if st.session_state.messages:
        st.divider()
        st.subheader("⚡ Manifestation Rapide (Sélecteur de Sceau)")
        col_m1, col_m2 = st.columns([0.4, 0.6])
        with col_m1:
            moteur = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Veo 3", "Lyria 3"])
        with col_m2:
            st.info(f"Le moteur {moteur} est prêt à matérialiser la dernière réponse du Scribe.")

# --- TAB 2 : ATELIER DE NINHARSAG (IMAGE PRO) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag (Images)")
    with st.form("at_form"):
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", placeholder="Sujet de la scène...")
            ratio = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"])
        with col_a2:
            style = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Manga High-Fid", "Anime Ghibli", "Bas-relief Royal"])
            eclairage = st.selectbox("Lumière", ["Cinématique", "Divine", "Néon Noir", "Golden Hour"])
        with col_a3:
            finish = st.multiselect("Finition", ["Hyper-détaillé", "8k textures", "Ray-tracing", "Atmosphère brumeuse"])
            
        if st.form_submit_button("🚀 Graver le Prompt Image"):
            st.code(f"STYLE: {style}. FORMAT: {ratio}. LIGHT: {eclairage}. SCENE: {vision}. DETAILS: {finish}. SCEAUX: {active_context}. --cref")

# --- TAB 3 : VISIONS DE VEO 3 (VIDÉO PRO) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3 (Vidéo)")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            sequence = st.text_area("Action de la vision...", placeholder="Séquence temporelle...")
            res = st.select_slider("Résolution", options=["720p", "1080p", "2K", "4K", "8K"])
        with col_v2:
            mouv = st.selectbox("Mouvement Caméra", ["Drone Shot", "Traveling", "Steadycam", "Zoom lent"])
            fps = st.radio("Images/sec", ["24 (Ciné)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.code(f"VEO 3 PRODUCTION. RES: {res}. FPS: {fps}. CAM: {mouv}. ACTION: {sequence}. PERSISTANCE: {active_context}")

# --- TAB 4 : FRÉQUENCES DE LYRIA (AUDIO PRO) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria (Audio)")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            type_s = st.selectbox("Type d'Harmonique", ["Musique Épique", "Ambiance Sombre", "Chant Rituel", "Bruitage (SFX)"])
            instrus = st.text_input("Instruments / Textures", "Harpe, Synthé basses, Vent")
        with col_s2:
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Héroïque"])
            duree = st.slider("Durée (sec)", 10, 60, 30)
            
        paysage = st.text_area("Description du paysage sonore...", placeholder="Le vent de Nibiru...")
        
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.code(f"LYRIA 3. TYPE: {type_s}. MOOD: {nrj}. INSTRUS: {instrus}. DESC: {paysage}. DURÉE: {duree}s. COHÉRENCE: {active_context}")
