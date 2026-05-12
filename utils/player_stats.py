import nflreadpy as nfl
import polars as pl
import streamlit as st

@st.cache_data
def load_weekly_stats(season):
    """Loads weekly nfl stats for all players"""
    weekly_stats = nfl.load_player_stats(seasons=[season])
    weekly_stats = build_fantasy_points_expr(weekly_stats, st.session_state.leagues[st.session_state.selected_league]['scoring_settings'])
    return weekly_stats

def build_fantasy_points_expr(weekly_stats, scoring_settings):
    SLEEPER_TO_NFLREADPY = {
        "pass_yd": "passing_yards",
        "pass_td": "passing_tds",
        "pass_int": "interceptions",
        "pass_2pt": "passing_2pt_conversions",
        "pass_sack": "sacks",
        "rush_yd": "rushing_yards",
        "rush_td": "rushing_tds",
        "rush_2pt": "rushing_2pt_conversions",
        "rush_fd": "rushing_first_downs",
        "rec": "receptions",
        "rec_yd": "receiving_yards",
        "rec_td": "receiving_tds",
        "rec_2pt": "receiving_2pt_conversions",
        "rec_fd": "receiving_first_downs",
        "fum": "fumbles",
        "fum_lost": "fumbles_lost",
        "fum_rec": "fumbles_recovered",
        "fum_rec_td": "fumble_recovery_tds",
        "sack": "sacks",
        "int": "interceptions",
        "ff": "forced_fumbles",
        "def_st_ff": "forced_fumbles",
        "def_st_fum_rec": "fumbles_recovered",
        "def_td": "defensive_tds",
        "def_st_td": "defensive_tds",
        "safe": "safeties",
        "blk_kick": "blocked_kicks",
        "fgm_0_19": "field_goals_made_0_19",
        "fgm_20_29": "field_goals_made_20_29",
        "fgm_30_39": "field_goals_made_30_39",
        "fgm_40_49": "field_goals_made_40_49",
        "fgm_50_59": "field_goals_made_50_59",
        "fgm_60p": "field_goals_made_60_plus",
        "fgmiss": "field_goals_missed",
        "xpm": "extra_points_made",
        "xpmiss": "extra_points_missed",
    }

    expr = None

    for sleeper_stat, multiplier in scoring_settings.items():
        nfl_col = SLEEPER_TO_NFLREADPY.get(sleeper_stat)

        if nfl_col and nfl_col in weekly_stats.columns:
            term = pl.col(nfl_col).fill_null(0) * multiplier
            expr = term if expr is None else expr + term

    weekly_stats = weekly_stats.with_columns(
        league_fantasy_points = expr
    )
    return weekly_stats

def weekly_score_player(player, week):
    """Generates fantasy score for a given player on a selected week using the current league's scoring settings.

    Args:
        player (str): First and last name of player
        week (int): Week number of season

    Returns:
        fantasy_points: Points scored that week for given player.
    """
    weekly_stats = load_weekly_stats(st.session_state.league_year)
    player_stats = weekly_stats.filter(
        (pl.col('player_display_name') == player) & (pl.col('week') == week)
    )
    return player_stats

def positional_points_share(league_name, player_name):
    """Calculates the percentage of fantasy points held by the player in the current season when considering the top 36 players at the position.

    Args:
        league_name (str): Name of league, for league specific scoring
        player_name (str): Name of player
    """

    #Get top 36 at position

    #
    pass

def __get_position_top_36(league_name, position):
    """Gets the top 36 players at the selected position and their fantasy points scored. 

    Args:
        position (str): Name of position (QB, WR, RB, TE)
    """

    weekly_stats = load_weekly_stats(st.session_state.league_year)
    positional_stats = weekly_stats.filter(
        pl.col('position_group') == position
    )

    seasonal_sum = positional_stats.group_by(
        ['player_name', 'season']
    ).agg(
        pl.col('league_fantasy_points').sum().alias('season_points')
    )

    st.write(seasonal_sum)
