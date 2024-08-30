from django.test import TestCase
from django.test import Client
from users.models import User


class TestUserModel(TestCase):
    def test_user_creation_valid(self):
        User.objects.create_user(
            username="test_user",
            email="test_user@mail.com",
            password="test_password",
        )
        user = User.objects.get(username="test_user")
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@mail.com")
        self.assertNotEqual(user.password, "test_password")
        self.assertTrue(user.check_password("test_password"))
        self.assertFalse(user.email_verified)
        self.assertFalse(user.seeker)
        self.assertFalse(user.helper)

    def test_user_creation_no_email(self):
        # TODO: add message checks
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="test_user",
                password="test_user_password",
            )

    def test_user_creation_no_password(self):
        # TODO: add message checks
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="test_user",
                email="test_user@mail.com",
            )

    def test_user_creation_no_username(self):
        # TODO: add message checks
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="test_user@mail.com",
                password="test_user_password",
            )


class TestUserEndpoints(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="test_user2",
            email="test_user2@mail.com",
            password="test_password",
        )

    def test_registration(self):
        response = self.client.post(
            "/register/",
            {
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_user_password",
                "password2": "test_user_password",
            },
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.data.get("msg"),
            "User was created",
        )

    def test_registration_different_passwords(self):
        response = self.client.post(
            "/register/",
            {
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_user",
                "password2": "test_user_password",
            },
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            str(response.data.get("non_field_errors")[0]),
            "Entered passwords do not match",
        )

    def test_registration_invalid_email(self):
        response = self.client.post(
            "/register/",
            {
                "username": "test_user",
                "email": "test_user@mail",
                "password": "test_user_password",
                "password2": "test_user_password",
            },
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            str(response.data.get("email")[0]),
            "Enter a valid email address.",
        )

    def test_registration_username_taken(self):
        response = self.client.post(
            "/register/",
            {
                "username": "test_user2",
                "email": "test_user@mail.com",
                "password": "test_user_password",
                "password2": "test_user_password",
            },
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            str(response.data.get("username")[0]),
            "A user with that username already exists.",
        )
