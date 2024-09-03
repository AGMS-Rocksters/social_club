from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import (
    CustomObtainPairSerializer,
    UserRegisterSerializer,
    ChangePasswordSerializer,
    UserInfoSerializer,
)


class CustomObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token pair using a custom serializer
    that includes the username.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomObtainPairSerializer


class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        User registration.
        """
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "password2": request.data.get("password2"),
        }
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "User was created"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = "id"


class UserView(APIView):
    """
    Retrieve information about currently authenticated user.
    """

    def get_user(self, request):
        try:
            return User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        user = self.get_user(request=request)

        serializer = UserInfoSerializer(user)

        return Response(serializer.data)

    def delete(self, request, format=None):
        user = self.get_user(request=request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
