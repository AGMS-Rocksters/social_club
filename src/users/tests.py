from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.test import TestCase
from django.test import Client


class LogoutAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@test.com"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )
        self.logout_url = reverse("users:logout")

    def test_logout(self):
        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_invalid(self):
        response = self.client.post(self.logout_url, {"refresh": "alkgflg8uz0p3qhgq"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_double_logout(self):
        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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


class TestUserInfo(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            username="test_user",
            email="test_user@mail.com",
            password="test_user_password",
        )
        self.user_url = reverse("users:user")
        self.login_url = reverse("users:token_obtain_pair")

    def test_user_info(self):
        login = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "test_user_password",
            },
        )

        access = login.data.get("access")

        response = self.client.get(
            self.user_url, headers={"Authorization": f"Bearer {access}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get("username"),
            "test_user",
        )
        self.assertEqual(
            response.data.get("email"),
            "test_user@mail.com",
        )
        self.assertFalse(response.data.get("seeker"))
        self.assertFalse(response.data.get("helper"))
        self.assertEqual(
            response.data.get("address"),
            None,
        )

    def test_user_delete(self):
        login = self.client.post(
            self.login_url,
            {
                "username": "test_user",
                "password": "test_user_password",
            },
        )

        access = login.data.get("access")

        response = self.client.delete(
            self.user_url, headers={"Authorization": f"Bearer {access}"}
        )

        user = User.objects.filter(username="test_user")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(len(user), 0)


class UserUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser5",
            password="testpassword5",
            email="testuser5@example.com",
        )

        response = self.client.post(
            reverse("users:token_obtain_pair"),
            {"username": "testuser5", "password": "testpassword5"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        self.url = reverse("users:update")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update_email(self):
        data = {"email": "update@test.com"}
        response = self.client.put(self.url, data, format="json")

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, "testuser5")
        self.assertEqual(self.user.email, "update@test.com")
        self.assertEqual(self.user.first_name, "")

    def test_update_empty_request(self):
        data = {}
        response = self.client.put(self.url, data, format="json")

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(self.user.email, "testuser5@example.com")

    def test_update_invalid_email(self):
        data = {"email": "notanemail"}
        response = self.client.put(self.url, data, format="json")

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_required(self):
        self.client.credentials()  # Remove the authentication token
        data = {"first_name": "John"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
