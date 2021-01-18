from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
import json
from api.models import Offer


@pytest.mark.django_db
def test_endpoint_permissions():
    """Ensure unauthenticated users cannot view Photo/OfferPhoto endpoints."""
    photo_list_url = reverse('listview')
    photo_detail_url = reverse('photodetailview', args=[1])
    offerphoto_url = reverse('offerphotos', args=[1])
    client = APIClient()
    endpoints = (photo_list_url, photo_detail_url, offerphoto_url)
    for endpoint in endpoints:
        response = client.get(endpoint, format='json')
        assert (response.status_code == status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
@pytest.mark.usefixtures('make_offerphoto_relation')
def test_offerphoto_view(api_client):
    """Ensures view is accessible by authenticated user, data is in expected format and at least 5 test objects were
    created by the fixture."""

    offerphotos_url = reverse('offerphotos', args=[3])
    response = api_client.get(offerphotos_url)
    data = json.loads(response.content.decode())

    assert response.status_code == status.HTTP_200_OK
    assert data is not None
    assert type(data) == list
    assert len(data) >= 5


@pytest.mark.django_db
@pytest.mark.usefixtures('make_offerphoto_relation')
def test_offer_has_offerphotos(api_client):
    """Ensures offer detail view properly displays a list of at least 5 test Photo URLs"""

    offer = Offer.objects.first()
    offer_url = reverse('detailview', args=[offer.pk])
    response = api_client.get(offer_url)
    data = json.loads(response.content.decode())
    photo_urls = data["photo_urls"]

    assert len(photo_urls) >= 5
