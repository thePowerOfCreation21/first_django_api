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

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """Test creating a superuser."""

        """creating user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'sample123'
        )

        """checking if user is superuser"""
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
