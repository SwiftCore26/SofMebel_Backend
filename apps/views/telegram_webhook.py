import json
import logging
from datetime import datetime, timezone

import requests
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.models.order import Order
from apps.utils import escape_telegram_html

logger = logging.getLogger(__name__)

ANSWER_CALLBACK_URL = "https://api.telegram.org/bot{token}/answerCallbackQuery"
EDIT_MESSAGE_URL    = "https://api.telegram.org/bot{token}/editMessageText"


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):

    def post(self, request, bot_token):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

        callback_query = data.get("callback_query")
        if not callback_query:
            return JsonResponse({"ok": True})

        callback_id   = callback_query["id"]
        callback_data = callback_query.get("data", "")
        message       = callback_query.get("message", {})
        chat_id       = message.get("chat", {}).get("id")
        message_id    = message.get("message_id")
        tg_user       = callback_query.get("from", {})

        tg_id        = tg_user.get("id")
        first_name   = tg_user.get("first_name", "")
        last_name    = tg_user.get("last_name", "")
        username     = tg_user.get("username", "")
        display_name = f"{first_name} {last_name}".strip() or username or "Noma'lum"
        safe_display_name = escape_telegram_html(display_name)
        safe_username = escape_telegram_html(username)

        now = datetime.now(tz=timezone.utc)

        if callback_data.startswith("accept_order_"):
            order_id   = int(callback_data.split("_")[-1])
            action     = "accept"

        elif callback_data.startswith("reject_order_"):
            order_id   = int(callback_data.split("_")[-1])
            action     = "reject"

        elif callback_data.startswith("called_order_"):
            order_id   = int(callback_data.split("_")[-1])
            action     = "called"

        else:
            self._answer_callback(bot_token, callback_id, "Noma'lum amal")
            return JsonResponse({"ok": True})

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            self._answer_callback(bot_token, callback_id, "❗ Buyurtma topilmadi")
            return JsonResponse({"ok": True})

        original_text = message.get("text", "")

        if action == "accept":
            if order.status != Order.Status.PENDING:
                self._answer_callback(
                    bot_token, callback_id,
                    f"⚠️ Buyurtma allaqachon '{order.get_status_display()}' holatida"
                )
                return JsonResponse({"ok": True})

            order.status             = Order.Status.ACTIVE
            order.handler_telegram_id = tg_id
            order.handler_first_name  = first_name
            order.handler_last_name   = last_name
            order.handler_username    = username
            order.handled_at          = now
            order.save(update_fields=[
                "status", "handler_telegram_id", "handler_first_name",
                "handler_last_name", "handler_username", "handled_at",
            ])

            new_text = (
                f"{original_text}\n\n━━━━━━━━━━━━━━\n"
                f"✅ <b>Qabul qildi:</b> {safe_display_name}"
                + (f" (@{safe_username})" if username else "")
            )
            keyboard = self._called_keyboard(order_id)
            self._edit_message(bot_token, chat_id, message_id, new_text, keyboard)
            self._answer_callback(bot_token, callback_id, "✅ Buyurtma qabul qilindi!", show_alert=True)
        elif action == "reject":
            if order.status in (Order.Status.FINISHED,):
                self._answer_callback(bot_token, callback_id, "⚠️ Bu buyurtmani o'zgartirish mumkin emas")
                return JsonResponse({"ok": True})

            order.status             = Order.Status.REJECTED
            order.handler_telegram_id = tg_id
            order.handler_first_name  = first_name
            order.handler_last_name   = last_name
            order.handler_username    = username
            order.handled_at          = now
            order.save(update_fields=[
                "status", "handler_telegram_id", "handler_first_name",
                "handler_last_name", "handler_username", "handled_at",
            ])

            new_text = (
                f"{original_text}\n\n━━━━━━━━━━━━━━\n"
                f"❌ <b>Bekor qildi:</b> {safe_display_name}"
                + (f" (@{safe_username})" if username else "")
            )
            self._edit_message(bot_token, chat_id, message_id, new_text, keyboard=None)
            self._answer_callback(bot_token, callback_id, "❌ Buyurtma bekor qilindi!", show_alert=True)

        elif action == "called":
            if order.is_called:
                self._answer_callback(bot_token, callback_id, "📞 Qo'ng'iroq allaqachon belgilangan")
                return JsonResponse({"ok": True})

            order.is_called = True
            order.called_at = now
            order.save(update_fields=["is_called", "called_at"])

            new_text = (
                f"{original_text}\n"
                f"📞 <b>Qo'ng'iroq qildi:</b> {safe_display_name}"
                + (f" (@{safe_username})" if username else "")
            )
            self._edit_message(bot_token, chat_id, message_id, new_text, keyboard=None)
            self._answer_callback(bot_token, callback_id, "📞 Qo'ng'iroq belgilandi!", show_alert=True)

        return JsonResponse({"ok": True})

    def _called_keyboard(self, order_id: int) -> dict:
        return {
            "inline_keyboard": [[
                {"text": "📞 Qo'ng'iroq qildim", "callback_data": f"called_order_{order_id}"},
                {"text": "❌ Bekor qilish",       "callback_data": f"reject_order_{order_id}"},
            ]]
        }

    def _answer_callback(self, token, callback_id, text, show_alert=False):
        try:
            requests.post(
                ANSWER_CALLBACK_URL.format(token=token),
                json={"callback_query_id": callback_id, "text": text, "show_alert": show_alert},
                timeout=5,
            )
        except Exception as e:
            logger.error(f"[Webhook] answerCallbackQuery xatolik: {e}")

    def _edit_message(self, token, chat_id, message_id, text, keyboard=None):
        try:
            requests.post(
                EDIT_MESSAGE_URL.format(token=token),
                json={
                    "chat_id":    chat_id,
                    "message_id": message_id,
                    "text":       text,
                    "parse_mode": "HTML",
                    "reply_markup": keyboard if keyboard else {"inline_keyboard": []},
                },
                timeout=5,
            )
        except Exception as e:
            logger.error(f"[Webhook] editMessageText xatolik: {e}")
