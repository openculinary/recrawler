from mock import patch

from duckpy import Client


def test_empty_products(client):
    response = client.post('/')

    assert response.status_code == 400


@patch.object(Client, 'search')
def test_positive_query(mock_search, client):
    response = client.post('/?products[]=tofu')

    assert response.status_code == 200
    mock_search.assert_called_with('tofu recipes')
