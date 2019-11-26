import pytest
from mock import patch

from duckpy import Client


@pytest.fixture
def positive_query():
    return {
        'include[]': ['tofu']
    }


@pytest.fixture
def negative_query():
    return {
        'include[]': ['tofu'],
        'exclude[]': ['beef']
    }


@pytest.fixture
def equipment_query():
    return {
        'include[]': ['tofu'],
        'exclude[]': ['beef'],
        'equipment[]': ['slow cooker']
    }


def test_empty_query(client):
    response = client.post('/')

    assert response.status_code == 400


@patch.object(Client, 'search')
def test_positive_query(mock_search, positive_query, client):
    response = client.post('/', query_string=positive_query)

    assert response.status_code == 200
    mock_search.assert_called_with('tofu recipes')


@patch.object(Client, 'search')
def test_negative_query(mock_search, negative_query, client):
    response = client.post('/', query_string=negative_query)

    assert response.status_code == 200
    mock_search.assert_called_with('tofu -beef recipes')


@patch.object(Client, 'search')
def test_equipment_query(mock_search, equipment_query, client):
    response = client.post('/', query_string=equipment_query)

    assert response.status_code == 200
    mock_search.assert_called_with('tofu -beef slow cooker recipes')
