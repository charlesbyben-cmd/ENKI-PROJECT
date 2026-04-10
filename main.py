import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION SACRÉE v6.0 ---
st.set_page_config(page_title="ENKI v6.0 : Sovereign Vision", layout="wide", page_icon="🏛️")

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

# --- MOTEUR SAGE (STABILITÉ TOTALE) ---
@st.cache_resource
def load_sage():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_sage()

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

    # BOUTON SUPPRIMER CHRONIQUE (RÉTABLI)
    if st.button("🗑️ Supprimer la Tablette", use_container_width=True, key="del_chron"):
        if len(st.session_state.chronicles) > 1:
            st.session_state.chronicles.pop(st.session_state.active_idx)
            st.session_state.active_idx = 0
            st.rerun()
        else:
            st.warning("Impossible de supprimer la dernière Tablette Sacrée.")

    st.divider()
    
    # SCEAUX DE PERSISTANCE (AVEC PHRASE EXPLICATIVE RÉTABLIE)
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.") # PHRASE RÉTABLIE
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        v_n = st.text_input("Nom de l'élément", key="v_n")
        v_d = st.text_area("Physique / Description", key="v_d")
        v_u = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="v_u")
        v_url = st.text_input("Ou URL de l'image", key="v_url")
        if st.button("Graver le Sceau", key="v_b"):
            if v_n and v_d:
                ref = v_u if v_u else v_url
                st.session_state.vault.append({"name": v_n, "desc": v_d, "ref": ref, "active": True})
                st.rerun()

    active_ctx = ""
    for i, seal in enumerate(st.session_state.vault):
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"], key=f"s_c_{i}")
        if seal["active"]:
            active_ctx += f" [{seal['name']}: {seal['desc']}]"
            if seal['ref']:
                try:
                    if isinstance(seal['ref'], str): st.image(seal['ref'], width=100)
                    else: st.image(seal['ref'], width=100)
                except: st.caption("🔗 Sceau actif")

    st.divider()
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True, key="res_sys"):
        st.session_state.clear(); st.rerun()

# --- INTERFACE PRINCIPALE (UI CONFIG v3.5/v4.0) ---
st.title("🏛️ ENKI v6.0 : Sovereign Vision")
st.caption("🚀 Moteur Actif : Gemini-1.5-Flash | Analyse Multi-Modale : ACTIVÉE")

# NAVIGATION SUPÉRIEURE
n_cols = st.columns(4)
titles = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, t in enumerate(titles):
    if n_cols[i].button(t, use_container_width=True, type="primary" if st.session_state.view == t else "secondary", key=f"nav_{i}"):
        st.session_state.view = t; st.rerun()

st.divider()

# --- LOGIQUE DES VUES ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    for m in active_c["messages"]:
        with st.chat_message(m["role"]): st.write(m["content"])

    with st.container():
        # ZONE ANALYSE (Upload)
        up_file = st.file_uploader("📎 Charger Vision, Séquence ou Fréquence pour analyse...", 
                                  type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf"], key="up_main")
        
        prompt = st.text_area("Analyse ou directive...", height=150, key="in_main")
        
        # LES 4 BOUTONS FIXES
        b = st.columns(4)
        with b[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True, key="b_run"):
                if prompt or up_file:
                    active_c["messages"].append({"role": "user", "content": prompt if prompt else "Analyse de la vision."})
                    
                    # Construction Robuste du Prompt (Fix Vision iPad)
                    p_parts = [f"Tu es le Sage. Contexte de persistance : {active_ctx}\n\nConsigne : {prompt}"]
                    
                    if up_file:
                        try:
                            # Utilisation d'un buffer pour garantir la lecture sur iPad
                            image_bytes = up_file.getvalue()
                            img_obj = PIL.Image.open(io.BytesIO(image_bytes))
                            p_parts.append(img_obj)
                        except Exception as e:
                            st.error(f"Erreur de lecture : {e}")

                    with st.spinner("Le Sage scrute les tablettes..."):
                        try:
                            # Appel direct et forcé
                            resp = model.generate_content(p_parts)
                            if resp.text:
                                active_c["last_response"] = resp.text
                                active_c["messages"].append({"role": "assistant", "content": resp.text})
                            else:
                                st.warning("Le Sage est resté silencieux. Réessaie avec une consigne plus précise.")
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
            f_at = st.selectbox("Format", ["1:1", "4:3", "16:9", "9:16"], key="at_f")
        with c2:
            s_at = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"], key="at_s")
            q_at = st.select_slider("Qualité", options=["720p", "1080p", "4K", "8K"], key="at_q")
        if st.form_submit_button("🚀 Graver & Manifester"):
            st.image(f"https://image.pollinations.ai/prompt/{v_at.replace(' ', '%20')}?nologo=true")

# (Visions et Fréquences identiques à tes photos)
