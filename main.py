import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="ENKI v1.4", layout="wide", page_icon="🏛️")

# --- CONNEXION NIBIRU ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ La clé API est absente des Secrets Streamlit.")
    st.stop()

st.title("🏛️ ENKI : Master Archive v1.4")

# --- SÉLECTION ---
target = st.selectbox(
    "Sur quel sujet le Sage doit-il se concentrer ?",
    ["(Choisir)", "Ea (Enki)", "Enlil", "Anu", "4ème Tablette", "Livre d'Enki (Complet)"]
)

if target != "(Choisir)":
    st.info(f"📍 Analyse en cours : **{target}**")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Posez votre question au Sage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # ON UTILISE ICI LE NOM DE MODÈLE LE PLUS COMPATIBLE
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            context = f"Tu es le Sage Anunnaki ENKI. Réponds en te basant sur les Chroniques de Sitchin. Sujet : {target}."
            
            with st.spinner("Consultation des tablettes de cristal..."):
                response = model.generate_content(f"{context}\n\nQuestion : {prompt}")
                
                if response:
                    answer = response.text
                    with st.chat_message("assistant"):
                        st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
        
        except Exception as e:
            st.error(f"⚠️ Erreur de connexion : {e}")
            st.info("Astuce : Si l'erreur 404 persiste, essayez de rafraîchir la page Safari.")
