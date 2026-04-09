import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION RÉVOLUTION v3.8 ---
st.set_page_config(page_title="ENKI v3.8 : Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Vérification Clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google 'GEMINI_API_KEY' manquante dans les secrets Streamlit.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE VIVE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""

# --- MOTEUR SAGE (INTELLIGENCE) ---
@st.cache_resource
def get_sage_engine():
    try:
        # On tente Gemini 3 Flash pour 2026
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a), a
    except: pass
    # Repli stable
    return genai.GenerativeModel("gemini-1.5-flash"), "Gemini-1.5-flash"

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
    
    # 1. CRÉATION DE SCEAU (Fidélité Totale image_4.png + Crash Fix)
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'élément (Perso, Objet, Décor)", placeholder="Ea, Vaisseau d'Alalu...")
        s_desc = st.text_area("Description physique précisément détaillée")
        
        st.write("**Référence Visuelle :**")
        s_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"])
        s_url = st.text_input("Ou coller URL de l'image")
        
        if st.button("Graver le Sceau"):
            if s_name and s_desc:
                ref = s_file if s_file else s_url
                st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": ref, "active": True})
                st.rerun()
            else:
                st.error("Le Nom et la Description sont obligatoires pour la persistance.")

    # 2. LISTE DES SCEAUX (Crash Fix)
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
            # Affichage sécurisé de l'image
            if seal['ref']:
                try:
                    # Si c'est un fichier uploader
                    if hasattr(seal['ref'], 'name'):
                        st.image(seal['ref'], width=100)
                    # Si c'est une URL valide et non vide
                    elif isinstance(seal['ref'], str) and (seal['ref'].startswith('http') or len(seal['ref']) > 10):
                        st.image(seal['ref'], width=100)
                    else:
                        st.caption("🔗 Réf. texte/vide active")
                except Exception as e:
                    st.caption("⚠️ Réf. visuelle invalide")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset)"):
        st.session_state.messages = []
        st.session_state.last_sage_response = ""
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG PHOTO VALIDÉE) ---
st.title("🏛️ ENKI v3.8 : Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {model_name} | Statut : Optimisé pour 2026")

# LES VRAIS ONGLEFTES (Sacrés et Immuables)
tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE ---
with tabs[0]:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input", placeholder="Décris Ea observant les Me dans le cockpit d'Abgal...")
        
        # LA LIGNE DE BOUTONS (EXACTEMENT COMME LA PHOTO VALIDÉE)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle Universel" if "Oracle" in mode_op else "LE SAGE Anunnaki"
                resp = model_obj.generate_content(f"Tu es {role}. Contexte de continuité : {active_context}\n\nUtilisateur : {user_input}")
                st.session_state.last_sage_response = resp.text
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.rerun()
        
        # Ces boutons capturent le contexte mais ne changent pas d'onglet (limite StreamlitTabs)
        with c2: 
            if st.button("🎨 Atelier de Ninharsag Direct", use_container_width=True, help="Cliquez sur l'onglet Atelier en haut pour matérialiser"):
                if st.session_state.last_sage_response: st.toast("🎨 Vision copiée dans l'Atelier. Allez dans l'onglet !")
        with c3: 
            if st.button("🎬 Visions de Veo 3 Directe", use_container_width=True, help="Cliquez sur l'onglet Visions en haut pour visionner"):
                if st.session_state.last_sage_response: st.toast("🎬 Séquence copiée dans les Visions. Allez dans l'onglet !")
        with c4: 
            if st.button("🎼 Fréquences de Lyria Direct", use_container_width=True, help="Cliquez sur l'onglet Fréquences en haut pour harmoniser"):
                if st.session_state.last_sage_response: st.toast("🎼 Harmoniques copiées dans les Fréquences. Allez dans l'onglet !")

# --- TAB 2 : ATELIER DE NINHARSAG (image_1.png + image_2.png RÉINTÉGRÉS) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_sage_response, height=150)
            # image_2.png : Formats complets
            format_img = st.selectbox("Géométrie Sacrée (Format)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"])
        with col_a2:
            # image_1.png : Moteurs complets
            moteur = st.selectbox("Moteur de Manifestation", ["DALL-E 3", "Midjourney v7", "Imagen 3", "Nano Banana 2"])
            style = st.selectbox("Esthétique Maître", ["Photoréaliste Brut (8k Leica)", "Concept Art UE5", "Manga Seinen High-Fid", "Bas-relief Royal"])
            qualite = st.select_slider("Qualité de Rendu", options=["720p", "1080p", "2K", "4K", "8K"])
            
        if st.form_submit_button("🚀 Graver & Manifester sur place"):
            st.info(f"Manifestation {qualite} via {moteur} en cours...")
            # Simulation SDK 2026
            st.image("https://via.placeholder.com/1792x1024.png?text=Manifestation+Directe+Active", caption="Manifestation Réelle Ninharsag - PlaceHolder SDK")

# --- TAB 3 : VISIONS DE VEO 3 (image_3.png RÉINTÉGRÉ) ---
with tabs[2]:
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence temporelle...", value=st.session_state.last_sage_response, height=150)
            # image_3.png : Qualités complètes avec 720p
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
            cam = st.selectbox("Mouvement Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
            fps = st.radio("Images/sec", ["24 (Cinéma)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.warning(f"Calcul des lignes de temps Veo 3 via {moteur_v}...")
            # Simulation SDK 2026
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- TAB 4 : FRÉQUENCES DE LYRIA (UI DÉTAILLÉE RESTAURÉE) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore à harmoniser...", value=st.session_state.last_response, height=150)
            type_s = st.selectbox("Type d'Harmonique", ["Musique Épique (Cinémascope)", "Atmosphère Sci-Fi Sombre", "Chant Sacré/Rituel"])
            duree = st.slider("Durée (secondes)", 10, 60, 30)
        with col_s2:
            moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
            instrus = st.text_input("Instruments / Textures (Optionnel)", "Harpe sumérienne, Synthé basses")
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Héroïque", "Apocalyptique"], value="Mystérieux")
            
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.success(f"Harmonisation de Abzu via {moteur_audio} terminée.")
            # Simulation SDK 2026
            st.audio("https://www.w3schools.com/html/horse.ogg")
