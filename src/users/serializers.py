from users.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        """
        Make sure the two passwords submitted match.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Entered passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user
