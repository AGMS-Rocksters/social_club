from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.http import Http404
from users.models import User
from drf_spectacular.utils import extend_schema


from users.serializers import (
    CustomObtainPairSerializer,
    UserRegisterSerializer,
    UserInfoSerializer,
    LogoutSerializer,
)


class CustomObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token pair using a custom serializer
    that includes the username.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomObtainPairSerializer


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses=UserRegisterSerializer)
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


class UserView(APIView):
    """
    Retrieve information about currently authenticated user.
    """

    @extend_schema(responses=UserInfoSerializer)
    def get_user(self, request):
        try:
            return User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Http404

    @extend_schema(responses=UserInfoSerializer)
    def get(self, request, format=None):
        user = self.get_user(request=request)

        serializer = UserInfoSerializer(user)

        return Response(serializer.data)

    @extend_schema(responses=UserInfoSerializer)
    def delete(self, request, format=None):
        user = self.get_user(request=request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
