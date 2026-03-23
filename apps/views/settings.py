import requests
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.serializers import ContactSerializer
from root import settings


class ContactView(APIView):
    @extend_schema(
        request=ContactSerializer,
        responses={201: None}
    )
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

            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

            requests.post(url, json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": text
            })

            return Response({"status": "sent"}, status=200)

        return Response(serializer.errors, status=400)
