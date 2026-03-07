import streamlit as st
import httpx
from datetime import date
from utils.sleeper import get_sleeper_leagues


if "_initialized" not in st.session_state:
    get_sleeper_leagues()
    st.stop()

st.write(st.session_state.user_info)

st.session_state.leagues
