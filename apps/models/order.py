from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import IntegerField, CharField, TextField, DecimalField

from apps.models.base import TimeBaseModel


class Order(TimeBaseModel):
    full_name = CharField(max_length=255)
    phone = CharField(max_length=20)
    message = TextField(blank=True)
    status = CharField(max_length=20, default='pending')
    total_price = DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(Model):
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    quantity = IntegerField(default=1)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
