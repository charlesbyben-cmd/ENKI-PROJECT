import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- CONFIGURATION RÉVOLUTION v4.8 ---
st.set_page_config(page_title="ENKI v4.8 : Unification of Wisdom Chronicles", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google 'GEMINI_API_KEY' manquante.")
    st.stop()

# --- INITIALISATION DES SYSTÈMES & GESTION DES CHRONIQUES ---
# Initialisation de la structure multi-discussions
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [
        {"id": "nibiru_sacree", "name": "Nibiru : Orbite Sacrée", "messages": [], "last_response": ""},
    ]
if "active_chronicle_id" not in st.session_state:
    st.session_state.active_chronicle_id = "nibiru_sacree"

# Fonction d'aide pour obtenir la chronique active
def get_active_chronicle():
    for chronicle in st.session_state.chronicles:
        if chronicle["id"] == st.session_state.active_chronicle_id:
            return chronicle
    return None

active_chronicle = get_active_chronicle()

# Initialisation des Sceaux (commun à toutes les discussions pour la continuité)
if "vault" not in st.session_state: st.session_state.vault = []

# --- MOTEUR SAGE (INTELLIGENCE & VISION) ---
@st.cache_resource
def get_sage_engine():
    # Gemini 1.5 Flash pour l'analyse multi-modale
    return genai.GenerativeModel("gemini-1.5-flash")

model_obj = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU & GESTIONNAIRE DE CHRONIQUES (NOUVEAU) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    st.divider()
    
    # --- GESTIONNAIRE DE CHRONIQUES (Discussions/Projets) ---
    st.subheader("📜 Tablettes de Destinée (Chroniques)")
    
    # Bouton Nouvelle Tablette
    if st.button("➕ Nouvelle Tablette (Discussion)", use_container_width=True):
        new_id = f"chronicle_{len(st.session_state.chronicles) + 1}"
        new_chronicle = {"id": new_id, "name": f"Nouvelle Chronique {len(st.session_state.chronicles) + 1}", "messages": [], "last_response": ""}
        st.session_state.chronicles.append(new_chronicle)
        st.session_state.active_chronicle_id = new_id
        st.rerun()

    # Liste des Chroniques existantes (selectbox pour iPad)
    st.write("**Cliquer pour charger une Chronique (Discussion) :**")
    chronicle_names = [c["name"] for c in st.session_state.chronicles]
    active_chronicle_name = st.selectbox("Sélectionner une Tablette active :", 
                                          options=chronicle_names, 
                                          index=chronicle_names.index(active_chronicle["name"]),
                                          label_visibility="collapsed")
    
    # Mise à jour de l'ID actif si le nom change
    for c in st.session_state.chronicles:
        if c["name"] == active_chronicle_name:
            st.session_state.active_chronicle_id = c["id"]
            break

    # Actions sur la Chronique Active
    c1, c2 = st.columns(2)
    with c1:
        # Renommer (Simulation pour iPad, le vrai renommage nécessiterait une pop-up)
        st.caption("✏️ Renommer (iPad limitation)")
    with c2:
        # Supprimer
        if st.button("🗑️ Briser la Tablette", help="Supprimer définitivement cette discussion"):
            if len(st.session_state.chronicles) > 1:
                idx_to_remove = next((i for i, c in enumerate(st.session_state.chronicles) if c["id"] == st.session_state.active_chronicle_id), None)
                if idx_to_remove is not None:
                    st.session_state.chronicles.pop(idx_to_remove)
                    st.session_state.active_chronicle_id = st.session_state.chronicles[0]["id"]
                    st.rerun()
            else:
                st.warning("Impossible de briser l'unique Tablette Sacrée.")

    st.divider()
    
    # --- SCEAUX DE PERSISTANCE ---
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau", expanded=False):
        s_name = st.text_input("Nom de l'élément (Perso, Objet, Décor)")
        s_desc = st.text_area("Physique / Description précise")
        s_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="sidebar_up")
        if st.button("Graver le Sceau"):
            if s_name and s_desc:
                st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_file, "active": True})
                st.rerun()

    # Affichage des Sceaux
    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Détails : {seal['name']}", value=seal["active"], key=f"seal_{i}")
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    # Reset System pour la Chronique Active
    if st.button("🧹 Effacer les Tablettes (Reset Active Chronicle)"):
        active_chronicle = get_active_chronicle()
        active_chronicle["messages"] = []
        active_chronicle["last_response"] = ""
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG PHOTO VALIDÉE) ---
st.title("🏛️ ENKI v4.8 : Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : Gemini-1.5-Flash | Chronique Active : {active_chronicle['name']}")

# LES VRAIS ONGLETS
tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE (AVEC FUSION CONSOLE & MULTI-CHRONICLES) ---
with tabs[0]:
    # Affichage des messages de la Chronique Active
    for msg in active_chronicle["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    # LA CONSOLE UNIFIÉE (Fusion Analyse + Saisie)
    with st.container(border=True):
        col_clip, col_up = st.columns([0.05, 0.95])
        with col_clip: st.markdown("### 📎")
        with col_up:
            uploaded_file = st.file_uploader("Joindre Image, Vidéo, Audio ou PDF pour analyse...", 
                                            type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf", "txt"],
                                            label_visibility="collapsed")
        
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input", placeholder=f"Écris tes consigne pour la Chronique active '{active_chronicle['name']}' ici...")
        
        # LIGNE DE BOUTONS (COPIES EXACTES DU HAUT)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if user_input or uploaded_file:
                    active_chronicle["messages"].append({"role": "user", "content": user_input if user_input else "Analyse du document joint."})
                    
                    # Préparation du prompt multi-modal
                    prompt_parts = [f"Tu es le Sage. Contexte : {active_context}\n\nChronique active : {active_chronicle['name']}\n\n{user_input}"]
                    if uploaded_file:
                        if uploaded_file.type.startswith("image/"):
                            prompt_parts.append(PIL.Image.open(uploaded_file))
                        else:
                            prompt_parts.append({"mime_type": uploaded_file.type, "data": uploaded_file.read()})

                    with st.spinner(f"Le Sage scrute les tablettes de '{active_chronicle['name']}'..."):
                        try:
                            resp = model_obj.generate_content(prompt_parts)
                            active_chronicle["last_response"] = resp.text
                            active_chronicle["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Erreur de communication : {e}")
                    st.rerun()
        
        with c2: st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="btn_at")
        with c3: st.button("🎬 Visions de Veo 3", use_container_width=True, key="btn_vi")
        with c4: st.button("🎼 Fréquences de Lyria", use_container_width=True, key="btn_ly")

# --- TAB 2 : ATELIER DE NINHARSAG (AVEC L'ATOME REEL) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            # Capture automatique de la pensée de la Chronique Active
            vision = st.text_area("Vision à matérialiser...", value=active_chronicle["last_response"], height=150)
            format_img = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"])
        with col_a2:
            moteur = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"])
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k Leica)", "Concept Art UE5", "Manga High-Fid", "Bas-relief Royal"])
            qualite = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"])
            
        if st.form_submit_button("🚀 Graver & Manifester sur place"):
            # L'Atome Réel : Nano Banana 2 (Pollinations)
            if moteur == "Nano Banana 2":
                with st.spinner("Manifestation en cours..."):
                    p_enc = vision.replace(" ", "%20").replace("\n", "%20")
                    url = f"https://image.pollinations.ai/prompt/{p_enc}%20aesthetic%20{style}%20{format_img}%20coherence%20{active_context}?nologo=true&enhance=true"
                    st.image(url, caption=f"Manifestation {moteur} réussie")

# --- TAB 3 : VISIONS DE VEO 3 (CONF. PHOTO) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            # Capture de la pensée de la Chronique Active
            action = st.text_area("Séquence temporelle...", value=active_chronicle["last_response"], height=150)
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
            cam = st.selectbox("Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
            fps = st.radio("Images/sec", ["24 (Cinéma)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser la Vision (Simulation)"):
            st.warning(f"Calcul des lignes de temps {res} via {moteur_v}...")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- TAB 4 : FRÉQUENCES DE LYRIA (CONF. PHOTO) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore à harmoniser...", value=active_chronicle["last_response"], height=150)
            duree = st.slider("Durée (secondes)", 10, 60, 30)
        with col_s2:
            moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
            
        if st.form_submit_button("🎼 Générer l'Harmonique (Simulation)"):
            st.success(f"Harmonisation via {moteur_audio} terminée.")
            st.audio("https://www.w3schools.com/html/horse.ogg")
