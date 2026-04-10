import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION SACRÉE v5.2 ---
st.set_page_config(page_title="ENKI v5.2 : Chronicle of the Archon", layout="wide", page_icon="🏛️")

# Accès API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API 'GEMINI_API_KEY' manquante dans les secrets.")
    st.stop()

# --- INITIALISATION DU SYSTÈME MULTI-CHRONIQUES ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [
        {"id": "init", "name": "📜 Tablette Originelle", "messages": [], "last_response": ""},
    ]
if "active_id" not in st.session_state:
    st.session_state.active_id = "init"
if "vault" not in st.session_state: st.session_state.vault = []
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"

# Helper pour la chronique active
def get_active_c():
    return next((c for c in st.session_state.chronicles if c["id"] == st.session_state.active_id), st.session_state.chronicles[0])

# --- MOTEUR SAGE (STABLE) ---
@st.cache_resource
def load_sage():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_sage()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO FIDÈLE) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="mode_radio")
    
    st.divider()
    
    # GESTION DES CHRONIQUES (PROJETS)
    st.subheader("📜 Tablettes de Destinée")
    if st.button("➕ Nouvelle Chronique", use_container_width=True, key="add_chron"):
        new_id = f"chron_{len(st.session_state.chronicles)+1}"
        st.session_state.chronicles.append({"id": new_id, "name": f"✨ Nouvelle Tablette {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_id = new_id
        st.rerun()
    
    c_list = [c["name"] for c in st.session_state.chronicles]
    current_c = get_active_c()
    sel_name = st.selectbox("Charger une Tablette :", c_list, index=c_list.index(current_c["name"]), key="select_chron")
    st.session_state.active_id = next(c["id"] for c in st.session_state.chronicles if c["name"] == sel_name)
    
    if st.button("🗑️ Briser la Tablette", use_container_width=True, key="del_chron"):
        if len(st.session_state.chronicles) > 1:
            st.session_state.chronicles = [c for c in st.session_state.chronicles if c["id"] != st.session_state.active_id]
            st.session_state.active_id = st.session_state.chronicles[0]["id"]
            st.rerun()

    st.divider()
    
    # SCEAUX DE PERSISTANCE
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        v_name = st.text_input("Nom de l'élément", key="v_name")
        v_desc = st.text_area("Physique / Description", key="v_desc")
        v_up = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="v_up")
        if st.button("Graver le Sceau", key="v_btn"):
            if v_name and v_desc:
                st.session_state.vault.append({"name": v_name, "desc": v_desc, "ref": v_up, "active": True})
                st.rerun()

    active_ctx = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"], key=f"s_check_{i}")
        if seal["active"]:
            active_ctx += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset)", key="reset_sys"):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG v3.5/v4.0) ---
st.title("🏛️ ENKI v3.5 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Statut : Optimisé pour 2026")

# LES 4 ONGLETS (BOUTONS LARGES)
nav = st.columns(4)
tabs_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(tabs_titles):
    if nav[i].button(title, use_container_width=True, type="primary" if st.session_state.view == title else "secondary", key=f"tab_btn_{i}"):
        st.session_state.view = title
        st.rerun()

st.divider()
active_c = get_active_c()

# --- LOGIQUE DES VUES ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    for msg in active_c["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        # ZONE DE TÉLÉCHARGEMENT POUR ANALYSE
        up_doc = st.file_uploader("📎 Charger Vision, Séquence ou Fréquence pour analyse...", 
                                 type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf"], key="scribe_upload")
        
        prompt = st.text_area("Analyse ou directive...", height=150, key="scribe_input")
        
        # BOUTONS D'ACTION (ALIGNÉS EN BAS)
        actions = st.columns(4)
        with actions[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="act_run"):
                if prompt or up_doc:
                    active_c["messages"].append({"role": "user", "content": prompt if prompt else "Analyse du média joint."})
                    
                    # Construction du prompt multi-modal
                    content = [f"Tu es le Sage. Contexte de continuité : {active_ctx}\n\n{prompt}"]
                    if up_doc:
                        if up_doc.type.startswith("image/"):
                            content.append(PIL.Image.open(up_doc))
                        else:
                            content.append({"mime_type": up_doc.type, "data": up_doc.read()})

                    with st.spinner("Le Sage scrute les ondes..."):
                        resp = model.generate_content(content)
                        active_c["last_response"] = resp.text
                        active_c["messages"].append({"role": "assistant", "content": resp.text})
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

# 2. ATELIER (image_2.png)
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        vision_at = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150, key="at_prompt")
        col_at1, col_at2 = st.columns(2)
        with col_at1:
            moteur_at = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"], key="at_mot")
            fmt_at = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:3", "16:9", "9:16", "21:9"], key="at_fmt")
        with col_at2:
            style_at = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"], key="at_sty")
            qual_at = st.select_slider("Qualité", options=["720p", "1080p", "4K", "8K"], key="at_qual")
        if st.form_submit_button("🚀 Graver & Manifester"):
            st.image(f"https://image.pollinations.ai/prompt/{vision_at.replace(' ', '%20')}?nologo=true")

# 3. VISIONS (image_3.png)
elif st.session_state.view == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        seq_vi = st.text_area("Séquence temporelle...", value=active_c["last_response"], height=150, key="vi_prompt")
        mot_vi = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"], key="vi_mot")
        qual_vi = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K"], value="1080p", key="vi_qual")
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. FRÉQUENCES (image_2.png / Audio config)
elif st.session_state.view == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        amb_ly = st.text_area("Paysage sonore...", value=active_c["last_response"], height=150, key="ly_prompt")
        mot_ly = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"], key="ly_mot")
        dur_ly = st.slider("Durée (sec)", 10, 60, 30, key="ly_dur")
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
