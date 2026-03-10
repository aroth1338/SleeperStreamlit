import streamlit as st

st.write("Roster")

st.write(len(st.session_state.players.keys()))
roster = st.session_state.leagues[st.session_state.selected_league]
roster