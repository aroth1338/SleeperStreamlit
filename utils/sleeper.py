import streamlit as st
import httpx 
from datetime import date
from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx, add_script_run_ctx 
from threading import Thread

@st.dialog(title = "Login", width = "medium", dismissible=False,)
def get_sleeper_leagues():
    """
    Initial dialog window to get username and select a league year.
    """
    
    st.html(
        """
        <style>

            div[data-testid='stVerticalBlock'] {
                gap: 0;
            }

            div[data-testid='stButton'] {
                padding-top: 1rem;
            }

            h3 {
                margin-top: 0;
                margin-bottom: 0;
                padding-top: 1rem;
            }

            label[data-testid="stWidgetLabel"] {
                font-size: 0;
                min-height: 0;
            }

        </style>
        """
    )
    years = [date.today().year - i for i in range(5)]

    st.html("<h3>Sleeper Username</h3>")
    username = st.text_input(
        label = "username",
        placeholder = "Username",
        label_visibility="hidden",
        key = "get_username"
    )

    st.html("<h3>League Year</h3>")
    st.selectbox(
        label = "leagues",
        options = years,
        key = "year_select",
        label_visibility="hidden"
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


def _fetch_players():
    client = httpx.Client(
            base_url="https://api.sleeper.app/v1/players/nfl"
        )
    players = client.get("").json()

    st.session_state['players'] = players
    

def load_sleeper_players(separate_thread = True):
    if separate_thread:
        thread = Thread(
            target = _fetch_players
        )
        add_script_run_ctx(thread, get_script_run_ctx()).start()
    else:
        _fetch_players()
