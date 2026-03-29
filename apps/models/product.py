from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, DecimalField, ImageField
from django.db.models.fields import FloatField

from apps.models.base import SlugBaseModel


class Category(SlugBaseModel):
    name = CharField(max_length=255)
    image = ImageField(upload_to='categories/')

    def __str__(self):
        return f'{self.name}'


class Product(SlugBaseModel):
    name = CharField(max_length=255)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    rating = FloatField(default=0)

    def __str__(self):
        return f'{self.name}'


class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"
