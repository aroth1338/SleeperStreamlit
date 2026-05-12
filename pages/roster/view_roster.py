import streamlit as st
from utils.sleeper import get_rosters
import nflreadpy as nfl
import polars as pl

st.header("Roster")

league_id = st.session_state.leagues[st.session_state.selected_league]['league_id']
all_rosters = get_rosters(league_id)
roster = [x for x in all_rosters if x['owner_id'] == st.session_state.user_id][0]
roster = [st.session_state.players[x] for x in roster['players']]
roster_names = [x["full_name"] for x in roster]

player_data = nfl.load_players()

player_data = player_data.filter(pl.col('display_name').is_in(roster_names)).drop_nulls('short_name').sort("last_name")

st.html(
    """
    <style>
    h3 {
        margin:0;
    }
    </style>
    """
)

def player_card(gsis_id, position):
    player = player_data.filter(pl.col('gsis_id') == gsis_id)
    with st.container(border = True, key = str(gsis_id) + "Card"):
        st.html(
            f"<h3>{player['display_name'].item(0)}</h3>"
        )
        with st.container(horizontal=True, key = str(gsis_id)+"InnerCard"):
            st.image(
                player['headshot'].item(0), 
                width = 125
            )

            st.write("Stats go here?")




from utils.player_stats import __get_position_top_36

__get_position_top_36(st.session_state.selected_league, "WR")

# for row in player_data.iter_rows(named=True):
#     player_card(row['gsis_id'], row['position'])