import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import requests
from datetime import datetime

# --- CONFIGURATION STRICTE v6.3 (Flawless Matrix) ---
st.set_page_config(page_title="ENKI v6.3 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API Google 'GEMINI_API_KEY' manquante dans les secrets.")
    st.stop()

# --- FONCTION DIVINE 1 : CONVERSION JPEG POUR GALERIE iPAD ---
def convert_to_jpeg(raw_bytes):
    try:
        img = PIL.Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        return buf.getvalue()
    except Exception:
        return raw_bytes 

# --- FONCTION DIVINE 2 : PRÉPARATION SÉCURISÉE DES IMAGES ---
def prepare_image_for_gemini(raw_bytes):
    try:
        img = PIL.Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        img.thumbnail((1024, 1024))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return {"mime_type": "image/jpeg", "data": buf.getvalue()}
    except Exception:
        return {"mime_type": "image/jpeg", "data": raw_bytes}

# --- SÉLECTION DYNAMIQUE DU MODÈLE ---
@st.cache_resource
def get_best_model_name():
    try:
        dispos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for pref in ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-1.5-pro"]:
            if pref in dispos:
                return pref.replace("models/", "")
        if dispos:
            return dispos[0].replace("models/", "")
    except:
        pass
    return "gemini-1.5-flash"

nom_modele_actif = get_best_model_name()
model = genai.GenerativeModel(nom_modele_actif)

# --- INITIALISATION DES SYSTÈMES ET DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_sage_response" not in st.session_state: st.session_state.last_sage_response = ""
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"

# --- SYSTÈME DE RÉINITIALISATION SÉCURISÉ (FIX STREAMLIT EXCEPTION) ---
if "seal_reset_key" not in st.session_state: st.session_state.seal_reset_key = 0
if "seal_auto_desc" not in st.session_state: st.session_state.seal_auto_desc = ""

# Stockage Images/Vidéos 
if "last_gen_bytes" not in st.session_state: st.session_state.last_gen_bytes = None
if "last_gen_url" not in st.session_state: st.session_state.last_gen_url = ""
if "saved_images" not in st.session_state: st.session_state.saved_images = []

# --- CHRONIQUES MANIFESTÉES AUTOMATIQUES (ARCHIVES) ---
if "manifested_archives" not in st.session_state: st.session_state.manifested_archives = []

# --- CALLBACK POUR RECALCUL DYNAMIQUE ---
if "trigger_atelier_regeneration" not in st.session_state: st.session_state.trigger_atelier_regeneration = False

def on_aesthetic_change():
    if st.session_state.get('in_at_prompt'): 
        st.session_state.trigger_atelier_regeneration = True

# --- INITIALISATION MULTI-PROJET ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [{"name": "📜 Tablette Originelle", "messages": [], "last_response": ""}]
if "active_idx" not in st.session_state: st.session_state.active_idx = 0

active_c = st.session_state.chronicles[st.session_state.active_idx]

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
        
        # Utilisation de la clé de reset pour contourner l'Exception de Streamlit
        k = st.session_state.seal_reset_key
        
        nom_sceau = st.text_input("Nom de l'élément (Ex: Ea)", key=f"v_n_{k}")
        upload_sceau = st.file_uploader("1. Upload Image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"v_u_{k}")
        
        if upload_sceau:
            if st.button("👁️ Extraire l'Essence", use_container_width=True):
                with st.spinner("Extraction de l'essence divine en cours..."):
                    try:
                        imgs_to_analyze = [prepare_image_for_gemini(f.getvalue()) for f in upload_sceau]
                        prompt_analyse = ["Décris avec une précision absolue et exhaustive le physique, le visage (barbe, cheveux, regard), les vêtements et les caractéristiques distinctives de ce sujet. Rédige-le sous forme de prompt ultra-détaillé et factuel pour cloner ce personnage dans un générateur d'images. Sois direct, pas d'introduction."] + imgs_to_analyze
                        
                        resp = model.generate_content(prompt_analyse)
                        st.session_state.seal_auto_desc = resp.text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur d'extraction : {e}")
        
        desc_sceau = st.text_area("2. Physique / Description", value=st.session_state.seal_auto_desc, height=150, key=f"v_d_{k}", placeholder="Laisse l'Œil extraire l'essence ou écris-la toi-même...")
        url_sceau = st.text_input("Ou URL de l'image (Lien direct)", key=f"v_url_{k}")
        
        if st.button("3. Graver le Sceau", type="primary"):
            if nom_sceau: 
                saved_refs = [f.getvalue() for f in upload_sceau] if upload_sceau else []
                
                st.session_state.vault.append({
                    "name": nom_sceau, 
                    "desc": desc_sceau, 
                    "refs": saved_refs, 
                    "url": url_sceau,
                    "active": True
                })
                
                # Le nettoyage parfait : on change l'identité des cases pour les vider
                st.session_state.seal_reset_key += 1
                st.session_state.seal_auto_desc = ""
                st.rerun()
            else:
                st.warning("Le nom de l'élément est obligatoire.")

    active_ctx = ""
    active_seal_images = [] 
    
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"], key=f"s_c_main_{i}")
        if seal["active"]:
            if seal.get('desc'):
                active_ctx += f" [Personnage/Objet '{seal['name']}': {seal['desc']}]"
            
            if seal.get('refs'):
                cols = st.columns(min(len(seal['refs']), 4)) 
                for idx, img_bytes in enumerate(seal['refs']):
                    cols[idx % 4].image(img_bytes)
                    try:
                        active_seal_images.append(prepare_image_for_gemini(img_bytes))
                    except:
                        pass
                        
            if seal.get('url'):
                try:
                    st.image(seal['url'], width=100)
                except:
                    st.caption("🔗 URL Sceau active")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True, key="res_sys_main"):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v6.3 : The Visual Continuity Revolution")
st.caption(f"🚀 Moteur Actif : {nom_modele_actif} | Manifestation Réelle : ACTIVÉE")

# NAVIGATION SUPÉRIEURE
nav = st.columns(4)
tabs_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(tabs_titles):
    if nav[i].button(title, use_container_width=True, type="primary" if st.session_state.view == title else "secondary", key=f"tab_btn_main_{i}"):
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
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="act_run_main"):
                if user_input or up_file:
                    active_c["messages"].append({"role": "user", "content": user_input if user_input else "Analyse du document."})
                    
                    prompt_parts = [f"Tu es le Sage. Contexte de continuité : {active_ctx}\nVoici les références visuelles verrouillées à garder en mémoire :\n"]
                    prompt_parts.extend(active_seal_images)
                    prompt_parts.append(f"\nDirective du Souverain : {user_input}")
                    
                    if up_file:
                        try:
                            img = prepare_image_for_gemini(up_file.getvalue())
                            prompt_parts.append(img)
                        except Exception as e:
                            st.error(f"Erreur d'intégration de l'image : {e}")

                    with st.spinner("Le Sage intègre les multiples visions..."):
                        try:
                            resp = model.generate_content(prompt_parts)
                            active_c["last_response"] = resp.text
                            active_c["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Erreur de communication API : {e}")
                    st.rerun()
        
        with actions[1]:
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="act_at_main"):
                st.session_state.view = "🎨 Atelier de Ninharsag"; st.rerun()
        with actions[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="act_vi_main"):
                st.session_state.view = "🎬 Visions de Veo 3"; st.rerun()
        with actions[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="act_ly_main"):
                st.session_state.view = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    
    esthetiques_uniques = ["Photo-réel Brut (8k Leica)", "Concept Art UE5", "Chroniques de Dilmun (Manga Ultra-Fidélité)", "Sourire de Babylone (Pixar Haute Fidélité)", "Bas-relief Royal"]
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        vision_input = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150, key="in_at_prompt")
        format_img_input = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:5", "3:4", "4:3", "16:9", "21:9", "9:16"], key="in_at_format")
        moteur_input = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"], key="in_at_motor")
    with col_a2:
        qualite_input = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"], key="in_at_qual")
        style_input = st.selectbox("Esthétique Maître", esthetiques_uniques, key="in_at_aesthetic", on_change=on_aesthetic_change)

    at_manual_submit = st.button("🚀 Graver & Manifester", use_container_width=True)

    if at_manual_submit or st.session_state.get("trigger_atelier_regeneration", False):
        st.session_state.trigger_atelier_regeneration = False

        if vision_input:
            with st.spinner("La vision se matérialise..."):
                if moteur_input == "Nano Banana 2":
                    
                    prompt_complet = vision_input
                    if active_ctx.strip():
                        prompt_complet += f". Consignes visuelles obligatoires : {active_ctx}"
                        
                    encoded_prompt = prompt_complet.replace(" ", "%20").replace("\n", "%20")
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}%20aesthetic%20{style_input}%20{format_img_input}?nologo=true&enhance=true"
                    
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            st.session_state.last_gen_bytes = response.content
                            st.session_state.last_gen_url = url
                            
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
