from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user

        user.delete()

        return Response(
            {"message": "Your account has been deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
