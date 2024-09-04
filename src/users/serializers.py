from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers


from users.models import User, Address


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        return token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": "Token expired or invalid",
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


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


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "passwords did not match"})
        return data

    def validate_old_password(self, data):
        user = self.context["request"].user
        if not user.check_password(data):
            raise serializers.ValidationError(
                {"old_password": "old password is not correct"}
            )

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "postal_code"]


class UserInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ["username", "email", "seeker", "helper", "address"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": False},
        }

    def update(self, instance, validated_data):
        # Update only the fields that are present in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
