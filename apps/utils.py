import logging
from html import escape
from typing import Any

import requests

from apps.models import TelegramGroup

logger = logging.getLogger(__name__)


def escape_telegram_html(value: Any) -> str:
    if value is None:
        return ""
    return escape(str(value), quote=False)


def send_telegram_message(text: str, parse_mode: str = "HTML", reply_markup: dict = None) -> None:
    groups = TelegramGroup.objects.all()
    for group in groups:
        token = (group.bot_token or "").strip()
        chat_id = (group.group_id or "").strip()
        if not token or not chat_id:
            logger.warning(
                "[Telegram] group='%s' skipped: empty bot_token or group_id",
                group.group_name,
            )
            continue

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error("[Telegram] Timeout: %s", group.group_name)
        except requests.exceptions.HTTPError as e:
            details = ""
            if e.response is not None:
                try:
                    details = e.response.json().get("description") or ""
                except ValueError:
                    details = e.response.text or ""
                details = details.strip()

            if details:
                logger.error("[Telegram] HTTP error %s: %s", group.group_name, details)
            else:
                logger.error("[Telegram] HTTP error %s: %s", group.group_name, e)
        except Exception as e:
            logger.exception("[Telegram] Xatolik %s: %s", group.group_name, e)


def build_order_keyboard(order_id: int) -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "✅ Qabul qilish", "callback_data": f"accept_order_{order_id}"},
                {"text": "❌ Bekor qilish", "callback_data": f"reject_order_{order_id}"},
            ]
        ]
    }
