import pytest
from unittest.mock import patch
import requests

from src.script import get_highest_hero


@pytest.fixture
def mock_hero_api():
    return [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["6'8", "203 cm"]},
            "work": {
                "occupation": "Musician, adventurer, author; formerly talk show host"
            },
        },
        {
            "id": 2,
            "name": "James Bond",
            "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]},
            "work": {"occupation": "00 Agent"},
        },
        {
            "id": 3,
            "name": "Ajax",
            "appearance": {"gender": "Male", "height": ["6'4", "193 cm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 4,
            "name": "Lightning Lord",
            "appearance": {"gender": "Male", "height": ["6'3", "191 cm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 5,
            "name": "Giganta",
            "appearance": {"gender": "Female", "height": ["205", "62.5 meters"]},
            "work": {
                "occupation": "Criminal, former Scientist, Professor at Ivy University"
            },
        },
        {
            "id": 6,
            "name": "Killer Frost",
            "appearance": {"gender": "Female", "height": ["-", "0 cm"]},
            "work": {"occupation": "Scientist"},
        },
        {
            "id": 7,
            "name": "Light Lass",
            "appearance": {"gender": "Female", "height": ["5'5", "150 cm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 8,
            "name": "Angel Dust",
            "appearance": {"gender": "Female", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"},
        },
    ]


"""Positive cases"""

"""Функция должна корректно обрабатывать валидный input на валидных данных"""


@patch("src.script._get_all_heroes")
def test_get_highest_hero_male_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("Male", True) == (1, "A-Bomb")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_female_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("Female", True) == (5, "Giganta")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_female_not_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("Female", False) == (8, "Angel Dust")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_male_not_working(mock_get_all_heroes, mock_hero_api):
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("Male", False) == (3, "Ajax")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_uppercase_gender(mock_get_all_heroes, mock_hero_api):
    """Функция должна быть не чувствительна к регистру входных данных"""
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("MALE", False) == (3, "Ajax")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_different_height_marks(mock_get_all_heroes):
    """Функция должна обрабатывать различные варианты обозначения сантиметров/метров"""
    mock_get_all_heroes.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 2,
            "name": "James Bond",
            "appearance": {"gender": "Male", "height": ["5'5", "190 Centimeters"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 3,
            "name": "Ajax",
            "appearance": {"gender": "Male", "height": ["5'5", "1.5 m"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 4,
            "name": "Lightning Lord",
            "appearance": {"gender": "Male", "height": ["5'5", "1 Meters"]},
            "work": {"occupation": "-"},
        },
    ]
    assert get_highest_hero("Male", False) == (2, "James Bond")


"""Negative cases"""


@patch("src.script.requests.get")
def test_get_highest_hero_request_error(mock_request_get_error):
    """Функция должна возвращать None при ошибках во время запроса API"""
    mock_request_get_error.side_effect = requests.exceptions.HTTPError

    assert get_highest_hero("Male", False) is None


@patch("src.script._get_all_heroes")
def test_get_highest_hero_name_is_none(mock_get_all_heroes_nameless):
    """Функция должна возвращать 'Nameless hero', если у искомого героя нет имени"""
    mock_get_all_heroes_nameless.return_value = [
        {
            "id": 1,
            "name": "",
            "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"},
        }
    ]
    assert get_highest_hero("Male", False) == (1, "Nameless hero")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_pass_no_height(mock_get_all_heroes_no_height):
    """Функция должна пропускать героев, для которых нет данных о росте"""
    mock_get_all_heroes_no_height.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["-", "-"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 2,
            "name": "Zoom",
            "appearance": {"gender": "Male", "height": ["5'5", "200 cm"]},
            "work": {"occupation": "-"},
        },
    ]
    assert get_highest_hero("Male", False) == (2, "Zoom")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_no_height(mock_get_all_heroes_no_height):
    """При отсутствии данных о росте у всех подходящих героев, возвращается первый в списке"""
    mock_get_all_heroes_no_height.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["-", "-"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 2,
            "name": "Zoom",
            "appearance": {"gender": "Male", "height": ["-", "-"]},
            "work": {"occupation": "-"},
        },
    ]
    assert get_highest_hero("Male", False) == (1, "A-Bomb")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_unknown_gender(mock_get_all_heroes, mock_hero_api):
    """Функция должна возвращать None при нестандартном поле(не Male/Female)"""
    mock_get_all_heroes.return_value = mock_hero_api
    assert get_highest_hero("Unknown", False) is None


@patch("src.script._get_all_heroes")
def test_get_highest_hero_pass_unknown_height_unit(mock_get_all_heroes_unknown_height):
    """Функция должна пропускать героев, чей рост указан в нестандартных единицах измерения(не сантиметры/метры)"""
    mock_get_all_heroes_unknown_height.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["5'5", "165 cm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 2,
            "name": "Zoom",
            "appearance": {"gender": "Male", "height": ["5'5", "200 mm"]},
            "work": {"occupation": "-"},
        },
    ]
    assert get_highest_hero("Male", False) == (1, "A-Bomb")


@patch("src.script._get_all_heroes")
def test_get_highest_hero_unknown_height_unit(mock_get_all_heroes_unknown_height):
    """При отсутствии корректных данных о росте у всех подходящих героев, возвращается первый в списке"""
    mock_get_all_heroes_unknown_height.return_value = [
        {
            "id": 1,
            "name": "A-Bomb",
            "appearance": {"gender": "Male", "height": ["5'5", "165 mm"]},
            "work": {"occupation": "-"},
        },
        {
            "id": 2,
            "name": "Zoom",
            "appearance": {"gender": "Male", "height": ["5'5", "200 mm"]},
            "work": {"occupation": "-"},
        },
    ]
    assert get_highest_hero("Male", False) == (1, "A-Bomb")
