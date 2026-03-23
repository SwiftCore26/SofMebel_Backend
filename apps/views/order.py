from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.serializers import OrderCreateSerializer


class CreateOrderAPIView(APIView):
    authentication_classes = []
    permission_classes = (AllowAny,)

    @extend_schema(
        request=OrderCreateSerializer,
        responses={201: None}
    )
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"message": "Order created", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
