"""Tests for the user API."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public features of user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        request_body = {
            'email': 'testapi@example.com',
            'password': 'testpass1234',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=request_body['email'])
        self.assertTrue(user.check_password(request_body['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with same email exists."""
        request_body = {
            'email': 'testapi@example.com',
            'password': 'testpass1234',
            'name': 'Test Name',
        }

        create_user(**request_body)

        res = self.client.post(CREATE_USER_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 chars."""
        request_body = {
            'email': 'testapi@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model()\
            .objects\
            .filter(
                email=request_body['email']
            )\
            .exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test User',
            'email': 'test_create_token_success@example.com',
            'password': 'test-user-password123'
        }

        create_user(**user_details)

        request_body = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, request_body)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials are invalid."""
        create_user(email='test@example.com', password='goodpass')

        request_body = {
            'email': 'test@example.com',
            'password': 'badpass'
        }

        res = self.client.post(TOKEN_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """Test returns error posting blank password."""
        request_body = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
