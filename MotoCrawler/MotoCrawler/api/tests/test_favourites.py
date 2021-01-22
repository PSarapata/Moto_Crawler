from django.urls import reverse
from rest_framework import status
import pytest
import json


@pytest.mark.django_db
@pytest.mark.usefixtures('make_useroffer_relation')
def test_userfavourites_list(api_client):
    """Ensure favourite offer list view displays expected information."""
    url = reverse('favourite_offers-list')
    response = api_client.get(url)
    data = json.loads(response.content.decode())
    results = data["results"][1]
    expected_keys = {
        "id",
        "timestamp",
        "offer"
    }
    print(results)
    assert response.status_code == status.HTTP_200_OK
    assert int(data["count"]) > 0
    assert all(key in results for key in expected_keys)
