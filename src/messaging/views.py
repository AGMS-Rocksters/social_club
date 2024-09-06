from messaging.models import Message, Communication
from messaging.serializers import MessageSerializer, CommunicationSerializer
from rest_framework import generics


class MessageList(generics.ListCreateAPIView):
    """This class handles listing and creating messages in our REST API."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # The validation happens in the serializer, so we just save the message.
        serializer.save()


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """This class handles operations for a single message instance.

    - GET: Retrieve the details of a specific message.
    - PUT: Update the entire message instance.
    - PATCH: Partially update the message instance.
    - DELETE: Remove the specific message instance.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class CommunicationList(generics.ListCreateAPIView):
    """This class handles listing and creating communications in our REST API."""

    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer

    def perform_create(self, serializer):
        # Set the user field to the current user
        serializer.save(user=self.request.user)


class CommunicationDetail(generics.RetrieveUpdateDestroyAPIView):
    """This class handles operations for a single communication instance.

    - GET: Retrieve the details of a specific communication.
    - PUT: Update the entire communication instance.
    - PATCH: Partially update the communication instance.
    - DELETE: Remove the specific communication instance.
    """

    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
