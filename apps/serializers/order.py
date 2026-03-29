from decimal import Decimal

from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer

from apps.models import Product
from apps.models.order import Order, OrderItem
from apps.utils import send_telegram_message


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
            raise ValidationError("Items bo'sh bo'lmasligi kerak")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

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

            price = product.price or Decimal('0')
            quantity = item.get('quantity', 0)
            if quantity is None or not isinstance(quantity, int):
                raise ValidationError(f"Product {product.name} uchun quantity noto'g'ri")

            item_total = price * quantity
            total += item_total
            text_items += f"\n📦 {product.name} x {quantity} = {item_total:,} so'm"

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
            )

        order.total_price = total
        order.save()
        OrderItem.objects.bulk_create(order_items)

        text = (
            f"🛒 <b>Yangi buyurtma #{order.id}</b>\n\n"
            f"👤 <b>Ism:</b> {order.full_name}\n"
            f"📞 <b>Telefon:</b> +{order.phone}\n\n"
            f"📦 <b>Mahsulotlar:</b>{text_items}\n\n"
            f"💰 <b>Jami:</b> {order.total_price:,} so'm\n"
            f"💬 <b>Izoh:</b> {order.message or '-'}"
        )
        send_telegram_message(text)

        return order
