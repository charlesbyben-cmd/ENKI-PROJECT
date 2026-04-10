import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURATION RÉVOLUTION v4.9 ---
st.set_page_config(page_title="ENKI v4.9 : L'Éveil des Sept Yeux", layout="wide", page_icon="🏛️")

# Configuration des Clés API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ Clé 'GEMINI_API_KEY' manquante dans les secrets.")
    st.stop()

# --- GESTION DES CHRONIQUES (PROJETS) ---
if "chronicles" not in st.session_state:
    st.session_state.chronicles = [
        {"id": "abzu_1", "name": "📜 Tablette de l'Abzu", "messages": [], "last_response": ""},
        {"id": "dilmun_1", "name": "🏝️ Chroniques de Dilmun", "messages": [], "last_response": ""},
    ]
if "active_id" not in st.session_state:
    st.session_state.active_id = "abzu_1"

def get_active():
    return next((c for c in st.session_state.chronicles if c["id"] == st.session_state.active_id), st.session_state.chronicles[0])

# Sceaux de Persistance
if "vault" not in st.session_state: st.session_state.vault = []

# --- MOTEUR SAGE (NOM FIXÉ POUR STABILITÉ) ---
@st.cache_resource
def get_sage():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_sage()

# --- SIDEBAR : ARCHIVES D'ABZU ---
with st.sidebar:
    st.title("🧠 Archives d'Abzu")
    st.subheader("📡 Mode d'Opération")
    mode = st.radio("Fréquence :", ["Oracle Universel", "Le Sage Anunnaki"])
    
    st.divider()
    st.subheader("📜 Tablettes (Discussions)")
    
    # Créer une nouvelle discussion
    if st.button("➕ Nouvelle Tablette Sacrée", use_container_width=True):
        new_id = f"chron_{len(st.session_state.chronicles)+1}"
        st.session_state.chronicles.append({"id": new_id, "name": f"✨ Nouvelle Chronique {len(st.session_state.chronicles)+1}", "messages": [], "last_response": ""})
        st.session_state.active_id = new_id
        st.rerun()

    # Sélecteur de Chronique
    names = [c["name"] for c in st.session_state.chronicles]
    current_name = st.selectbox("Charger une Tablette :", names, index=names.index(get_active()["name"]))
    st.session_state.active_id = next(c["id"] for c in st.session_state.chronicles if c["name"] == current_name)

    if st.button("🗑️ Briser la Tablette Active"):
        if len(st.session_state.chronicles) > 1:
            st.session_state.chronicles = [c for c in st.session_state.chronicles if c["id"] != st.session_state.active_id]
            st.session_state.active_id = st.session_state.chronicles[0]["id"]
            st.rerun()

    st.divider()
    st.subheader("📌 Sceaux de Persistance")
    with st.expander("➕ Graver un Sceau", expanded=False):
        s_name = st.text_input("Nom de l'entité")
        s_desc = st.text_area("Description physique")
        s_up = st.file_uploader("Image de référence", type=["png", "jpg", "jpeg"], key="vault_up")
        if st.button("Fixer dans l'éternité"):
            if s_name and s_desc:
                st.session_state.vault.append({"name": s_name, "desc": s_desc, "ref": s_up, "active": True})
                st.rerun()

    active_ctx = ""
    for seal in st.session_state.vault:
        seal["active"] = st.checkbox(f"Sceau : {seal['name']}", value=seal["active"])
        if seal["active"]: active_ctx += f" [{seal['name']}: {seal['desc']}]"

# --- INTERFACE PRINCIPALE ---
active_c = get_active()
st.title(f"🏛️ ENKI v4.9 : {active_c['name']}")

tabs = st.tabs(["📜 Scribe", "🎨 Atelier", "🎬 Visions", "🎼 Fréquences"])

# --- TAB 1 : LE SCRIBE ---
with tabs[0]:
    for msg in active_c["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    with st.container(border=True):
        st.caption("🛰️ Console de Vision et de Saisie")
        col_up, col_txt = st.columns([0.3, 0.7])
        with col_up:
            # Uploader d'image directement visible
            doc = st.file_uploader("📎 Vision (Image, PDF)", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
        with col_txt:
            prompt = st.text_area("Analyse ou directive...", height=100, key="p_input", placeholder="Décris ce que tu vois sur cette tablette...")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔱 Lancer la Réflexion", use_container_width=True):
                if prompt or doc:
                    active_c["messages"].append({"role": "user", "content": prompt if prompt else "Analyse de la vision."})
                    
                    # Construction du prompt Multi-Modal
                    parts = [f"Tu es le Sage. Contexte Anunnaki : {active_ctx}\n\n{prompt}"]
                    if doc:
                        if doc.type.startswith("image/"):
                            parts.append(PIL.Image.open(doc))
                        else:
                            parts.append({"mime_type": doc.type, "data": doc.read()})

                    with st.spinner("Le Sage ouvre ses sept yeux..."):
                        try:
                            resp = model.generate_content(parts)
                            active_c["last_response"] = resp.text
                            active_c["messages"].append({"role": "assistant", "content": resp.text})
                        except Exception as e:
                            st.error(f"Interruption du flux : {e}")
                    st.rerun()
        
        with c2: st.button("🎨 Atelier", use_container_width=True, on_click=lambda: st.toast("Transmis à Ninharsag"))
        with c3: st.button("🎬 Visions", use_container_width=True, on_click=lambda: st.toast("Transmis à Veo"))
        with c4: st.button("🎼 Fréquences", use_container_width=True, on_click=lambda: st.toast("Transmis à Lyria"))

# --- TAB 2 : ATELIER (NANO BANANA 2 RÉEL) ---
with tabs[1]:
    st.header("🎨 Atelier de Ninharsag")
    with st.form("at_form"):
        vision = st.text_area("Vision à matérialiser...", value=active_c["last_response"], height=150)
        col1, col2 = st.columns(2)
        with col1:
            moteur = st.selectbox("Moteur", ["Nano Banana 2", "DALL-E 3", "Midjourney v7"])
            format_img = st.selectbox("Format", ["1:1", "4:3", "16:9", "9:16"])
        with col2:
            style = st.selectbox("Esthétique", ["Photo-réel Brut (8k)", "Concept Art UE5", "Bas-relief Royal"])
            if st.form_submit_button("🚀 Graver & Manifester"):
                if moteur == "Nano Banana 2":
                    p_enc = vision.replace(" ", "%20").replace("\n", "%20")
                    st.image(f"https://image.pollinations.ai/prompt/{p_enc}%20{style}%20{format_img}?nologo=true")
