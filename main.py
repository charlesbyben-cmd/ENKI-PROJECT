import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import requests
from datetime import datetime

# --- CONFIGURATION STRICTE v4.6 (Visual Sovereignty) ---
st.set_page_config(page_title="ENKI v4.6 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google 'GEMINI_API_KEY' manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DES SYSTÈMES ET DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"

# Stockage Images/Vidéos (Conservation across tabs)
if "last_gen_bytes" not in st.session_state: st.session_state.last_gen_bytes = None
if "last_gen_url" not in st.session_state: st.session_state.last_gen_url = ""
# Stockage pour Sceaux Personnels (Fichier -> URL)
if "saved_images" not in st.session_state: st.session_state.saved_images = []

# ==================================================================================================================================================
# --- NEW v4.6 : CHRONIQUES MANIFESTÉES AUTOMATIQUES (ARCHIVES) ---
# Dictionnaire : {'id': str, 'prompt': str, 'type': str (image/video), 'data': bytes/url/sim, 'time': str, 'raw_bytes': bytes (for DL)}
if "manifested_archives" not in st.session_state: st.session_state.manifested_archives = []

# --- CALLBACK FOR DYNAMIC REGEN ON AESTHETIC CHANGE ---
if "trigger_atelier_regeneration" not in st.session_state: st.session_state.trigger_atelier_regeneration = False

# Function defined before main UI to track input changes
def on_aesthetic_change():
    if st.session_state.get('in_at_prompt'): # Don't trigger on empty prompt area
        st.session_state.trigger_atelier_regeneration = True
# ==================================================================================================================================================

# --- INITIALISATION MULTI-PROJET ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [{"name": "📜 Tablette Originelle", "messages": [], "last_response": ""}]
if "active_idx" not in st.session_state: st.session_state.active_idx = 0

active_c = st.session_state.chronicles[st.session_state.active_idx]

# --- MOTEUR SAGE (NOM FIXÉ POUR ÉVITER L'ERREUR 404 NOTFOUND) ---
@st.cache_resource
def get_sage_engine():
    # Utilisation de la version stable pour garantir la vision
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO FIDÈLE) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="radio_mode")
    
    st.divider()
    
    # GESTION DES CHRONIQUES (PROJETS MULTIPLES)
    st.subheader("📜 Tablettes de Destinée")
    if st.button("➕ Nouvelle Chronique", use_container_width=True, key="new_ch"):
        st.session_state.chronicles.append({"name": f"✨ Tablette {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_idx = len(st.session_state.chronicles) - 1
        st.rerun()
    
    c_names = [c["name"] for c in st.session_state.chronicles]
    st.session_state.active_idx = st.selectbox("Charger une Tablette :", range(len(c_names)), format_func=lambda x: c_names[x], index=st.session_state.active_idx, key="sel_ch")
    
    if st.button("🗑️ Briser la Tablette Active", use_container_width=True, key="del_chron"):
        if len(st.session_state.chronicles) > 1:
            st.session_state.chronicles.pop(st.session_state.active_idx)
            st.session_state.active_idx = 0
            st.rerun()

    st.divider()

    # ==================================================================================================================================================
    # --- NEW v4.6 : SECTION ARCHIVES AUTOMATIQUES "MES CONTENUS" ---
    if st.session_state.manifested_archives:
        st.subheader("📚 Chroniques Manifestées (Archives)")
        st.caption("Conservation automatique de tes contenus de l'Atelier et de Sora.")
        # Reverse list to show newest on top
        for i, manifested in enumerate(reversed(st.session_state.manifested_archives)):
            with st.expander(f"{manifested['id']} - {manifested['prompt'][:30]}...", expanded=(i == 0)):
                st.caption(f"Manifesté à : {manifested['time']}")
                if manifested['type'] == 'image':
                    st.image(manifested['data'], use_container_width=True)
                    # Download button for bytes stored in archive
                    st.download_button(label="📥 Télécharger l'Image PNG", data=manifested['raw_bytes'], file_name=f"{manifested['id']}.png", mime="image/png", use_container_width=True, key=f"dl_arc_{manifested['id']}")
                elif manifested['type'] == 'video':
                    st.video(manifested['data'])
                    st.caption(f"Manifesté par {manifested['engine']}")
        
        if st.button("🧹 Vider les Chroniques de Manifestation"):
            st.session_state.manifested_archives = []
            st.rerun()
        st.divider()
    # ==================================================================================================================================================
    
    # SCEAUX DE PERSISTANCE
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        v_n = st.text_input("Nom de l'élément", key="v_n")
        v_d = st.text_area("Physique / Description", key="v_d")
        v_u = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="v_u")
        v_url = st.text_input("Ou URL de l'image (Lien direct)", key="v_url")
        if st.button("Graver le Sceau", key="v_b"):
            if v_n and v_d:
                st.session_state.vault.append({"name": v_n, "desc": v_d, "ref": v_u if v_u else v_url, "active": True})
                st.rerun()

    active_ctx = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"], key=f"s_c_{i}")
        if seal["active"]:
            active_ctx += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']:
                try:
                    if isinstance(seal['ref'], str) and "http" in seal['ref']: st.image(seal['ref'], width=100)
                    else: st.image(seal['ref'], width=100)
                except: st.caption("🔗 Sceau actif")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True, key="res_sys"):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG v3.5/v4.0 FIDÈLE) ---
st.title("🏛️ ENKI v4.0 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Manifestation Réelle : ACTIVÉE")

# NAVIGATION SUPÉRIEURE (Les 4 Onglets - BOUTONS LARGES)
nav = st.columns(4)
tabs_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(tabs_titles):
    if nav[i].button(title, use_container_width=True, type="primary" if st.session_state.view == title else "secondary", key=f"tab_btn_{i}"):
        st.session_state.view = title
        st.rerun()

st.divider()
active_chron = st.session_state.chronicles[st.session_state.active_idx]

# --- LOGIQUE DES VUES ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    # Display message history of the ACTIVE chronicle
    for msg in active_chron["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        # ZONE ANALYSE (Upload)
        up_file = st.file_uploader("📎 Vision (Image, PDF)", type=["png", "jpg", "jpeg", "pdf"], key="scribe_upload", label_visibility="collapsed")
        
        user_input = st.text_area("Analyse ou directive...", height=150, key="scribe_input", placeholder="Analyse cette image ou écris une scène...")
        
        # BOUTONS DU BAS (SYMETRIE DIVINE)
        actions = st.columns(4)
        with actions[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="act_run"):
                if user_input or up_file:
                    active_chron["messages"].append({"role": "user", "content": user_input if user_input else "Analyse du document."})
                    
                    # Construction du prompt
                    prompt_parts = [f"Tu es le Sage. Contexte de continuité : {active_ctx}\n\n{user_input}"]
                    if up_file:
                        if up_file.type.startswith("image/"):
                            img = PIL.Image.open(up_file)
                            prompt_parts.append(img)
                        else:
                            # Gemini handles PDF/Text data
                            prompt_parts.append({"mime_type": up_file.type, "data": up_file.read()})

                    with st.spinner("Le Sage scrute les tablettes..."):
                        try:
                            resp = model.generate_content(prompt_parts)
                            active_chron["last_response"] = resp.text
                            active_chron["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Erreur de communication API (Forte affluence?) : {e}")
                    st.rerun()
        
        # Les boutons copies conformes du haut pour navigation
        with actions[1]:
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="act_at"):
                st.session_state.view = "🎨 Atelier de Ninharsag"; st.rerun()
        with actions[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="act_vi"):
                st.session_state.view = "🎬 Visions de Veo 3"; st.rerun()
        with actions[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="act_ly"):
                st.session_state.view = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER (image_2.png)
# ==================================================================================================================================================
# --- REFACTORED FOR DYNAMIC REGEN ON AESTHETIC CHANGE ---
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    
    # --------------------------------------------------------------------------------------------------------------------------------------------------
    # RESTORATION ESTHÉTIQUE MANGA / AJOUT PIXAR HAUTE FIDÉLITÉ (v4.6)
    esthetiques_uniques = ["Photo-réel Brut (8k Leica Leica)", "Concept Art UE5", "Chroniques de Dilmun (Manga Ultra-Fidélité Leica)", "Sourire de Babylone (Pixar Haute Fidélité)", "Bas-relief Royal"]
    
    #Inputs NO LONGER inside st.form to allow dynamic reactivity
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        vision_input = st.text_area("Vision à matérialiser...", value=active_chron["last_response"], height=150, key="in_at_prompt")
        format_img_input = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"], key="in_at_format")
        moteur_input = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"], key="in_at_motor")
    with col_a2:
        qualite_input = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"], key="in_at_qual")
        
        # NEW v4.6 : Selectbox uses callback to trigger instant regen on change
        style_input = st.selectbox("Esthétique Maître", esthetiques_uniques, key="in_at_aesthetic", on_change=on_aesthetic_change)

    at_manual_submit = st.button("🚀 Graver & Manifester (Submit)", use_container_width=True)

    # UNIFIED GENERATION LOGIC (Triggered by manual button OR dynamic aesthetic change callback)
    if at_manual_submit or st.session_state.get("trigger_atelier_regeneration", False):
        # Reset callback flag
        st.session_state.trigger_atelier_regeneration = False
        
        # Use values currently in st.session_state (mapped via keys)
        current_vision = vision_input
        current_style = style_input
        current_format = format_img_input
        current_moteur = moteur_input
        current_qual = qualite_input

        if current_vision:
            with st.spinner("La vision se matérialise..."):
                if current_moteur == "Nano Banana 2":
                    encoded_prompt = current_vision.replace(" ", "%20").replace("\n", "%20")
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}%20aesthetic%20{current_style}%20{current_format}?nologo=true&enhance=true"
                    
                    try:
                        # 1. Fetch Bytes directly
                        response = requests.get(url)
                        if response.status_code == 200:
                            st.session_state.last_gen_bytes = response.content
                            st.session_state.last_gen_url = url
                            
                            # ==================================================================================================================================================
                            # --- NEW v4.6 : ARCHIVAGE AUTOMATIQUE ---
                            # timestamp and ID for uniqueness
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            id_manifest = f"IMG-{current_moteur.replace(' ', '')}-{datetime.now().strftime('%H%M%S')}"
                            st.session_state.manifested_archives.append({
                                "id": id_manifest,
                                "prompt": current_vision,
                                "type": "image",
                                "engine": current_moteur,
                                "data": url,
                                "raw_bytes": response.content,
                                "time": timestamp
                            })
                            # Clear current saved state to prevent old DL buttons appearing? No, keep it.
                            # rerunning will refresh sidebar with new archive item
                            st.rerun()
                    except Exception as e:
                        st.error(f"Interruption divine : {e}")
                else:
                    st.warning(f"{current_moteur} n'est pas encore synchronisé pour le recalcul instantané.")
        else:
            st.warning("Inscrivez une vision au scribe pour la manifester.")

    # Affichage du résultat actuel (si existant)
    if st.session_state.last_gen_url:
        st.caption("Manifestation Divine Réussie (Détentrice du ME : Ninharsag)")
        st.image(st.session_state.last_gen_url, use_container_width=True)
        # Sceaux bouton (manual manual favorites list kept separate from archives list)
        if st.button("📁 Graver dans les Sceaux Personnels Abzu (Sauvegarde Manuelle)", use_container_width=True, key="save_fav"):
            st.session_state.saved_images.append(st.session_state.last_gen_url)
            st.toast("Ajouté aux Sceaux personnels d'Abzu")
        # Download button uses session state bytes
        if st.session_state.last_gen_bytes:
            st.download_button(label="📥 Télécharger la Manifestation PNG", data=st.session_state.last_gen_bytes, file_name="Manifestation.png", mime="image/png", use_container_width=True, key="dl_main_at")

# ==================================================================================================================================================

# 3. VISIONS (image_3.png)
elif st.session_state.view == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action_v = st.text_area("Séquence temporelle...", value=active_chron["last_response"], height=150)
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
            cam = st.selectbox("Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
            fps = st.radio("Images/sec", ["24 (Cinéma)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            with st.spinner("Synchronisation des lignes de temps Veo 3..."):
                # Simulation (pas de recalcul instantané en vidéo pour l'instant)
                
                # ==================================================================================================================================================
                # --- NEW v4.6 : ARCHIVAGE AUTOMATIQUE VIDÉO ---
                vid_url = "https://www.w3schools.com/html/mov_bbb.mp4" # Simulated data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id_vid = f"VID-{moteur_v.replace(' ', '')}-{datetime.now().strftime('%H%M%S')}"
                st.session_state.manifested_archives.append({
                    "id": id_vid,
                    "prompt": action_v,
                    "type": "video",
                    "engine": moteur_v,
                    "data": vid_url,
                    "raw_bytes": b'', # no bytes for video simulation download, display placeholder
                    "time": timestamp
                })
                # clear saved state for other tab
                st.session_state.last_gen_url = "" 
                # ==================================================================================================================================================
                st.rerun()

    # Display simulated result (from archives or logic)
    # Check newest archive if video simulation just happened
    if st.session_state.manifested_archives:
        last_manifest = st.session_state.manifested_archives[-1]
        if last_manifest['type'] == 'video':
            st.video(last_manifest['data'])
            st.caption("Synchronisation du ME Veo 3 terminée.")

# 4. FRÉQUENCES (image_4.png)
elif st.session_state.view == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore...", value=active_chron["last_response"], height=150)
            duree = st.slider("Durée (secondes)", 10, 60, 30)
        with col_s2:
            moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
            
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            with st.spinner("Harmonisation des ME musicaux..."):
                # no automated archives logic here as no simulation bytes/data extracted.
                
                # Clear existing image state from other tabs
                st.session_state.last_gen_url = ""
                st.audio("https://www.w3schools.com/html/horse.ogg")
            st.caption("Génération Harmonique terminée (ME de Lyria).")
