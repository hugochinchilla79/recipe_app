from decimal import Decimal

from django.test import TestCase

from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "password123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@example.com", "TEST3@example.com"],
            ["test4@example.com", "test4@example.com"],
        ]

        for email in sample_emails:
            user = get_user_model().objects.create_user(
                email=email[0], password="test123"
            )
            self.assertEqual(user.email, email[1])

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="test123"
            )

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a new recipe"""
        user = get_user_model().objects.create_user(
            email="test@example.com", password="test123"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)
