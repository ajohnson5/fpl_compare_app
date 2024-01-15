from gameweek_pipeline.assets.players import get_players, get_gameweeks
import responses

from unittest.mock import patch, Mock
import pytest


valid_players_example = {
    "elements": [
        {
            "chance_of_playing_next_round": 0,
            "chance_of_playing_this_round": 0,
            "code": 232223,
            "cost_change_event": 0,
            "cost_change_event_fall": 0,
            "cost_change_start": -1,
            "cost_change_start_fall": 1,
            "dreamteam_count": 0,
            "element_type": 4,
            "ep_next": "0.0",
            "ep_this": "0.0",
            "event_points": 0,
            "first_name": "Folarin",
            "form": "0.0",
            "id": 1,
            "in_dreamteam": False,
            "news": "Transferred to Monaco",
            "news_added": "2023-08-31T08:55:15.272751Z",
            "now_cost": 44,
            "photo": "232223.jpg",
            "points_per_game": "0.0",
            "second_name": "Balogun",
            "selected_by_percent": "0.2",
            "special": False,
            "squad_number": "",
            "status": "u",
            "team": 1,
            "team_code": 3,
            "total_points": 0,
            "transfers_in": 10024,
            "transfers_in_event": 0,
            "transfers_out": 61915,
            "transfers_out_event": 105,
            "value_form": "0.0",
            "value_season": "0.0",
            "web_name": "Balogun",
            "minutes": 0,
            "goals_scored": 0,
            "assists": 0,
            "clean_sheets": 0,
            "goals_conceded": 0,
            "own_goals": 0,
            "penalties_saved": 0,
            "penalties_missed": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "saves": 0,
            "bonus": 0,
            "bps": 0,
            "influence": "0.0",
            "creativity": "0.0",
            "threat": "0.0",
            "ict_index": "0.0",
            "starts": 0,
            "expected_goals": "0.00",
            "expected_assists": "0.00",
            "expected_goal_involvements": "0.00",
            "expected_goals_conceded": "0.00",
            "influence_rank": 626,
            "influence_rank_type": 61,
            "creativity_rank": 615,
            "creativity_rank_type": 62,
            "threat_rank": 598,
            "threat_rank_type": 61,
            "ict_index_rank": 631,
            "ict_index_rank_type": 63,
            "corners_and_indirect_freekicks_order": "",
            "corners_and_indirect_freekicks_text": "",
            "direct_freekicks_order": "",
            "direct_freekicks_text": "",
            "penalties_order": "",
            "penalties_text": "",
            "expected_goals_per_90": 0,
            "saves_per_90": 0,
            "expected_assists_per_90": 0,
            "expected_goal_involvements_per_90": 0,
            "expected_goals_conceded_per_90": 0,
            "goals_conceded_per_90": 0,
            "now_cost_rank": 524,
            "now_cost_rank_type": 92,
            "form_rank": 570,
            "form_rank_type": 54,
            "points_per_game_rank": 639,
            "points_per_game_rank_type": 66,
            "selected_rank": 327,
            "selected_rank_type": 49,
            "starts_per_90": 0,
            "clean_sheets_per_90": 0,
        },
    ]
}
invalid_players_example = {"detail": []}


valid_gameweeks_example = {
    "elements": [
        {
            "id": 1,
            "stats": {
                "minutes": 0,
                "goals_scored": 0,
                "assists": 0,
                "clean_sheets": 0,
                "goals_conceded": 0,
                "own_goals": 0,
                "penalties_saved": 0,
                "penalties_missed": 0,
                "yellow_cards": 0,
                "red_cards": 0,
                "saves": 0,
                "bonus": 0,
                "bps": 0,
                "influence": "0.0",
                "creativity": "0.0",
                "threat": "0.0",
                "ict_index": "0.0",
                "starts": 0,
                "expected_goals": "0.00",
                "expected_assists": "0.00",
                "expected_goal_involvements": "0.00",
                "expected_goals_conceded": "0.00",
                "total_points": 0,
                "in_dreamteam": False,
            },
            "explain": [
                {
                    "fixture": 193,
                    "stats": [{"identifier": "minutes", "points": 0, "value": 0}],
                }
            ],
        }
    ]
}
invalid_gameweeks_example = {"elements": []}
out_of_bounds_gameweeks_example = {"detail": "Not found."}


@patch("gameweek_pipeline.assets.players.requests.get")
def test_get_players(mock_get):
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = valid_players_example

    extracted_players = get_players(1)

    assert mock_get.called
    assert extracted_players == {
        "1": {
            "first_name": "Folarin",
            "second_name": "Balogun",
            "web_name": "Balogun",
            "team_name": "Arsenal",
            "team_name_short": "ARS",
            "total_points": 0,
            "actual_position": 4,
        }
    }


@patch("gameweek_pipeline.assets.players.requests.get")
def test_get_players_unavailable(mock_get):
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = invalid_players_example

    mock_get.called

    get_gameweeks(1)


@patch("gameweek_pipeline.assets.players.requests.get")
def test_get_gameweek_for_gameweek_unavailable(mock_get):
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = invalid_gameweeks_example

    with pytest.raises(Exception):
        get_gameweeks(-1)


@patch("gameweek_pipeline.assets.players.requests.get")
def test_get_gameweek_for_gameweek_out_of_bounds(mock_get):
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = out_of_bounds_gameweeks_example

    with pytest.raises(Exception):
        get_gameweeks(-1)
