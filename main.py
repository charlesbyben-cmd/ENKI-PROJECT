import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- CONFIGURATION ENKI v5.5 ---
st.set_page_config(page_title="ENKI v5.5 : Restoration", layout="wide", page_icon="🏛️")

# Configuration API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- GESTION DE LA MÉMOIRE ET DES CHRONIQUES ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [
        {"name": "📜 Tablette Originelle", "messages": [], "last_response": ""},
    ]
if "active_chron_idx" not in st.session_state:
    st.session_state.active_chron_idx = 0
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "📜 Scribe de Destinée"
if "vault" not in st.session_state: 
    st.session_state.vault = []

active_c = st.session_state.chronicles[st.session_state.active_chron_idx]

# --- MOTEUR SAGE (STABLE) ---
@st.cache_resource
def load_sage():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_sage()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="mode")
    
    st.divider()
    
    # NOUVEAU : GESTION DES CHRONIQUES
    st.subheader("📜 Tablettes de Destinée")
    if st.button("➕ Nouvelle Chronique", use_container_width=True):
        st.session_state.chronicles.append({"name": f"✨ Tablette {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_chron_idx = len(st.session_state.chronicles) - 1
        st.rerun()
    
    c_names = [c["name"] for c in st.session_state.chronicles]
    new_idx = st.selectbox("Charger une Tablette :", range(len(c_names)), format_func=lambda x: c_names[x], index=st.session_state.active_chron_idx)
    st.session_state.active_chron_idx = new_idx

    st.divider()
    
    # SCEAUX DE PERSISTANCE
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        v_name = st.text_input("Nom de l'élément", key="v_n")
        v_desc = st.text_area("Physique / Description", key="v_d")
        v_up = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="v_u")
        if st.button("Graver le Sceau"):
            if v_name and v_desc:
                st.session_state.vault.append({"name": v_name, "desc": v_desc, "ref": v_up, "active": True})
                st.rerun()

    active_ctx = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"], key=f"s_{i}")
        if seal["active"]:
            active_ctx += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE (CONFIG PHOTO) ---
st.title("🏛️ ENKI v3.5 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Statut : Optimisé pour 2026")

# NAVIGATION SUPÉRIEURE (Les 4 Onglets Originaux)
n_cols = st.columns(4)
btns = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, b_title in enumerate(btns):
    if n_cols[i].button(b_title, use_container_width=True, type="primary" if st.session_state.current_tab == b_title else "secondary"):
        st.session_state.current_tab = b_title
        st.rerun()

st.divider()

# --- VUES ---

# 1. SCRIBE (Avec Upload Analyse)
if st.session_state.current_tab == "📜 Scribe de Destinée":
    for m in active_c["messages"]:
        with st.chat_message(m["role"]): st.write(m["content"])

    with st.container():
        # MODULE DE TÉLÉCHARGEMENT POUR ANALYSE
        up_doc = st.file_uploader("📎 Charger Vision, Séquence ou Fréquence pour analyse...", 
                                 type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf"], key="up_scribe")
        
        u_input = st.text_area("Analyse ou directive...", height=150, key="in_scribe")
        
        # BOUTONS DU BAS (SYMETRIE DIVINE)
        b_cols = st.columns(4)
        with b_cols[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if u_input or up_doc:
                    active_c["messages"].append({"role": "user", "content": u_input if u_input else "Analyse du document joint."})
                    prompt = [f"Tu es le Sage. Contexte de continuité : {active_ctx}\n\n{u_input}"]
                    if up_doc:
                        if up_doc.type.startswith("image/"):
                            prompt.append(PIL.Image.open(up_doc))
                        else:
                            prompt.append({"mime_type": up_doc.type, "data": up_doc.read()})
                    
                    with st.spinner("Le Sage scrute les tablettes..."):
                        resp = model.generate_content(prompt)
                        active_c["last_response"] = resp.text
                        active_c["messages"].append({"role": "assistant", "content": resp.text})
                    st.rerun()
        
        with b_cols[1]: 
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="go_at"):
                st.session_state.current_tab = "🎨 Atelier de Ninharsag"; st.rerun()
        with b_cols[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="go_vi"):
                st.session_state.current_tab = "🎬 Visions de Veo 3"; st.rerun()
        with b_cols[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="go_ly"):
                st.session_state.current_tab = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER (image_2.png)
elif st.session_state.current_tab == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        v_at = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150)
        c_at1, c_at2 = st.columns(2)
        with c_at1:
            mot_at = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"])
            fmt_at = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:3", "3:4", "16:9", "9:16"])
        with c_at2:
            sty_at = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"])
            qual_at = st.select_slider("Qualité Rendu", options=["720p", "1080p", "2K", "4K", "8K"])
        if st.form_submit_button("🚀 Graver & Manifester"):
            st.image(f"https://image.pollinations.ai/prompt/{v_at.replace(' ', '%20')}?nologo=true")

# 3. VISIONS (image_3.png)
elif st.session_state.current_tab == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        s_vi = st.text_area("Séquence temporelle...", value=active_c["last_response"], height=150)
        m_vi = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
        q_vi = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K"], value="1080p")
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. FRÉQUENCES (image_2.png / Audio config)
elif st.session_state.current_tab == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        a_ly = st.text_area("Paysage sonore à harmoniser...", value=active_c["last_response"], height=150)
        m_ly = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
        d_ly = st.slider("Durée (sec)", 10, 60, 30)
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
