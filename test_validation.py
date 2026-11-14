import pytest
import requests
from unittest.mock import patch
from main import validate_name, validate_email, process_users, fetch_users

@pytest.mark.parametrize("name, expected", [
    ("Matti", True),
    ("", False),
    (" Maija ", True),
    ("   ", False),
    (None, False),
    (123, False),

])
def test_validate_name(name, expected):
    assert validate_name(name) == expected

@pytest.mark.parametrize("email, expected", [
    ("matti@example.com", True),
    ("  maija@example.com  ", True),
    ("matti.example.com", False),
    ("   ", False),
    ("", False),
    (None, False),
    (123, False),
    ("@example.com", False),
    ("matti@", False),
    ("matti@@example.com", False),
    ("matti example@example.com", False),
    ("matti@example", False),
    ("matti@example.", False),
    ("matti@.com", False),
    ("matti testi@example.com", False), 

])    
def test_validate_email(email, expected):
    assert validate_email(email) == expected

def test_process_users_valid(capsys):
    users = [
        {"name": "Matti", "email": "matti@example.com"}
    ]

    process_users(users)

    captured = capsys.readouterr()

    assert "Nimi: Matti" in captured.out
    assert "Sähköposti: matti@example.com" in captured.out    

def test_process_users_invalid_structure(capsys):
    users = {"name": "Matti", "email": "matti@example.com"}
        
    process_users(users)

    captured = capsys.readouterr()

    assert "API palautti virheellisen tietorakenteen" in captured.out

def test_process_users_invalid_user(capsys):
    users = [
        {"name": "Matti", "email": "matti@example.com"},
        None,
        {"name": "Maija", "email": "maija@example.com"}
    ]
        
    process_users(users)

    captured = capsys.readouterr()

    assert "Nimi: Matti" in captured.out
    assert "Virheellinen käyttäjätieto" in captured.out
    assert "Nimi: Maija" in captured.out

def test_fetch_users_success():
    test_users = [
        {"name": "Matti", "email": "matti@example.com"}
    ]

    with patch("main.requests.get") as mock_get:
        mock_get.return_value.json.return_value = test_users

        result = fetch_users()

        assert result == test_users

    mock_get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/users",
        timeout=5
    ) 

def test_fetch_users_http_error():
    # patch() korvaa oikean HTTP-pyynnön
    with patch("main.requests.get") as mock_get:
        # side_effect määrittää nostettavan poikkeuksen
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("500 Server Error")
        )
            # pytest.raises() varmistaa, että fetch_users() nostaa HTTPError-poikkeuksen
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_users()
        # assert_clled_once_with() varmistaa, että HTTP-pyyntö tehtiin oikeilla argumenteilla
        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            timeout=5
        )

def test_fetch_users_timeout_exception():
    with patch("main.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout(
            "Request timed out"
        )
        with pytest.raises(requests.exceptions.Timeout):
            fetch_users()

        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            timeout=5
        )        

def test_fetch_users_invalid_json():
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.json.side_effect = (
            requests.exceptions.JSONDecodeError(
                "Invalid JSON", "invalid", 0
            )
        )        
        with pytest.raises(requests.exceptions.JSONDecodeError):
            fetch_users()

        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            timeout=5
        )    
