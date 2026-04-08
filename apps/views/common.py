from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Contact
from apps.serializers import ContactSerializer
from apps.utils import send_telegram_message, escape_telegram_html


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

            safe_name = escape_telegram_html(contact.name)
            safe_surname = escape_telegram_html(contact.surname)
            safe_email = escape_telegram_html(contact.email)
            safe_phone = escape_telegram_html(contact.phone)
            safe_message = escape_telegram_html(contact.message)

            text = (
                f"📝 <b>Yangi murojaat</b>\n\n"
                f"👤 <b>Ism:</b> {safe_name} {safe_surname}\n"
                f"📧 <b>Email:</b> {safe_email}\n"
                f"📞 <b>Telefon:</b> {safe_phone}\n\n"
                f"💬 <b>Xabar:</b>\n{safe_message}"
            )
            send_telegram_message(text)  # ✅ utils orqali, parse_mode=HTML

            return Response({"status": "sent"}, status=201)

        return Response(serializer.errors, status=400)
