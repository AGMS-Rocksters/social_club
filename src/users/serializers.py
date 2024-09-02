from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from users.models import User, Address
from rest_framework import serializers


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        return token


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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "postal_code"]


class UserInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ["username", "email", "seeker", "helper", "address"]
