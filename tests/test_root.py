import pytest


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


@pytest.fixture
def offset_query():
    return {
        'include[]': ['tofu'],
        'offset': 10
    }


def test_empty_query(client):
    response = client.post('/')

    assert response.status_code == 400
