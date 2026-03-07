import streamlit as st
import httpx
from datetime import date

@st.dialog(title = "Login", width = "medium", dismissible=False,)
def get_sleeper_username():

    st.html(
        """
        <style>
            div[data-testid="stHeading"] {
                padding: 0 rem;
            }
        </style>
        """
    )
    years = [date.today().year - i for i in range(5)]

    st.subheader("Sleeper Username")
    username = st.text_input(
        label = "",
        placeholder = "Username",
        label_visibility="hidden",
        key = "get_username"
    )

    st.subheader("League Year")
    st.selectbox(
        label = "",
        options = years,
        key = "year_select"
    )

    with st.columns(5)[-1]:
        fetch_league = st.button(
            label = "Fetch Leagues",
            type = "primary",
            key = "fetch_league_data",
            width = "stretch"
        )
    
    if fetch_league:
        sleeper_client = httpx.Client(
            base_url="https://api.sleeper.app/v1/user/"
        )

        user_info = sleeper_client.get(
            f"{username}"
        )

        if user_info.is_error:
            st.error("Username not recognized by Sleeper.")
        else:
            #save the info
            st.session_state.sleeper_client = sleeper_client
            st.session_state.user_info = user_info.json()
            st.session_state.user_id = st.session_state.user_info['user_id']

            league_data = st.session_state.sleeper_client.get(
                f"{st.session_state.user_id}/leagues/nfl/2025"
            ).json()
            st.session_state.leagues = {
                x['name']: x for x in league_data
            }

            st.session_state._initialized = True
            st.rerun()



if "_initialized" not in st.session_state:
    get_sleeper_username()
    st.stop()

st.write(st.session_state.user_info)

st.session_state.leagues
