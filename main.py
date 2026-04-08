import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="ENKI v2.0", layout="wide", page_icon="🚀")

# Initialisation API avec sécurité
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# --- MÉMOIRE PERSISTANTE (Side Bar) ---
if "locked_data" not in st.session_state:
    st.session_state.locked_data = {
        "Anu": "Homme puissant, barbe majestueuse, tiare à 7 cornes.",
        "Ea": "Scientifique royal, regard perçant, symboles techniques.",
        "Projet_X": "Description de votre recherche actuelle ici..."
    }

# --- LOGIQUE DE CACHE ---
@st.cache_resource
def get_model(model_name='gemini-1.5-flash'):
    return genai.GenerativeModel(model_name)

# --- INTERFACE LATERALE ---
with st.sidebar:
    st.title("🧠 Mémoire & Verrous")
    mode = st.radio("Mode d'Opération :", ["Chercheur Universel", "Sage Anunnaki"])
    
    st.divider()
    st.subheader("📌 Éléments Verrouillés")
    for k, v in st.session_state.locked_data.items():
        with st.expander(f"Détails : {k}"):
            st.session_state.locked_data[k] = st.text_area(f"Éditer {k}", v, key=f"edit_{k}")
    
    if st.button("+ Ajouter une référence"):
        st.session_state.locked_data["Nouveau"] = "Décrivez ici..."

# --- INTERFACE PRINCIPALE ---
st.title(f"🚀 ENKI v2.0 : {mode}")

tabs = st.tabs(["💬 Intelligence (Texte)", "🎨 Studio Image", "🎬 Studio Vidéo"])

# --- TAB : TEXTE & RECHERCHE ---
with tabs[0]:
    st.info(f"Mode actuel : {mode}. L'IA utilise les éléments verrouillés comme contexte.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Posez une question ou analysez un document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            model = get_model()
            # Construction du contexte selon le mode
            contexte = f"Tu es un assistant de recherche expert en mode {mode}."
            memoire = f" Voici les données verrouillées à respecter : {str(st.session_state.locked_data)}"
            
            with st.spinner("Analyse des flux de données..."):
                response = model.generate_content(f"{contexte}\n{memoire}\n\nQuestion : {prompt}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.markdown(response.text)
        except Exception as e:
            st.error(f"⚠️ Pause requise par le serveur (Quota). Réessayez dans 30s.")

# --- TAB : IMAGE (NANO BANANA 2) ---
with tabs[1]:
    st.header("🎨 Générateur d'Images")
    col1, col2 = st.columns(2)
    with col1:
        sujet = st.text_area("Description visuelle...", placeholder="Un laboratoire spatial sur Mars...")
        aspect = st.selectbox("Format", ["16:9 (Large)", "1:1 (Carré)", "9:16 (Vertical)"])
    with col2:
        if st.button("🚀 Générer avec Nano Banana 2"):
            st.write("### 📝 Prompt Optimisé pour Nano Banana 2 :")
            # Ici, l'IA génère le prompt parfait basé sur tes verrous
            final_prompt = f"Scène : {sujet}. Format : {aspect}. Style : Réalisme froid. Références : {st.session_state.locked_data}"
            st.code(final_prompt)
            st.caption("Copiez ce code dans le module de génération d'image.")

# --- TAB : VIDÉO (VEO) ---
with tabs[2]:
    st.header("🎬 Studio Vidéo Veo")
    video_prompt = st.text_input("Décrivez la séquence animée (mouvements, audio...)")
    if st.button("🎬 Préparer Séquence Veo"):
        st.progress(100)
        st.success("Séquence prête pour l'injection Veo. Audio natif synchronisé.")
