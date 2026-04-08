import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="ENKI v1.4", layout="wide", page_icon="🏛️")

# --- CONFIGURATION API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ Clé API manquante dans les Secrets !")
    st.stop()

# --- TITRE ---
st.title("🏛️ ENKI : Master Archive v1.4")
st.subheader("⚙️ Centre d'Opérations")

# --- SÉLECTION DE LA CIBLE ---
with st.expander("🔍 Sélectionner une Tablette ou une Entité", expanded=True):
    target = st.selectbox(
        "Sur quel sujet le Sage doit-il concentrer son analyse ?",
        ["(Choisir)", "Ea (Enki)", "Enlil", "Anu", "4ème Tablette", "Livre d'Enki (Complet)"],
        index=0
    )

# --- ZONE D'ANALYSE ---
if target != "(Choisir)":
    st.info(f"📍 Analyse focalisée sur : **{target}**")
    
    # Initialisation de l'historique de discussion
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affichage de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur (Modernisée)
    if prompt := st.chat_input(f"Posez votre question sur {target}..."):
        # On affiche le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Appel à l'IA avec sécurité
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Contexte renforcé
            context = f"Tu es le Sage Numérique ENKI. Ton savoir repose sur les Chroniques de Zecharia Sitchin. Analyse spécifiquement : {target}."
            
            with st.spinner("Consultation des archives..."):
                # On vérifie que le prompt n'est pas vide
                if prompt.strip():
                    response = model.generate_content(f"{context}\n\nQuestion : {prompt}")
                    
                    if response.text:
                        full_response = response.text
                        with st.chat_message("assistant"):
                            st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.warning("Le Sage attend une question claire.")
                    
        except Exception as e:
            st.error(f"⚠️ Erreur de transmission : {str(e)}")
            st.info("Astuce : Vérifiez que votre clé API dans 'Secrets' est bien entre guillemets.")

else:
    st.warning("⚔️ En attente de sélection. Choisissez une cible pour éveiller le Sage.")
