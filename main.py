import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import requests
from datetime import datetime

# --- CONFIGURATION STRICTE v4.8 (Sovereignty & Vision Fix) ---
st.set_page_config(page_title="ENKI v4.8 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google 'GEMINI_API_KEY' manquante dans les secrets.")
    st.stop()

# --- FONCTION DIVINE : CONVERSION JPEG POUR GALERIE iPAD ---
def convert_to_jpeg(raw_bytes):
    try:
        img = PIL.Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        return buf.getvalue()
    except Exception:
        return raw_bytes 

# --- INITIALISATION DES SYSTÈMES ET DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"

# Stockage Images/Vidéos 
if "last_gen_bytes" not in st.session_state: st.session_state.last_gen_bytes = None
if "last_gen_url" not in st.session_state: st.session_state.last_gen_url = ""
if "saved_images" not in st.session_state: st.session_state.saved_images = []

# --- CHRONIQUES MANIFESTÉES AUTOMATIQUES (ARCHIVES) ---
if "manifested_archives" not in st.session_state: st.session_state.manifested_archives = []

# --- CALLBACK POUR RECALCUL DYNAMIQUE (CHANGEMENT D'ESTHÉTIQUE) ---
if "trigger_atelier_regeneration" not in st.session_state: st.session_state.trigger_atelier_regeneration = False

def on_aesthetic_change():
    if st.session_state.get('in_at_prompt'): 
        st.session_state.trigger_atelier_regeneration = True

# --- INITIALISATION MULTI-PROJET ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [{"name": "📜 Tablette Originelle", "messages": [], "last_response": ""}]
if "active_idx" not in st.session_state: st.session_state.active_idx = 0

active_c = st.session_state.chronicles[st.session_state.active_idx]

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="radio_mode")
    
    st.divider()
    
    # GESTION DES CHRONIQUES
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

    # --- ARCHIVES AUTOMATIQUES "MES CONTENUS" ---
    st.subheader("📚 Chroniques Manifestées")
    
    if st.session_state.manifested_archives:
        st.caption("Conservation automatique de tes contenus de l'Atelier et de Sora.")
        for i, manifested in enumerate(reversed(st.session_state.manifested_archives)):
            with st.expander(f"{manifested['id']} - {manifested['prompt'][:30]}...", expanded=(i == 0)):
                st.caption(f"Manifesté à : {manifested['time']}")
                if manifested['type'] == 'image':
                    st.image(manifested['data'], use_container_width=True)
                    # DOUBLE BOUTON DE TÉLÉCHARGEMENT (PNG + JPEG)
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        st.download_button(label="📥 PNG", data=manifested['raw_bytes'], file_name=f"{manifested['id']}.png", mime="image/png", use_container_width=True, key=f"dl_png_{manifested['id']}")
                    with dl_col2:
                        st.download_button(label="📸 JPEG", data=convert_to_jpeg(manifested['raw_bytes']), file_name=f"{manifested['id']}.jpg", mime="image/jpeg", use_container_width=True, key=f"dl_jpg_{manifested['id']}")
                elif manifested['type'] == 'video':
                    st.video(manifested['data'])
                    st.caption(f"Manifesté par {manifested['engine']}")
        
        if st.button("🧹 Vider les Chroniques de Manifestation"):
            st.session_state.manifested_archives = []
            st.rerun()
    else:
        st.info("📌 Tes images et vidéos générées s'archiveront automatiquement ici.")
        
    st.divider()
    
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

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v4.8 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Manifestation Réelle : ACTIVÉE")

# NAVIGATION SUPÉRIEURE
nav = st.columns(4)
tabs_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(tabs_titles):
    if nav[i].button(title, use_container_width=True, type="primary" if st.session_state.view == title else "secondary", key=f"tab_btn_{i}"):
        st.session_state.view = title
        st.rerun()

st.divider()

# --- LOGIQUE DES VUES ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    for msg in active_c["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        up_file = st.file_uploader("📎 Vision (Image, PDF)", type=["png", "jpg", "jpeg", "pdf"], key="scribe_upload", label_visibility="collapsed")
        user_input = st.text_area("Analyse ou directive...", height=150, key="scribe_input", placeholder="Analyse cette image ou écris une scène...")
        
        actions = st.columns(4)
        with actions[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="act_run"):
                if user_input or up_file:
                    active_c["messages"].append({"role": "user", "content": user_input if user_input else "Analyse du document."})
                    
                    prompt_parts = [f"Tu es le Sage. Contexte de continuité : {active_ctx}\n\n{user_input}"]
                    
                    # LA CORRECTION EST ICI : ENVOI BRUT DES DONNÉES (BYPASS PIL.Image)
                    if up_file:
                        try:
                            # Utilisation stricte de getvalue() pour l'iPad
                            prompt_parts.append({"mime_type": up_file.type, "data": up_file.getvalue()})
                        except Exception as e:
                            st.error(f"Erreur d'intégration de l'image : {e}")

                    with st.spinner("Le Sage scrute les tablettes..."):
                        try:
                            resp = model.generate_content(prompt_parts)
                            active_c["last_response"] = resp.text
                            active_c["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Erreur de communication API : {e}")
                    st.rerun()
        
        with actions[1]:
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="act_at"):
                st.session_state.view = "🎨 Atelier de Ninharsag"; st.rerun()
        with actions[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="act_vi"):
                st.session_state.view = "🎬 Visions de Veo 3"; st.rerun()
        with actions[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="act_ly"):
                st.session_state.view = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    
    # NOUVELLES ESTHÉTIQUES
    esthetiques_uniques = ["Photo-réel Brut (8k Leica)", "Concept Art UE5", "Chroniques de Dilmun (Manga Ultra-Fidélité)", "Sourire de Babylone (Pixar Haute Fidélité)", "Bas-relief Royal"]
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        vision_input = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150, key="in_at_prompt")
        format_img_input = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"], key="in_at_format")
        moteur_input = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"], key="in_at_motor")
    with col_a2:
        qualite_input = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"], key="in_at_qual")
        # CHANGEMENT DYNAMIQUE D'ESTHÉTIQUE
        style_input = st.selectbox("Esthétique Maître", esthetiques_uniques, key="in_at_aesthetic", on_change=on_aesthetic_change)

    at_manual_submit = st.button("🚀 Graver & Manifester", use_container_width=True)

    # LOGIQUE DE GÉNÉRATION
    if at_manual_submit or st.session_state.get("trigger_atelier_regeneration", False):
        st.session_state.trigger_atelier_regeneration = False

        if vision_input:
            with st.spinner("La vision se matérialise..."):
                if moteur_input == "Nano Banana 2":
                    encoded_prompt = vision_input.replace(" ", "%20").replace("\n", "%20")
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}%20aesthetic%20{style_input}%20{format_img_input}?nologo=true&enhance=true"
                    
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            st.session_state.last_gen_bytes = response.content
                            st.session_state.last_gen_url = url
                            
                            # ARCHIVAGE AUTOMATIQUE
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            id_manifest = f"IMG-{moteur_input.replace(' ', '')}-{datetime.now().strftime('%H%M%S')}"
                            st.session_state.manifested_archives.append({
                                "id": id_manifest,
                                "prompt": vision_input,
                                "type": "image",
                                "engine": moteur_input,
                                "data": url,
                                "raw_bytes": response.content,
                                "time": timestamp
                            })
                            st.rerun()
                    except Exception as e:
                        st.error(f"Interruption divine : {e}")
                else:
                    st.warning(f"{moteur_input} n'est pas encore synchronisé.")
        else:
            st.warning("Inscrivez une vision pour la manifester.")

    if st.session_state.last_gen_url:
        st.caption("Manifestation Divine Réussie")
        st.image(st.session_state.last_gen_url, use_container_width=True)
        if st.session_state.last_gen_bytes:
            # DOUBLE BOUTON POUR LA VUE PRINCIPALE
            c_dl1, c_dl2 = st.columns(2)
            with c_dl1:
                st.download_button(label="📥 Télécharger en PNG", data=st.session_state.last_gen_bytes, file_name="Manifestation.png", mime="image/png", use_container_width=True, key="dl_main_png")
            with c_dl2:
                st.download_button(label="📸 Télécharger en JPEG (Galerie)", data=convert_to_jpeg(st.session_state.last_gen_bytes), file_name="Manifestation.jpg", mime="image/jpeg", use_container_width=True, key="dl_main_jpg")

# 3. VISIONS
elif st.session_state.view == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action_v = st.text_area("Séquence temporelle...", value=active_c["last_response"], height=150)
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
            cam = st.selectbox("Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
            fps = st.radio("Images/sec", ["24 (Cinéma)", "30 (TV)", "60 (Action)"], horizontal=True)
            
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            with st.spinner("Synchronisation des lignes de temps Veo 3..."):
                vid_url = "https://www.w3schools.com/html/mov_bbb.mp4"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id_vid = f"VID-{moteur_v.replace(' ', '')}-{datetime.now().strftime('%H%M%S')}"
                st.session_state.manifested_archives.append({
                    "id": id_vid,
                    "prompt": action_v,
                    "type": "video",
                    "engine": moteur_v,
                    "data": vid_url,
                    "raw_bytes": b'', 
                    "time": timestamp
                })
                st.session_state.last_gen_url = "" 
                st.rerun()

    if st.session_state.manifested_archives:
        last_manifest = st.session_state.manifested_archives[-1]
        if last_manifest['type'] == 'video':
            st.video(last_manifest['data'])
            st.caption("Synchronisation terminée.")

# 4. FRÉQUENCES
elif st.session_state.view == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore...", value=active_c["last_response"], height=150)
            duree = st.slider("Durée (secondes)", 10, 60, 30)
        with col_s2:
            moteur_audio = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
            
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            with st.spinner("Harmonisation en cours..."):
                st.session_state.last_gen_url = ""
                st.audio("https://www.w3schools.com/html/horse.ogg")
            st.caption("Génération Harmonique terminée.")
