from decimal import Decimal
import requests
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer

from apps.models import Product, TelegramGroup
from apps.models.order import Order, OrderItem


class OrderItemCreateSerializer(Serializer):
    product_id = IntegerField()
    quantity = IntegerField(min_value=1)


class OrderCreateSerializer(Serializer):
    full_name = CharField(max_length=255)
    phone = CharField(max_length=20)
    message = CharField(required=False, allow_blank=True)
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise ValidationError("Items bo‘sh bo‘lmasligi kerak")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Order yaratish
        order = Order.objects.create(**validated_data)

        # Mahsulotlarni olish
        product_ids = [item['product_id'] for item in items_data]
        products = Product.objects.filter(id__in=product_ids)
        products_dict = {p.id: p for p in products}

        order_items = []
        total = Decimal('0')
        text_items = ""

        for item in items_data:
            product = products_dict.get(item['product_id'])
            if not product:
                raise ValidationError(f"Product {item['product_id']} topilmadi")

            item_total = product.price * item['quantity']
            total += item_total

            text_items += f"\n📦 {product.name} x {item['quantity']} = {item_total}"

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
            )

        # Order totalni saqlash
        order.total_price = total
        order.save()
        OrderItem.objects.bulk_create(order_items)

        # Telegram uchun xabar tayyorlash
        text = f"""
<b>🛒 Yangi buyurtma</b>

<b>👤 Ism:</b> {order.full_name}
<b>📞 Telefon:</b> +{order.phone}

<b>📦 Mahsulotlar:</b>
{text_items}

<b>💰 Jami:</b> {order.total_price}

<b>💬 Izoh:</b> {order.message or '-'}
"""

        # Telegram xabarini barcha guruhlarga yuborish
        groups = TelegramGroup.objects.all()
        for group in groups:
            url = f"https://api.telegram.org/bot{group.bot_token}/sendMessage"
            payload = {
                "chat_id": group.group_id,
                "text": text,
                "parse_mode": "HTML"
            }
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
            except Exception as e:
                print(f"Telegram error for group {group.group_name}: {e}")

        return order