from django.db.models import Model, ForeignKey, CASCADE, TextChoices
from django.db.models.fields import (
    IntegerField, CharField, TextField, DecimalField,
    BooleanField, DateTimeField, BigIntegerField,
)

from apps.models.base import TimeBaseModel


class Order(TimeBaseModel):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        REJECTED = 'rejected', 'Rejected'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        FINISHED = 'finished', 'Finished'

    # ── Mijoz ma'lumotlari ──────────────────────────────────────────────────
    full_name   = CharField(max_length=255)
    phone       = CharField(max_length=20)
    message     = TextField(blank=True)
    status      = CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_price = DecimalField(max_digits=12, decimal_places=2, default=0)

    # ── Kim qabul/rad qildi (Telegram) ──────────────────────────────────────
    handler_telegram_id = BigIntegerField(null=True, blank=True, verbose_name="Telegram ID")
    handler_first_name  = CharField(max_length=255, blank=True, verbose_name="Ism")
    handler_last_name   = CharField(max_length=255, blank=True, verbose_name="Familiya")
    handler_username    = CharField(max_length=255, blank=True, verbose_name="Username")
    handled_at          = DateTimeField(null=True, blank=True, verbose_name="Qabul vaqti")

    # ── Telefon holati ───────────────────────────────────────────────────────
    is_called   = BooleanField(default=False, verbose_name="Qo'ng'iroq qilindimi?")
    called_at   = DateTimeField(null=True, blank=True, verbose_name="Qo'ng'iroq vaqti")

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(Model):
    order    = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    product  = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    quantity = IntegerField(default=1)
    price    = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
