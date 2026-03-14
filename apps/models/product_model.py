from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, DecimalField, ImageField


class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'



class Product(Model):
    name = CharField(max_length=100)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name}'


class ProductImage(Model):
    product = ForeignKey(Product, CASCADE, related_name='images')
    image = ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"