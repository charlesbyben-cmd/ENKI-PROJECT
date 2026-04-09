import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION RÉVOLUTION ---
st.set_page_config(page_title="ENKI v3.0 - Visual Continuity", layout="wide", page_icon="🏛️")

# Initialisation de la Clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Configurez votre clé API dans les secrets.")
    st.stop()

# --- ARCHITECTURE DE LA MÉMOIRE (Le Coffre-fort) ---
if "vault" not in st.session_state:
    st.session_state.vault = {
        "Personnages": {
            "Ea (Enki)": {"desc": "Scientifique royal, regard bleu perçant, barbe sumérienne soignée.", "ref_img": "URL_IMAGE_ICI"},
            "Anu": {"desc": "Souverain, tiare dorée à 7 paires de cornes, barbe longue majestueuse.", "ref_img": ""}
        },
        "Équipements": {
            "Skaph-Suit": "Armure segmentée gris irisé, texture peau de poisson.",
            "Sceptre Lapis-Lazuli": "Cristal bleu profond, veines dorées, énergie plasma."
        },
        "Décors": {
            "Laboratoire Brutaliste": "Murs en pierre sombre, hologrammes bleus, technologie Nibiru."
        }
    }

if "active_locks" not in st.session_state:
    st.session_state.active_locks = []

# --- DÉTECTION DU MOTEUR ---
@st.cache_resource
def get_model():
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Priorité Gen 3 / 2026
    for m in ["gemini-3-flash", "gemini-1.5-flash"]:
        for a in available:
            if m in a: return genai.GenerativeModel(a), a
    return None, None

model_obj, model_name = get_model()

# --- SIDEBAR : LE POSTE DE VERROUILLAGE ---
with st.sidebar:
    st.title("🔏 Vault & Verrous")
    
    # 1. NOUVEAU SUJET (Comme sur Replit)
    with st.expander("➕ Nouveau Sujet", expanded=False):
        new_cat = st.selectbox("Catégorie", ["Personnages", "Équipements", "Décors"])
        new_name = st.text_input("Nom (ex: Tablette_IV)")
        new_desc = st.text_area("Description précise")
        new_ref = st.text_input("URL Image de Réf (Optionnel)")
        if st.button("Enregistrer au Vault"):
            if new_cat == "Personnages":
                st.session_state.vault[new_cat][new_name] = {"desc": new_desc, "ref_img": new_ref}
            else:
                st.session_state.vault[new_cat][new_name] = new_desc
            st.success(f"{new_name} verrouillé !")
            st.rerun()

    st.divider()

    # 2. ACTIVATION DES VERROUS POUR LA SCÈNE
    st.subheader("🛡️ Verrous Actifs")
    
    all_current_locks = []
    for cat, items in st.session_state.vault.items():
        st.write(f"**{cat}**")
        for name in items.keys():
            if st.checkbox(name, key=f"lock_{name}"):
                all_current_locks.append(f"[{name}: {items[name]['desc'] if isinstance(items[name], dict) else items[name]}]")
                if isinstance(items[name], dict) and items[name]['ref_img']:
                    all_current_locks.append(f"(REF VISUELLE: {items[name]['ref_img']})")
    
    st.session_state.active_locks = all_current_locks
    
    if st.button("🗑️ Reset Session"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title(f"🏛️ ENKI Master Studio v3.0")
st.caption(f"📡 Signal : {model_name} | Continuité Visuelle Activée")

tabs = st.tabs(["📜 Intelligence & Script", "🎨 Studio Image Pro", "🎬 Studio Vidéo Veo"])

# --- TAB 1 : INTELLIGENCE (L'esprit de continuité) ---
with tabs[0]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.form("chat_form"):
        user_input = st.text_area("Contexte de la scène...", height=100)
        if st.form_submit_button("Lancer la Réflexion"):
            # L'IA reçoit TOUS les verrous actifs en système
            system_prompt = f"Tu es le Sage Anunnaki. CONTEXTE VERROUILLÉ : {' '.join(st.session_state.active_locks)}"
            full_prompt = f"{system_prompt}\n\nUtilisateur: {user_input}"
            
            response = model_obj.generate_content(full_prompt)
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

# --- TAB 2 : STUDIO IMAGE (Prompt avec --cref simulé) ---
with tabs[1]:
    with st.form("image_pro"):
        col1, col2 = st.columns(2)
        with col1:
            scene = st.text_area("Action spécifique dans cette scène...")
            format_img = st.selectbox("Format", ["16:9", "21:9", "4:3", "1:1", "9:16"])
        with col2:
            style = st.selectbox("Esthétique Maître", ["Photo-réel Brut", "Concept Art UE5", "Manga High-Fidelity"])
            upscale = st.checkbox("Détails Ultra (8k)")
        
        if st.form_submit_button("🚀 Générer Master Prompt"):
            locks_str = " ".join(st.session_state.active_locks)
            final_prompt = f"STYLE: {style}. FORMAT: {format_img}. SCÈNE: {scene}. VERROUS ACTIFS: {locks_str}. --v 6.0 --cref"
            st.write("### 📜 Prompt avec Continuité Visuelle :")
            st.code(final_prompt)
            st.info("Ce prompt contient l'empreinte génétique de vos personnages verrouillés.")

# (Le Studio Vidéo suit la même logique d'injection des active_locks)
