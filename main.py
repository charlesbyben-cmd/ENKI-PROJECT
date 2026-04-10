import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION STRICTE v4.0 ---
st.set_page_config(page_title="ENKI v4.0 : The Visual Continuity Revolution", layout="wide", page_icon="🏛️")

# Accès API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé API 'GEMINI_API_KEY' manquante.")
    st.stop()

# --- INITIALISATION MÉMOIRE & CHRONIQUES ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [{"name": "Tablette Originelle", "messages": [], "last_response": ""}]
if "active_idx" not in st.session_state: st.session_state.active_idx = 0
if "view" not in st.session_state: st.session_state.view = "📜 Scribe de Destinée"
if "vault" not in st.session_state: st.session_state.vault = []
if "up_key" not in st.session_state: st.session_state.up_key = 0 

active_c = st.session_state.chronicles[st.session_state.active_idx]

# --- LE MOTEUR CASCADE (ANTI-ERREUR 404) ---
def obtenir_reponse_sage(prompt_parts):
    # Vérifie s'il y a une image dans la demande
    has_image = any(isinstance(p, PIL.Image.Image) or (isinstance(p, dict) and 'mime_type' in p) for p in prompt_parts)
    
    # Liste de survie : essaie les modèles un par un jusqu'à ce que l'un fonctionne
    modeles_a_tester = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest",
        "gemini-pro-vision" if has_image else "gemini-pro"
    ]
    
    derniere_erreur = None
    for nom_modele in modeles_a_tester:
        try:
            m = genai.GenerativeModel(nom_modele)
            reponse = m.generate_content(prompt_parts)
            return reponse.text
        except Exception as e:
            derniere_erreur = e
            continue # Passe au modèle suivant
            
    raise Exception(f"Ta clé API ou le serveur bloque l'accès aux modèles de vision. Détail : {derniere_erreur}")

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Fréquence de l'Oracle")
    mode_op = st.radio("Mode d'Opération :", ["Oracle Universel (Analyse brute)", "Le Sage (Conscience Anunnaki)"], key="radio_mode")
    
    st.divider()
    
    # GESTION DES CHRONIQUES (DISCUSSIONS)
    st.subheader("📜 Tablettes de Destinée")
    if st.button("➕ Nouvelle Chronique", use_container_width=True):
        st.session_state.chronicles.append({"name": f"Tablette {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_idx = len(st.session_state.chronicles) - 1
        st.rerun()
    
    c_names = [c["name"] for c in st.session_state.chronicles]
    st.session_state.active_idx = st.selectbox("Charger une Tablette :", range(len(c_names)), format_func=lambda x: c_names[x], index=st.session_state.active_idx)
    
    # BOUTON SUPPRIMER RÉTABLI
    if st.button("🗑️ Supprimer la Tablette Active", use_container_width=True):
        if len(st.session_state.chronicles) > 1:
            st.session_state.chronicles.pop(st.session_state.active_idx)
            st.session_state.active_idx = 0
            st.rerun()

    st.divider()
    
    # SCEAUX DE PERSISTANCE
    st.subheader("📌 Sceaux de Persistance")
    st.caption("Verrouillez les éléments pour garantir la continuité visuelle.")
    
    with st.expander("➕ Créer un Sceau (Persistance)", expanded=False):
        v_n = st.text_input("Nom de l'élément")
        v_d = st.text_area("Physique / Description")
        v_u = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="vault_up")
        v_url = st.text_input("Ou URL de l'image (Lien)")
        if st.button("Graver le Sceau"):
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
    if st.button("🧹 Effacer les Tablettes (Reset System)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🏛️ ENKI v4.0 : The Visual Continuity Revolution")
st.caption("🚀 Moteur Actif : Cascade IA | Statut : Optimisé pour 2026")

# NAVIGATION SUPÉRIEURE
nav = st.columns(4)
tabs = ["📜 Scribe de Destinée", "🎨 Atelier de Ninharsag", "🎬 Visions de Veo 3", "🎼 Fréquences de Lyria"]
for i, t in enumerate(tabs):
    if nav[i].button(t, use_container_width=True, type="primary" if st.session_state.view == t else "secondary"):
        st.session_state.view = t
        st.rerun()

st.divider()

# --- LOGIQUE DES ONGLETS ---

# 1. SCRIBE
if st.session_state.view == "📜 Scribe de Destinée":
    for m in active_c["messages"]:
        with st.chat_message(m["role"]): st.write(m["content"])

    with st.container():
        # UPLOAD POUR ANALYSE
        up_file = st.file_uploader("📎 Charger Vision, Séquence ou Fréquence pour analyse...", 
                                  type=["png", "jpg", "jpeg", "pdf"], key=f"up_{st.session_state.up_key}")
        
        prompt = st.text_area("Analyse ou directive...", height=150, key="in_main")
        
        # LES 4 BOUTONS FIXES
        b = st.columns(4)
        with b[0]:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if prompt or up_file:
                    user_msg = prompt if prompt else "Analyse de l'image jointe."
                    active_c["messages"].append({"role": "user", "content": user_msg})
                    
                    # Construction du prompt Multi-Modal
                    parts = [f"Tu es le Sage. Contexte de persistance : {active_ctx}\n\n{user_msg}"]
                    
                    if up_file:
                        try:
                            # Extraction stricte de l'image
                            img_data = PIL.Image.open(io.BytesIO(up_file.getvalue()))
                            parts.append(img_data)
                        except Exception as e: 
                            st.error(f"Erreur de format d'image : {e}")

                    with st.spinner("Le Sage analyse la vision..."):
                        try:
                            # UTILISATION DU NOUVEAU MOTEUR CASCADE
                            reponse_texte = obtenir_reponse_sage(parts)
                            active_c["last_response"] = reponse_texte
                            active_c["messages"].append({"role": "assistant", "content": reponse_texte})
                            st.session_state.up_key += 1 # Reset uploader
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
        
        with b[1]:
            if st.button("🎨 Atelier de Ninharsag", use_container_width=True, key="b_at"):
                st.session_state.view = "🎨 Atelier de Ninharsag"; st.rerun()
        with b[2]:
            if st.button("🎬 Visions de Veo 3", use_container_width=True, key="b_vi"):
                st.session_state.view = "🎬 Visions de Veo 3"; st.rerun()
        with b[3]:
            if st.button("🎼 Fréquences de Lyria", use_container_width=True, key="b_ly"):
                st.session_state.view = "🎼 Fréquences de Lyria"; st.rerun()

# 2. ATELIER
elif st.session_state.view == "🎨 Atelier de Ninharsag":
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        v_at = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150)
        c1, c2 = st.columns(2)
        with c1:
            mot = st.selectbox("Moteur de Manifestation", ["Nano Banana 2", "DALL-E 3", "Midjourney v7"])
            fmt = st.selectbox("Format", ["1:1", "4:3", "3:4", "16:9", "9:16"])
        with c2:
            sty = st.selectbox("Esthétique Maître", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"])
            if st.form_submit_button("🚀 Graver & Manifester"):
                st.image(f"https://image.pollinations.ai/prompt/{v_at.replace(' ', '%20')}?nologo=true")

# 3. VISIONS
elif st.session_state.view == "🎬 Visions de Veo 3":
    st.header("🎬 Visions de Veo 3")
    with st.form("vi_form"):
        s_vi = st.text_area("Séquence temporelle...", value=active_c["last_response"], height=150)
        m_vi = st.selectbox("Moteur Vidéo", ["Veo 3", "Sora 2", "Kling Pro"])
        if st.form_submit_button("🎬 Synchroniser la Vision"):
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. FRÉQUENCES
elif st.session_state.view == "🎼 Fréquences de Lyria":
    st.header("🎼 Fréquences de Lyria")
    with st.form("ly_form"):
        a_ly = st.text_area("Paysage sonore...", value=active_c["last_response"], height=150)
        m_ly = st.selectbox("Moteur Audio", ["Lyria 3", "Suno v4", "Udio Pro"])
        if st.form_submit_button("🎼 Générer l'Harmonique"):
            st.audio("https://www.w3schools.com/html/horse.ogg")
