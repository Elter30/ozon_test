import pytest
from unittest.mock import patch, Mock
import requests

from src.script import get_highest_hero

@pytest.fixture
def mock_hero_api():
    return [
        {   
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["6'8","203 cm"]},
            "work": {"occupation": "Musician, adventurer, author; formerly talk show host"}
        },
        {   
            "id": 2,
            "name": "James Bond",
            "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]},
            "work": {"occupation": "00 Agent"}
        },
        {   
            "id": 3,
            "name": "Ajax",
            "appearance": {"gender": "Male", "height": ["6'4", "193 cm"]},
            "work": {"occupation": "-"}
        },
        {   
            "id": 4,
            "name": "Lightning Lord",
            "appearance": {"gender": "Male", "height": ["6'3", "191 cm"]},
            "work": {"occupation": "-"}
        },
        {   
            "id": 5,
            "name": "Giganta",
            "appearance": {"gender": "Female", "height": ["205", "62.5 meters"]},
            "work": {"occupation": "Criminal, former Scientist, Professor at Ivy University"}
        },
        {   
            "id": 6,
            "name": "Killer Frost",
            "appearance": {"gender": "Female", "height": ["-", "0 cm"]},
            "work": {"occupation": "Scientist"}
        },
        {   
            "id": 7,
            "name": "Light Lass",
            "appearance": {"gender": "Female", "height": ["5'5", "150 cm"]},
            "work": {"occupation": "-"}
        },
        {   
            "id": 8,
            "name": "Angel Dust",
            "appearance": {"gender": "Female", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"}
        },
    ]

# def test_convert_height_cm(mock_hero_api):
#     hero = mock_hero_api[0]
#     assert convert_height(hero) == 203.0

# def test_convert_height_meter(mock_hero_api):
#     hero = mock_hero_api[3]
#     assert convert_height(hero) == 6250.0

"""Positive cases"""
@patch("src.script._get_all_heroes")
def test_get_highest_hero_male_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('Male', True) == (1, "A-Bomb")

@patch("src.script._get_all_heroes")
def test_get_highest_hero_female_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('Female', True) == (5, "Giganta")

@patch("src.script._get_all_heroes")
def test_get_highest_hero_female_not_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('Female', False) == (8, "Angel Dust")

@patch("src.script._get_all_heroes")
def test_get_highest_hero_male_not_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('Male', False) == (3, "Ajax")

@patch("src.script._get_all_heroes")
def test_get_highest_hero_uppercase_gender(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('MALE', False) == (3, "Ajax")

"""Negative cases"""
@patch("src.script.requests.get")
def test_get_highest_hero_request_error(mock_request_get_error):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_request_get_error.side_effect = requests.exceptions.HTTPError

    assert get_highest_hero('Male', False) is None

@patch("src.script._get_all_heroes")
def test_get_highest_hero_name_is_none(mock_get_all_heroes_nameless):
    mock_get_all_heroes_nameless.return_value = [{
        "id": 1,
        "name": "",
        "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
        "work": {"occupation": "-"}
    }]
    assert get_highest_hero('Male', False) == (1, "Nameless hero")

@patch("src.script._get_all_heroes")
def test_get_highest_hero_unknown_gender(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero('Unknown', False) is None

@patch("src.script._get_all_heroes")
def test_get_highest_hero_unknown_height_unit(mock_get_all_heroes_unknown_height):
    mock_get_all_heroes_unknown_height.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"}
        },
        {
            "id": 2,
            "name": "B-Bomb",
            "appearance": {"gender": "Male", "height": ["5'5", "200 mm"]},
            "work": {"occupation": "-"}
        }
    ]
    assert get_highest_hero('Male', False) == (1, "A-Bomb")