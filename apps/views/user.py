from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.permissions import IsAdmin, IsManager
from apps.serializers import ManagerCreateSerializer, LoginSerializer, UserCreateByManagerSerializer


@extend_schema(
    tags=['Auth'],
    request=ManagerCreateSerializer,
    responses={201: ManagerCreateSerializer},
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
    tags=['Auth'],
    request=LoginSerializer,
    responses={200: OpenApiResponse(description="access, refresh, role tokenlar")},
)
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Auth'],
    request=UserCreateByManagerSerializer,
    responses={201: UserCreateByManagerSerializer},
)
class UserCreateByManagerView(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        serializer = UserCreateByManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
