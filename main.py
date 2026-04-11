    # ==================================================================================================================================================
    # --- SECTION ARCHIVES AUTOMATIQUES "MES CONTENUS" (TOUJOURS VISIBLE) ---
    st.subheader("📚 Chroniques Manifestées")
    
    if st.session_state.manifested_archives:
        st.caption("Conservation automatique de tes contenus de l'Atelier et de Sora.")
        # Inversion de la liste pour voir les plus récents en haut
        for i, manifested in enumerate(reversed(st.session_state.manifested_archives)):
            with st.expander(f"{manifested['id']} - {manifested['prompt'][:30]}...", expanded=(i == 0)):
                st.caption(f"Manifesté à : {manifested['time']}")
                if manifested['type'] == 'image':
                    st.image(manifested['data'], use_container_width=True)
                    st.download_button(label="📥 Télécharger l'Image PNG", data=manifested['raw_bytes'], file_name=f"{manifested['id']}.png", mime="image/png", use_container_width=True, key=f"dl_arc_{manifested['id']}")
                elif manifested['type'] == 'video':
                    st.video(manifested['data'])
                    st.caption(f"Manifesté par {manifested['engine']}")
        
        if st.button("🧹 Vider les Chroniques de Manifestation"):
            st.session_state.manifested_archives = []
            st.rerun()
    else:
        st.info("📌 Tes images et vidéos générées s'archiveront automatiquement ici.")
        
    st.divider()
    # ==================================================================================================================================================
