from rest_framework import serializers
from messaging.models import Message, Communication


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "communication", "created_at", "msg"]

    def validate(self, data):
        """Check if communication is accepted before sending a message."""
        communication = data.get("communication")
        if not communication.is_communication_allowed():
            raise serializers.ValidationError(
                "Messages can only be sent in accepted communications."
            )
        return data

    def create(self, validated_data):
        """Custom create method if additional logic is required."""
        # You can add custom logic here if needed
        return Message.objects.create(**validated_data)


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = ["id", "to_user", "from_user", "status"]
