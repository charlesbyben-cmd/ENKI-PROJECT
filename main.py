import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION v3.2 ---
st.set_page_config(page_title="ENKI v3.2 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Configuration des clés
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante dans les secrets.")
    st.stop()

# --- INITIALISATION ---
if "vault" not in st.session_state: st.session_state.vault = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- MOTEUR SAGE ---
@st.cache_resource
def get_sage_engine():
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for m in ["gemini-3-flash", "gemini-1.5-flash"]:
        for a in available:
            if m in a: return genai.GenerativeModel(a), a
    return None, "Aucun"

model_obj, model_name = get_sage_engine()

# --- SIDEBAR (Comme v3.1) ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel", "Le Sage"])
    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    # ... (Garder le système de création de sceaux de la v3.1 ici) ...
    active_context = ""
    for seal in st.session_state.vault:
        if st.checkbox(f"Sceau : {seal['name']}", value=seal.get('active', True)):
            active_context += f" [{seal['name']}: {seal['desc']}]"

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v3.2 : The Visual Continuity Revolution")

tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE (Avec Manifestation Intégrée) ---
with tabs[0]:
    # Affichage des messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    # Zone de saisie
    with st.container():
        user_input = st.text_area("Posez une question ou donnez une directive...", height=100, key="main_input")
        col_btn1, col_btn2 = st.columns([0.2, 0.8])
        
        with col_btn1:
            launch = st.button("🔱 Lancer la Réflexion")
        
        if launch and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            role = "Oracle" if "Oracle" in mode_op else "LE SAGE Anunnaki"
            prompt = f"Tu es {role}. Contexte : {active_context}\n\n{user_input}"
            response = model_obj.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

    st.divider()

    # --- NOUVEAU : PANNEAU DE MANIFESTATION RAPIDE ---
    if st.session_state.messages:
        st.subheader("⚡ Manifestation Immédiate")
        st.caption("Générez des actifs basés sur la dernière réponse du Sage sans remonter.")
        
        col_m1, col_m2 = st.columns([0.4, 0.6])
        
        with col_m1:
            moteur = st.selectbox("Sceau de Manifestation", 
                                ["Nano Banana 2 (Vitesse/Style)", 
                                 "DALL-E 3 (Précision Textuelle)", 
                                 "Veo 3 (Cinéma Temporel)"])
        
        with col_m2:
            st.write("") # Alignement
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🎨 Image", use_container_width=True):
                    st.info(f"Requête envoyée à Ninharsag via {moteur}...")
                    # Ici le code appellerait l'API choisie
            with c2:
                if st.button("🎬 Vidéo", use_container_width=True):
                    st.info(f"Ouverture des Visions de Veo 3...")
            with c3:
                if st.button("🎼 Audio", use_container_width=True):
                    st.info("Harmonisation Lyria 3 en cours...")

# --- ONGLETS DÉTAILLÉS (Pour les configurations avancées) ---
with tabs[1]:
    st.header("🎨 Atelier Profond de Ninharsag")
    # ... (Garder le configurateur détaillé d'image ici) ...

with tabs[2]:
    st.header("🎬 Visions Temporelles de Veo 3")
    # ... (Garder le configurateur détaillé de vidéo ici) ...
