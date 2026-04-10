import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION SACRÉE v5.0 ---
st.set_page_config(page_title="ENKI v5.0 : Eternal Scribe", layout="wide", page_icon="🏛️")

# Accès API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- INITIALISATION DE LA MÉMOIRE ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "last_response" not in st.session_state: st.session_state.last_response = ""
if "active_tab" not in st.session_state: st.session_state.active_tab = "📜 Scribe de Destinée"

# --- MOTEUR SAGE (STABLE) ---
@st.cache_resource
def get_sage_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_sage_model()

# --- SIDEBAR : ARCHIVES D'ABZU (CONFIG PHOTO) ---
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
        s_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"])
        if st.button("Graver le Sceau"):
            if s_name and s_desc:
                st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_file, "active": True})
                st.rerun()

    active_ctx = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Détails : {seal['name']}", value=seal["active"], key=f"s_{i}")
        if seal["active"]:
            active_ctx += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']: st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)"):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()

# --- INTERFACE PRINCIPALE (UI PHOTO VALIDÉE) ---
st.title("🏛️ ENKI v5.0 : Eternal Scribe")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Statut : Optimisé pour 2026")

# NAVIGATION PAR BOUTONS (Simulant les onglets pour Switcher de l'un à l'autre)
nav_cols = st.columns(4)
titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, t in enumerate(titles):
    if nav_cols[i].button(t, use_container_width=True, type="primary" if st.session_state.active_tab == t else "secondary"):
        st.session_state.active_tab = t
        st.rerun()

st.divider()

# --- LOGIQUE DES ONGLETS ---

# 1. SCRIBE
if st.session_state.active_tab == "📜 Scribe de Destinée":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container():
        # UPLOAD DISCRET (Comme sur la photo)
        doc = st.file_uploader("📎 Vision (Image, PDF)", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
        prompt = st.text_area("Analyse ou directive...", height=150, key="main_input")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if prompt or doc:
                    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyse de l'image."})
                    
                    # Construction du prompt multi-modal
                    content_parts = [f"Tu es le Sage. Contexte de persistance : {active_ctx}\n\n{prompt}"]
                    if doc:
                        img = PIL.Image.open(doc)
                        content_parts.append(img)

                    with st.spinner("Le Sage ouvre ses sept yeux..."):
                        resp = model.generate_content(content_parts)
                        st.session_state.last_response = resp.text
                        st.session_state.messages.append({"role": "assistant", "content": resp.text})
                    st.rerun()
        
        with c2: 
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True):
                st.session_state.active_tab = "🎨 Atelier de Ninharsag"
                st.rerun()
        with c3:
            if st.button("🎬 Visions de Veo 3", use_container_width=True):
                st.session_state.active_tab = "🎬 Visions de Veo 3"
                st.rerun()
        with c4:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True):
                st.session_state.active_tab = "🎼 Fréquences de Lyria"
                st.rerun()

# 2. ATELIER (CONFIG NANO BANANA 2)
elif st.session_state.active_tab == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_response, height=150)
        moteur = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7", "Imagen 3"])
        fmt = st.selectbox("Format (Géométrie Sacrée)", ["1:1", "4:3", "16:9", "9:16"])
        style = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"])
        if st.form_submit_button("🚀 Graver & Manifester"):
            st.image(f"https://image.pollinations.ai/prompt/{vision.replace(' ', '%20')}?nologo=true")

# 3. VISIONS (CONFIG VEO 3)
elif st.session_state.active_tab == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        action = st.text_area("Séquence temporelle...", value=st.session_state.last_response, height=150)
        moteur_v = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro", "Gen-3 Alpha"])
        res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "2K", "4K"], value="1080p")
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. FRÉQUENCES (CONFIG LYRIA 3)
elif st.session_state.active_tab == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        amb = st.text_area("Paysage sonore...", value=st.session_state.last_response, height=150)
        moteur_a = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
        duree = st.slider("Durée (sec)", 10, 60, 30)
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
