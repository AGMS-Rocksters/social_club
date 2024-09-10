from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from messaging.models import Communication  # , Message
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.exceptions import PermissionDenied


class CommunicationTests(APITestCase):
    """Test the Communication API views"""

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
            email="test_user1@mail.com",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            email="test_user2@mail.com",
        )
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
            email="test_user3@mail.com",
        )
        self.recipient_user = User.objects.create_user(
            username="recipient_user",
            password="testpassword",
            email="recipient_user@mail.com",
        )

        # Create test communications
        self.communication1 = Communication.objects.create(
            to_user=self.user1, from_user=self.user2, status="accepted"
        )
        self.communication2 = Communication.objects.create(
            to_user=self.recipient_user, from_user=self.user1, status="accepted"
        )
        self.communication3 = Communication.objects.create(
            to_user=self.recipient_user, from_user=self.user2, status="accepted"
        )
        # URLs to access the communication list and detail
        self.communication_list_url = reverse("messaging:communication-list")
        self.communication_detail_url1 = reverse(
            "messaging:communication-detail", args=[self.communication1.id]
        )
        self.communication_detail_url2 = reverse(
            "messaging:communication-detail", args=[self.communication2.id]
        )

    # Define a helper method to get the JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # Define a helper method to set JWT authentication
    def set_jwt_authentication(self, user):
        jwt_token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt_token)

    def test_communication_list_as_participant(self):
        # Authenticate the client as user2
        self.set_jwt_authentication(self.user2)
        response = self.client.get(self.communication_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user2 should see communications where they are a participant
        self.assertEqual(len(response.data), 2)

    def test_communication_list_as_non_participant(self):
        # Authenticate the client as a user who is not a participant in any communication
        self.set_jwt_authentication(self.user3)
        response = self.client.get(self.communication_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User2 should only see communications where they are a participant
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_communication_detail_as_participant(self):
        # Authenticate the client as user2
        self.set_jwt_authentication(self.user2)
        response = self.client.get(self.communication_detail_url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["to_user"], self.user1.id)
        self.assertEqual(response.data["from_user"], self.user2.id)
        self.assertEqual(response.data["status"], "accepted")

    def test_communication_detail_as_non_participant(self):
        # Authenticate the client as user1 who is not a participant in communication1
        self.set_jwt_authentication(self.user3)
        response = self.client.get(self.communication_detail_url1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_communication_update_as_participant(self):
        # Authenticate the client as user2
        self.set_jwt_authentication(self.user2)
        # Attempt to update communication1, which user2 should not be able to update
        response = self.client.patch(
            self.communication_detail_url1, {"status": "rejected"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure that the communication status has not changed
        self.communication1.refresh_from_db()
        self.assertEqual(self.communication1.status, "accepted")

    def test_communication_update_as_recipient(self):
        # Authenticate the client as the recipient
        self.set_jwt_authentication(self.recipient_user)
        # Perform the PATCH request
        response = self.client.patch(
            self.communication_detail_url2, {"status": "rejected"}
        )
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "rejected")

    def test_communication_update_as_non_participant(self):
        # Authenticate the client as user3 who is not a participant in communication2
        self.set_jwt_authentication(self.user3)
        response = self.client.patch(
            self.communication_detail_url2, {"status": "rejected"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_communication_create(self):
        # Authenticate the client as user1
        self.set_jwt_authentication(self.user1)
        response = self.client.post(
            self.communication_list_url, {"to_user": self.user3.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Communication.objects.count(), 4)
        self.assertEqual(response.data["to_user"], self.user3.id)
        self.assertEqual(response.data["from_user"], self.user1.id)
        self.assertEqual(response.data["status"], "pending")

    def test_perform_destroy_as_participant(self):
        # Authenticate the client as user1
        self.set_jwt_authentication(self.user1)
        response = self.client.delete(self.communication_detail_url2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_perform_destroy_as_non_participant(self):
        # Authenticate the client as user3 who is not a participant in communication2
        self.set_jwt_authentication(self.user3)
        response = self.client.delete(self.communication_detail_url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
