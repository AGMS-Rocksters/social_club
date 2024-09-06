from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from messaging.models import Message, Communication
from rest_framework_simplejwt.tokens import RefreshToken


class CommunicationTests(APITestCase):
    """Test the Communication API views"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test_user@mail.com",
        )
        # Create test communication
        self.communication = Communication.objects.create(
            to_user=self.user, from_user=self.user, status="accepted"
        )
        # URLs to access the communication list and detail
        self.communication_list_url = reverse("messaging:communication-list")
        self.communication_detail_url = reverse(
            "messaging:communication-detail", args=[self.communication.id]
        )

    # Define a helper method to get the JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # Define a helper method to set JWT authentication
    def set_jwt_authentication(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token)

    def test_communication_list(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.get(self.communication_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_communication_detail(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()

        response = self.client.get(self.communication_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["to_user"], self.user.id)
        self.assertEqual(response.data["from_user"], self.user.id)
        self.assertEqual(response.data["status"], "accepted")


class MessageTests(APITestCase):
    """Test the Message API views"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test_user@mail.com",
        )
        # Create test communication
        self.communication = Communication.objects.create(
            to_user=self.user, from_user=self.user, status="accepted"
        )
        # Create test message
        self.message = Message.objects.create(
            communication=self.communication, msg="This is a test message"
        )
        # URLs to access the message list and detail
        self.message_list_url = reverse("messaging:message-list")
        self.message_detail_url = reverse(
            "messaging:message-detail", args=[self.message.id]
        )

    # Define a helper method to get the JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # Define a helper method to set JWT authentication
    def set_jwt_authentication(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token)

    def test_message_list(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.get(self.message_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_message_detail(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.get(self.message_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["msg"], "This is a test message")

    def test_create_message(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.post(
            self.message_list_url,
            {"communication": self.communication.id, "msg": "This is a new message"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(Message.objects.last().msg, "This is a new message")

    def test_update_message(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.put(
            self.message_detail_url,
            {
                "communication": self.communication.id,
                "msg": "This is an updated message",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.last().msg, "This is an updated message")

    def test_delete_message(self):
        # Authenticate the client with JWT
        self.set_jwt_authentication()
        response = self.client.delete(self.message_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)
