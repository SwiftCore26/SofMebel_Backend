import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.models import TelegramGroup


class Command(BaseCommand):
    help = "Barcha Telegram botlar uchun webhook o'rnatadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default=None,
            help="Webhook base URL (masalan: https://xxxx.ngrok-free.app). "
                 "Ko'rsatilmasa settings.BASE_URL ishlatiladi.",
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help="Webhookni o'chirish (deleteWebhook)",
        )

    def handle(self, *args, **options):
        base_url = (options['url'] or settings.BASE_URL or '').rstrip('/')

        groups = TelegramGroup.objects.all()
        if not groups.exists():
            self.stdout.write(self.style.WARNING("❗ Hech qanday TelegramGroup topilmadi."))
            return

        for group in groups:
            token = group.bot_token

            if options['delete']:
                self._delete_webhook(token, group.group_name)
            else:
                if not base_url:
                    self.stderr.write(
                        self.style.ERROR(
                            "❌ BASE_URL topilmadi! --url parametrini bering yoki .env ga BASE_URL yozing."
                        )
                    )
                    return
                webhook_url = f"{base_url}/api/v1/telegram/webhook/{token}/"
                self._set_webhook(token, webhook_url, group.group_name)

    def _set_webhook(self, token: str, webhook_url: str, group_name: str):
        url = f"https://api.telegram.org/bot{token}/setWebhook"
        try:
            resp = requests.post(url, json={"url": webhook_url}, timeout=10)
            data = resp.json()
            if data.get("ok"):
                self.stdout.write(
                    self.style.SUCCESS(f"✅ [{group_name}] Webhook o'rnatildi: {webhook_url}")
                )
            else:
                self.stderr.write(
                    self.style.ERROR(f"❌ [{group_name}] Xatolik: {data.get('description')}")
                )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ [{group_name}] So'rov xatosi: {e}"))

    def _delete_webhook(self, token: str, group_name: str):
        url = f"https://api.telegram.org/bot{token}/deleteWebhook"
        try:
            resp = requests.post(url, timeout=10)
            data = resp.json()
            if data.get("ok"):
                self.stdout.write(self.style.SUCCESS(f"✅ [{group_name}] Webhook o'chirildi"))
            else:
                self.stderr.write(self.style.ERROR(f"❌ [{group_name}] {data.get('description')}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ [{group_name}] So'rov xatosi: {e}"))
