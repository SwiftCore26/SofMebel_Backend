import requests

from apps.models import TelegramGroup


def send_telegram_message(text: str, parse_mode: str = "HTML", reply_markup: dict = None) -> None:
    groups = TelegramGroup.objects.all()
    for group in groups:
        url = f"https://api.telegram.org/bot{group.bot_token}/sendMessage"
        payload = {
            "chat_id": group.group_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print(f"[Telegram] Timeout: {group.group_name}")
        except requests.exceptions.HTTPError as e:
            print(f"[Telegram] HTTP error {group.group_name}: {e}")
        except Exception as e:
            print(f"[Telegram] Xatolik {group.group_name}: {e}")


def build_order_keyboard(order_id: int) -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "✅ Qabul qilish", "callback_data": f"accept_order_{order_id}"},
                {"text": "❌ Bekor qilish", "callback_data": f"reject_order_{order_id}"},
            ]
        ]
    }
