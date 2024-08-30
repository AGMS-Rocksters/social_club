from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import CustomObtainPairSerializer


class CustomObtainPairView(TokenObtainPairView):
    """
    Obtain JWT token pair using a custom serializer
    that includes the username.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomObtainPairSerializer
