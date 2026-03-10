import streamlit as st
from utils.sleeper import get_sleeper_leagues, load_sleeper_players, _fetch_players


if "_initialized" not in st.session_state:
    get_sleeper_leagues()
    st.stop()

if "players" not in st.session_state:
    load_sleeper_players(separate_thread=False)

with st.sidebar:
    st.image(
       f"https://sleepercdn.com/avatars/{st.session_state.user_info['avatar']}",
       width = 120
    )

    st.header(f"Welcome, {st.session_state.user_info['username']}")
    st.session_state.selected_league = st.selectbox(
        label = "**Select a league**",
        options = st.session_state.leagues.keys(),
        key = "league_select"
    )

navi = st.navigation(
    pages = {
        "My Team" : [
            st.Page(
                "pages/roster/view_roster.py", 
                title = "View Roster",
            )
        ],
        "League": [
            st.Page(
                "pages/league/view_league.py", 
                title = "View League",
            )
        ]
    },
    position = "top"
)

navi.run()