import requests
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.serializers import ContactSerializer
from apps.models import TelegramGroup

from rest_framework.permissions import AllowAny


@extend_schema(
    tags=['Contact'],
    request=ContactSerializer,
    responses={201: None}
)
class ContactView(APIView):
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            text = f"""
📝 Yangi xabar:

👤 Ism: {data['name']} {data['surname']}
📧 Email: {data['email']}
📞 Telefon: {data['phone']}

💬 Xabar:
{data['message']}
"""

            groups = TelegramGroup.objects.all()
            for group in groups:
                url = f"https://api.telegram.org/bot{group.bot_token}/sendMessage"
                payload = {"chat_id": group.group_id, "text": text}
                try:
                    response = requests.post(url, json=payload)
                    response.raise_for_status()
                except Exception as e:
                    print(f"Error sending message to {group.group_name}: {e}")

            return Response({"status": "sent"}, status=201)

        return Response(serializer.errors, status=400)
