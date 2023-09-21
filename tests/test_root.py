import pytest
from unittest.mock import patch

from pymojeek import Search


@pytest.fixture
def positive_query():
    return {"include[]": ["tofu"]}


@pytest.fixture
def negative_query():
    return {"include[]": ["tofu"], "exclude[]": ["beef"]}


@pytest.fixture
def equipment_query():
    return {
        "include[]": ["tofu"],
        "exclude[]": ["beef"],
        "equipment[]": ["slow cooker"],
    }


@pytest.fixture
def offset_query():
    return {"include[]": ["tofu"], "offset": 10}


def test_empty_query(client):
    response = client.post("/")

    assert response.status_code == 400


@patch.object(Search, "search")
def test_positive_query(mock_search, positive_query, client):
    response = client.post("/", query_string=positive_query)

    assert response.status_code == 200
    mock_search.assert_called_with("tofu recipes", exclude_words=[])


@patch.object(Search, "search")
def test_negative_query(mock_search, negative_query, client):
    response = client.post("/", query_string=negative_query)

    assert response.status_code == 200
    mock_search.assert_called_with("tofu recipes", exclude_words=["beef"])


@pytest.mark.skip("equipment validation and web search pending openculinary/backend#79")
@patch.object(Search, "search")
def test_equipment_query(mock_search, equipment_query, client):
    response = client.post("/", query_string=equipment_query)

    assert response.status_code == 200
    mock_search.assert_called_with("tofu slow cooker recipes", exclude_words=["beef"])


@patch.object(Search, "search")
def test_offset_query(mock_search, offset_query, client):
    response = client.post("/", query_string=offset_query)

    assert response.status_code == 501
