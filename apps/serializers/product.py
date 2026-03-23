from rest_framework.fields import SerializerMethodField, CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Product, Category


class ProductModelSerializer(ModelSerializer):
    images = SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        return [img.image.url for img in obj.images.all()]


class CategoryDetailSerializer(ModelSerializer):
    products = ProductModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products']


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ContactSerializer(Serializer):
    name = CharField()
    surname = CharField()
    email = EmailField()
    phone = CharField()
    message = CharField()