from django.urls import reverse
from rest_framework import status
import pytest
import json
from api.models import UserFavouriteOffer
from authentication.models import MotoCrawlerUser


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


@pytest.mark.django_db
@pytest.mark.usefixtures('make_useroffer_relation')
def test_userfavourites_detail(api_client):
    """Ensure user can see his favourites and detail view displays expected information."""
    user = MotoCrawlerUser.objects.get(username='john')
    offer = UserFavouriteOffer.objects.filter(user=user)[0]
    url = reverse('favourite_offers-detail', args=[offer.pk])
    response = api_client.get(url)
    data = json.loads(response.content.decode())
    print(data)
    expected_keys = {
        'id',
        'timestamp',
        'offer'
    }
    assert response.status_code == status.HTTP_200_OK
    assert all(key in data for key in expected_keys)
    assert type(data["offer"]) == dict
    assert len(data["offer"].keys()) > 0
