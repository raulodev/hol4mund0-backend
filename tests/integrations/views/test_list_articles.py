import pytest


@pytest.mark.django_db
def test_list_articles(client):

    request = client.get("/api/v1/articles/")

    assert request.status_code == 200

    assert request.json() == {"count": 0, "next": None, "previous": None, "results": []}
