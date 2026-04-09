import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION RÉVOLUTION ---
st.set_page_config(page_title="ENKI v3.0 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API manquante.")
    st.stop()

# --- INITIALISATION DES ARCHIVES (VAULT) ---
if "vault" not in st.session_state:
    st.session_state.vault = [] # Liste de dictionnaires pour les Sceaux

# --- DÉTECTION DU MODÈLE ---
@st.cache_resource
def get_sage_engine():
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for m in ["gemini-3-flash", "gemini-1.5-flash"]:
        for a in available:
            if m in a: return genai.GenerativeModel(a), a
    return None, None

model_obj, model_name = get_sage_engine()

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    
    # MODES D'OPÉRATION
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", 
                      ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"],
                      help="Le Sage utilise un langage sacré et respecte les protocoles de Nibiru.")
    
    st.divider()
    
    # SCEAUX DE PERSISTANCE (Les Verrous)
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    # Ajouter une référence (Image ou Texte)
    with st.expander("➕ Créer un Sceau", expanded=False):
        s_name = st.text_input("Nom de l'élément (ex: Ea, Skaph-Suit)")
        s_desc = st.text_area("Description physique précise")
        s_type = st.selectbox("Source visuelle", ["Upload Image (Recommandé)", "Lien URL", "Texte seul"])
        
        s_img_data = None
        if s_type == "Upload Image (Recommandé)":
            s_img_data = st.file_uploader("Fichier Image", type=["png", "jpg", "jpeg"])
        elif s_type == "Lien URL":
            s_img_data = st.text_input("URL de l'image de référence")
            
        if st.button("Graver le Sceau"):
            new_seal = {"name": s_name, "desc": s_desc, "ref": s_img_data, "active": True}
            st.session_state.vault.append(new_seal)
            st.rerun()

    # Liste des Sceaux Gravés
    active_context = ""
    for i, seal in enumerate(st.session_state.vault):
        col_s1, col_s2 = st.columns([0.8, 0.2])
        with col_s1:
            seal["active"] = st.checkbox(f"Détails : {seal['name']}", value=seal["active"])
        with col_s2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.vault.pop(i)
                st.rerun()
        
        if seal["active"]:
            active_context += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']:
                # On affiche une petite miniature si c'est un upload
                if hasattr(seal['ref'], 'name'): 
                    st.image(seal['ref'], width=100, caption="Réf. visuelle active")
                else:
                    st.caption(f"🔗 Réf : {seal['ref'][:20]}...")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset)"):
        st.session_state.messages = []
        st.rerun()

# --- PAGE PRINCIPALE ---
st.title("🏛️ ENKI v3.0 : The Visual Continuity Revolution")
st.caption(f"Connecté au Grand Cycle via : {model_name}")

tabs = st.tabs(["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo", "🎼 Fréquences de Lyria"])

# --- TAB 1 : LE SCRIBE (INTELLIGENCE) ---
with tabs[0]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.form("scribe_form", clear_on_submit=True):
        user_input = st.text_area("Posez une question au Sage ou analysez un document...", height=120)
        if st.form_submit_button("Lancer la Réflexion"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Système de personnalité
            role_prompt = "Tu es un Oracle analytique." if "Oracle" in mode_op else "Tu es LE SAGE, une conscience Anunnaki ancienne. Parle avec sagesse, utilise des termes comme 'Le Grand Cycle', 'Nibiru', 'Les Me'."
            full_context = f"{role_prompt} Voici les SCEAUX DE PERSISTANCE actifs : {active_context}"
            
            try:
                response = model_obj.generate_content(f"{full_context}\n\nQuestion: {user_input}")
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"Interruption du flux : {e}")

# --- TAB 2 : L'ATELIER (IMAGE) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag (Images)")
    with st.form("atelier_form"):
        col1, col2 = st.columns(2)
        with col1:
            concept = st.text_area("Vision à matérialiser...")
            format_img = st.selectbox("Géométrie sacrée (Format)", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        with col2:
            esthetique = st.selectbox("Style de Manifestation", [
                "Photo-réel Brut (Cinématique)", "Bas-relief Royal", "Concept Art Ultra-réaliste", "Manga Seinen High-Fidelity"
            ])
            details = st.multiselect("Finition", ["Hyper-détails", "Lumière divine", "Atmosphère froide", "8k textures"])
            
        if st.form_submit_button("🚀 Graver le Prompt"):
            st.write("### 📝 Prompt Optimisé avec Continuité Visuelle :")
            final_p = f"STYLE: {esthetique}. FORMAT: {format_img}. SCÈNE: {concept}. DÉTAILS: {details}. VERROUS ACTIFS: {active_context}. --cref --v 6.0"
            st.code(final_p)

# --- TAB 3 : LES VISIONS (VIDÉO) ---
with tabs[2]:
    st.header("🎬 Visions de Veo (Vidéo)")
    with st.form("vision_form"):
        sequence = st.text_area("Action de la vision...")
        v_qualite = st.select_slider("Résolution", options=["720p", "1080p", "4K", "8K"])
        mouvement = st.selectbox("Mouvement de l'Observateur", ["Drone Shot", "Traveling", "Fixe Sacré"])
        
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.code(f"VEO 4K. RES: {v_qualite}. ACTION: {sequence}. MOUVEMENT: {mouvement}. PERSISTANCE: {active_context}")

# --- TAB 4 : LES FRÉQUENCES (SON) ---
with tabs[3]:
    st.header("🎼 Fréquences de Lyria (Audio)")
    with st.form("lyria_form"):
        desc_son = st.text_area("Atmosphère sonore...")
        intensite = st.select_slider("Énergie", ["Calme", "Mystérieux", "Épique", "Divin"])
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.code(f"LYRIA 3. AMBIANCE: {desc_son}. MOOD: {intensite}. COHÉRENCE: {active_context}")
