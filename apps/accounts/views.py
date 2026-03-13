from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .permissions import IsSuperAdmin
from .serializers import RegisterSerializers, UserSerializers


class AdminCreate(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = UserSerializers(user).data

            return Response(data=user_data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
