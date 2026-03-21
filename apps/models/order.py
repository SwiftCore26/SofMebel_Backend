from django.db.models import Model, ForeignKey, CASCADE


class Order(Model):
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')

