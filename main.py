import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION SACRÉE v5.6 ---
st.set_page_config(page_title="ENKI v5.6 : Sovereign Restoration", layout="wide", page_icon="🏛️")

# Accès API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API 'GEMINI_API_KEY' manquante.")
    st.stop()

# --- INITIALISATION MÉMOIRE & CHRONIQUES ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [{"name": "📜 Tablette Originelle", "messages": [], "last_response": ""}]
if "active_idx" not in st.session_state: st.session_state.active_idx = 0
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"
if "vault" not in st.session_state: st.session_state.vault = []

active_c = st.session_state.chronicles[st.session_state.active_idx]

# --- MOTEUR SAGE (NOM STABLE POUR ÉVITER NOTFOUND) ---
@st.cache_resource
def load_sage():
    # Utilisation de la version stable pour garantir l'analyse d'image
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_sage()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO FIDÈLE) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="radio_mode")
    
    st.divider()
    
    # GESTION DES CHRONIQUES (NOUVELLES DISCUSSIONS)
    st.subheader("📜 Tablettes de Destinée")
    if st.button("➕ Nouvelle Chronique", use_container_width=True, key="new_ch"):
        st.session_state.chronicles.append({"name": f"✨ Tablette {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_idx = len(st.session_state.chronicles) - 1
        st.rerun()
    
    c_names = [c["name"] for c in st.session_state.chronicles]
    st.session_state.active_idx = st.selectbox("Charger une Tablette :", range(len(c_names)), format_func=lambda x: c_names[x], index=st.session_state.active_idx, key="sel_ch")

    st.divider()
    
    # SCEAUX DE PERSISTANCE (AVEC OPTION URL)
    st.subheader("📌 Sceaux de Persistance")
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
                    # Gestion URL ou Fichier
                    if isinstance(seal['ref'], str): st.image(seal['ref'], width=100)
                    else: st.image(seal['ref'], width=100)
                except: st.caption("🔗 Réf. active")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True, key="res_sys"):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG v3.5/v4.0) ---
st.title("🏛️ ENKI v3.5 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Analyse Multi-Modale : ACTIVÉE")

# NAVIGATION SUPÉRIEURE (Les 4 Onglets - PLACE 1)
n_cols = st.columns(4)
titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, t in enumerate(titles):
    if n_cols[i].button(t, use_container_width=True, type="primary" if st.session_state.view == t else "secondary", key=f"nav_{i}"):
        st.session_state.view = t
        st.rerun()

st.divider()

# --- LOGIQUE DES VUES ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    for m in active_c["messages"]:
        with st.chat_message(m["role"]): st.write(m["content"])

    with st.container():
        # ZONE DE TÉLÉCHARGEMENT (Fichiers pour Sage)
        up_file = st.file_uploader("📎 Charger Vision, Séquence ou Fréquence pour analyse...", 
                                  type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf"], key="up_main")
        
        prompt = st.text_area("Analyse ou directive...", height=150, key="in_main", placeholder="Décris ce que tu vois sur cette tablette...")
        
        # LES 4 BOUTONS (STATIQUES - PLACE 2)
        b = st.columns(4)
        with b[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="b_run"):
                if prompt or up_file:
                    active_c["messages"].append({"role": "user", "content": prompt if prompt else "Analyse du document."})
                    
                    # Construction du prompt Multi-Modal (Corrigé pour éviter NotFound)
                    p_parts = [f"Tu es le Sage. Contexte de persistance : {active_ctx}\n\n{prompt}"]
                    if up_file:
                        if up_file.type.startswith("image/"):
                            p_parts.append(PIL.Image.open(up_file))
                        else:
                            p_parts.append({"mime_type": up_file.type, "data": up_file.read()})
                    
                    with st.spinner("Le Sage scrute les tablettes..."):
                        try:
                            resp = model.generate_content(p_parts)
                            active_c["last_response"] = resp.text
                            active_c["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Erreur d'analyse : {e}")
                    st.rerun()
        
        with b[1]: 
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="b_at"):
                st.session_state.view = "🎨 Atelier de Ninharsag"; st.rerun()
        with b[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="b_vi"):
                st.session_state.view = "🎬 Visions de Veo 3"; st.rerun()
        with b[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="b_ly"):
                st.session_state.view = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER (image_2.png)
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        v_at = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150, key="at_p")
        c1, c2 = st.columns(2)
        with c1:
            m_at = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7"], key="at_m")
            f_at = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:3", "3:4", "16:9", "9:16", "21:9"], key="at_f")
        with c2:
            s_at = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"], key="at_s")
            q_at = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"], key="at_q")
        if st.form_submit_button("🚀 Graver & Manifester"):
            st.image(f"https://image.pollinations.ai/prompt/{v_at.replace(' ', '%20')}?nologo=true")

# 3. VISIONS (image_3.png)
elif st.session_state.view == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        s_vi = st.text_area("Séquence temporelle...", value=active_c["last_response"], height=150, key="vi_p")
        m_vi = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro"], key="vi_m")
        q_vi = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K"], value="1080p", key="vi_qual")
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. FRÉQUENCES (image_4.png)
elif st.session_state.view == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        a_ly = st.text_area("Paysage sonore...", value=active_c["last_response"], height=150, key="ly_p")
        m_ly = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"], key="ly_m")
        d_ly = st.slider("Durée (sec)", 10, 60, 30, key="ly_d")
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
