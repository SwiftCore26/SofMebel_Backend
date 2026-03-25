from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.serializers import ManagerCreateSerializer, LoginSerializer
from apps.permissions import IsAdmin


@extend_schema(
    tags=['Admin Manager Create'],
    request=ManagerCreateSerializer,
)
class ManagerCreateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = ManagerCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Login API'],
    request=LoginSerializer,
)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
