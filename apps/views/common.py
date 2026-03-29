import requests
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Contact
from apps.serializers import ContactSerializer
from apps.utils import send_telegram_message


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
            contact = serializer.save()  # ✅ DB ga saqlanadi

            text = (
                f"📝 <b>Yangi murojaat</b>\n\n"
                f"👤 <b>Ism:</b> {contact.name} {contact.surname}\n"
                f"📧 <b>Email:</b> {contact.email}\n"
                f"📞 <b>Telefon:</b> {contact.phone}\n\n"
                f"💬 <b>Xabar:</b>\n{contact.message}"
            )
            send_telegram_message(text)  # ✅ utils orqali, parse_mode=HTML

            return Response({"status": "sent"}, status=201)

        return Response(serializer.errors, status=400)
