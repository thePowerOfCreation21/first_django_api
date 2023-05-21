"""Tests for models."""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """testing if creating user with email is successful"""

        """user credentials"""
        email = 'email@example.com'
        password = '12345678'

        """creating user"""
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        """checking if user was created successfully"""
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
