import streamlit as st
import google.generativeai as genai
import time
import requests

# --- CONFIGURATION RÉVOLUTION v3.7 - MANIFESTATION TOTALE ---
st.set_page_config(page_title="ENKI v3.7 : Manifestation Totale", layout="wide", page_icon="🏛️")

# VÉRIFICATION DES SECRETS (RIGUEUR TOTAL)
if "GEMINI_API_KEY" in st.secrets and "OPENAI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Configuration réelle pour OpenAI (DALL-E 3, Sora)
    from openai import OpenAI
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("❌ Configuration API manquante dans les secrets.")
    st.write("Veuillez ajouter 'GEMINI_API_KEY' et 'OPENAI_API_KEY' à vos secrets Streamlit.")
    st.stop()

# --- INITIALISATION ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []
if "active_tab" not in st.session_state: st.session_state.active_tab = "📜 Scribe de Destinée"
if "last_response" not in st.session_state: st.session_state.last_response = ""

# --- FONCTION DE NAVIGATION ---
def navigate_to(target):
    st.session_state.active_tab = target
    st.rerun()

# --- MOTEUR SAGE (RÉEL) ---
@st.cache_resource
def get_sage_engine():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ["gemini-3-flash", "gemini-1.5-flash"]:
            for a in available:
                if m in a: return genai.GenerativeModel(a)
    except: pass
    return genai.GenerativeModel("gemini-1.5-flash")

sage_mod = get_sage_engine()

# --- SIDEBAR (ARCHIVES D'ABZU) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        s_name = st.text_input("Nom de l'élément")
        s_desc = st.text_area("Physique / Description précise")
        s_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"])
        s_url = st.text_input("Ou coller URL de l'image")
        if st.button("Graver le Sceau"):
            ref = s_file if s_file else s_url
            st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": ref, "active": True})
            st.rerun()

    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"])
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref'] and hasattr(seal['ref'], 'name'): st.image(seal['ref'], width=100)

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE PRINCIPALE (HAUT) ---
st.title("🏛️ ENKI v3.7 : Manifestation Totale")
st.caption(f"🚀 Moteur Scribe Actif via Gemini | Statut : Optimisé pour 2026")

c_nav = st.columns(4)
nav_titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, title in enumerate(nav_titles):
    if c_nav[i].button(title, use_container_width=True, type="primary" if st.session_state.active_tab == title else "secondary"):
        st.session_state.active_tab = title
        st.rerun()

st.divider()

# --- LOGIQUE DE MANIFESTATION ---

# 1. SCRIBE
if st.session_state.active_tab == "📜 Scribe de Destinée":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    with st.container():
        user_input = st.text_area("Analyse ou directive...", height=120, key="scribe_input")
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": user_input})
                role = "Oracle" if "Oracle" in mode_op else "LE SAGE"
                resp = sage_mod.generate_content(f"Tu es {role}. Contexte de continuité : {active_context}\n\nUtilisateur : {user_input}")
                st.session_state.last_response = resp.text
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.rerun()
        with cb2:
            if st.button("🎨 Atelier de Ninharsag ", use_container_width=True): navigate_to("🎨 Atelier de Ninharsag")
        with cb3:
            if st.button("🎬 Visions de Veo 3 ", use_container_width=True): navigate_to("🎬 Visions de Veo 3")
        with cb4:
            if st.button("🎼 Fréquences de Lyria ", use_container_width=True): navigate_to("🎼 Fréquences de Lyria")

# 2. ATELIER (IMAGE - CONNECTÉ RÉEL OPENAI)
elif st.session_state.active_tab == "🎨 Atelier de Ninharsag":
    st.title("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            vision = st.text_area("Vision à matérialiser...", value=st.session_state.last_response, height=150)
            ratio = st.selectbox("Format", ["1024x1024", "1792x1024 (16:9)", "1024x1792 (9:16)"])
        with col_a2:
            moteur = st.selectbox("Moteur", ["DALL-E 3 (Réel Connecté)", "Nano Banana 2 (PlaceHolder)"])
            style = st.selectbox("Esthétique", ["Photoréaliste Brut (8k Leica)", "Concept Art UE5", "Manga Seinen High-Fidelity"])
            if st.form_submit_button("🚀 Graver & Manifester (Réel DALL-E 3)"):
                with st.spinner("Matérialisation de l'atome en cours via OpenAI..."):
                    if moteur == "DALL-E 3 (Réel Connecté)":
                        try:
                            full_prompt = f"STYLE: {style}. SCENE: {vision}. PERSISTANCE VISUELLE: {active_context}"
                            # APPEL RÉEL À L'API DALL-E 3
                            response = client_openai.images.generate(
                                model="dall-e-3",
                                prompt=full_prompt,
                                size=ratio,
                                quality="hd",
                                n=1,
                            )
                            # Manifestation réelle sur place
                            st.image(response.data[0].url, caption=f"Manifestation {style} - DALL-E 3")
                        except Exception as e:
                            st.error(f"Interruption du flux de manifestation DALL-E 3 : {e}")
                    else:
                        st.info("Simulation activée pour ce moteur.")

# 3. VISIONS (VIDÉO - PLACEHOLDER SORA)
elif st.session_state.active_tab == "🎬 Visions de Veo 3":
    st.title("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            action = st.text_area("Séquence temporelle...", value=st.session_state.last_response, height=150)
            res = st.select_slider("Qualité Vidéo", options=["720p", "1080p", "4K", "8K"], value="1080p")
        with col_v2:
            moteur_v = st.selectbox("Moteur Vidéo", ["Sora 2 (PlaceHolder)", "Veo 3 (PlaceHolder)"])
            cam = st.selectbox("Caméra", ["Drone Shot", "Traveling Latéral", "Steadycam", "Fixe Sacré"])
            if st.form_submit_button("🎬 Synchroniser la Vision (Simulation)"):
                with st.spinner(f"Simulation de génération via {moteur_v}..."):
                    time.sleep(2) # Simulation de latence API
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Placeholder vidéo direct

# 4. FRÉQUENCES (AUDIO - PLACEHOLDER LYRIA)
elif st.session_state.active_tab == "🎼 Fréquences de Lyria":
    st.title("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            amb = st.text_area("Paysage sonore...", value=st.session_state.last_response, height=150)
            duree = st.slider("Durée (secondes)", 10, 60, 30)
        with col_s2:
            nrj = st.select_slider("Énergie", ["Méditatif", "Mystérieux", "Tension", "Épique", "Apocalyptique"], value="Mystérieux")
            if st.form_submit_button("🎼 Générer l'Harmonique (Simulation)"):
                with st.spinner("Simulation d'harmonisation audio..."):
                    st.audio("https://www.w3schools.com/html/horse.ogg") # Placeholder audio direct
