from django.test import TestCase
from django.test import Client
from users.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model


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


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="test_user",
            email="test_user@mail.com",
            password="test_user_password",
        )
        self.login_url = reverse("users:token_obtain_pair")
        self.login_refresh_url = reverse("users:token_refresh")

    def test_login_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "test_user_password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("refresh" in response.data.keys())
        self.assertTrue("access" in response.data.keys())

    def test_login_invalid_username(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "test_user_password",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data.get("detail"),
            "No active account found with the given credentials",
        )

    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "testuserpassword",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data.get("detail"),
            "No active account found with the given credentials",
        )

    def test_refresh_valid_key(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "test_user_password",
            },
        )

        refresh = response.data.get("refresh")

        refresh_request = self.client.post(
            self.login_refresh_url,
            data={"refresh": refresh},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in refresh_request.data.keys())

    def test_refresh_invalid_key(self):
        # TODO: add more "types" of token being invalid
        response = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "test_user_password",
            },
        )

        # To get a JWT token that is invalid
        # for this operation, use the access
        # token instead:
        access = response.data.get("access")

        refresh_request = self.client.post(
            self.login_refresh_url,
            data={"refresh": access},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            refresh_request.data.get("detail"),
            "Token has wrong type",
        )


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="test_user2",
            email="test_user2@mail.com",
            password="test_password",
        )

        self.register_url = reverse("users:register")

    # TODO: maybe add check whether received token is a JWT token
    def test_registration(self):
        response = self.client.post(
            self.register_url,
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
            self.register_url,
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
            self.register_url,
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
            self.register_url,
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


class TestDeleteUser(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="password1234",
            email="testuser@example.com",
        )

        self.client = Client()
        self.client.login(username="testuser", password="password1234")

        self.url = reverse("users:delete_user")

    def test_delete_user_successful(self):
        response = self.client.delete(self.url)
        User = get_user_model()
        self.assertEqual(response.status_code, 401)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_delete_user_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)
