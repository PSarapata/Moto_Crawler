"""Test registration for MotoCrawlerUsers"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_user_registration():
    """Ensure registration works and POST requests are handled correctly."""

    url = reverse('create_user')
    client = APIClient()
    response = client.post(url, {"username": "john.doe", "email": "john@doe.com", "password": "johndoepassword"})
    assert response.status_code == status.HTTP_201_CREATED
