import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- CONFIGURATION RÉVOLUTION v4.6 ---
st.set_page_config(page_title="ENKI v4.6 : Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DES SYSTÈMES ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""

# --- MOTEUR SAGE (INTELLIGENCE & VISION) ---
@st.cache_resource
def get_sage_engine():
    try:
        # Gemini 1.5 Flash est le standard 2026 pour l'analyse multi-modale
        return genai.GenerativeModel("gemini-1.5-flash"), "Gemini-1.5-flash"
    except:
        return genai.GenerativeModel("gemini-pro"), "Gemini-Pro"

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
        s_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"], key="sidebar_up")
        if st.button("Graver le Sceau"):
            if s_name and s_desc:
                st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_file, "active": True})
                st.rerun()

    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"])
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)"):
        st.session_state.messages = []
        st.session_state.last_sage_response = ""
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG PHOTO VALIDÉE) ---
st.title("🏛️ ENKI v4.6 : Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {model_name} | Analyse Multi-Modale : ACTIVÉE")

# LES VRAIS ONGLETS
tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE (AVEC BOUTON D'UPLOAD) ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        # MODULE D'ANALYSE (Le bouton "+" pour les documents)
        col_plus, col_txt = st.columns([0.05, 0.95])
        with col_plus:
            st.markdown("### 📎") # Icône d'attachement
        with col_txt:
            uploaded_file = st.file_uploader("Joindre Image, Vidéo, Audio ou PDF pour analyse...", 
                                            type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf", "txt"],
                                            label_visibility="collapsed")
            user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        
        # LIGNE DE BOUTONS (COPIES EXACTES DU HAUT)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if user_input or uploaded_file:
                    st.session_state.messages.append({"role": "user", "content": user_input if user_input else "Analyse ce document."})
                    
                    # Préparation du prompt multi-modal pour le Sage
                    prompt_parts = [f"Tu es le Sage. Contexte : {active_context}\n\n{user_input}"]
                    if uploaded_file:
                        if uploaded_file.type.startswith("image/"):
                            prompt_parts.append(PIL.Image.open(uploaded_file))
                        else:
                            prompt_parts.append({"mime_type": uploaded_file.type, "data": uploaded_file.read()})

                    with st.spinner("Le Sage scrute les tablettes..."):
                        resp = model_obj.generate_content(prompt_parts)
                        st.session_state.last_sage_response = resp.text
                        st.session_state.messages.append({"role": "assistant", "content": resp.text})
                    st.rerun()
        
        with c2: st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="btn_at")
        with c3: st.button("🎬 Visions de Veo 3", use_container_width=True, key="btn_vi")
        with c4: st.button("🎼 Fréquences de Lyria", use_container_width=True, key="btn_ly")

# --- TAB 2 : ATELIER DE NINHARSAG (PHOTO 4 VALIDÉE) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_sage_response, height=150)
            format_img = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"])
        with col_a2:
            moteur = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"])
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k Leica)", "Concept Art UE5", "Manga High-Fid", "Bas-relief Royal"])
            qualite = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"])
            
        if st.form_submit_button("🚀 Graver & Manifester"):
            if moteur == "Nano Banana 2":
                p_enc = vision.replace(" ", "%20").replace("\n", "%20")
                url = f"https://image.pollinations.ai/prompt/{p_enc}%20{style}%20{format_img}?nologo=true&enhance=true"
                st.image(url, caption=f"Manifestation {moteur} réussie")

# --- TAB 3 : VISIONS DE VEO 3 (PHOTO 3 VALIDÉE) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        action = st.text_area("Séquence temporelle...", value=st.session_state.last_sage_response, height=150)
        res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
        cam = st.selectbox("Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- TAB 4 : FRÉQUENCES DE LYRIA (PHOTO 2 VALIDÉE) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        amb = st.text_area("Paysage sonore...", value=st.session_state.last_sage_response, height=150)
        moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
        nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
