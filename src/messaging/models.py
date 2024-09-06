from django.db import models
from users.models import User


class Communication(models.Model):
    """
    The Communication model represents a request for communication between two users.

    Fields:
    - to_user (ForeignKey): The user receiving the communication request.
    - from_user (ForeignKey): The user sending the communication request.
    - status (CharField): The current status of the communication request. Choices are 'pending', 'accepted', 'rejected'.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    to_user = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def accept_communication(self):
        """
        Accepts the communication request by setting the status to 'accepted'.
        """
        self.status = "accepted"
        self.save()

    def reject_communication(self):
        """
        Rejects the communication request by setting the status to 'rejected'.
        """
        self.status = "rejected"
        self.save()

    def is_communication_allowed(self):
        """
        Checks if communication is allowed by verifying if the status is 'accepted'.

        Returns:
        - bool: True if the status is 'accepted', False otherwise.
        """
        return self.status == "accepted"


class Message(models.Model):
    """The Message model represents a message sent within a communication."""

    communication = models.ForeignKey(Communication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()
