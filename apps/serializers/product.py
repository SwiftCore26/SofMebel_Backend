from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Category


class ProductModelSerializer(ModelSerializer):
    images = SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [
            request.build_absolute_uri(img.image.url) if request else img.image.url
            for img in obj.images.all()
        ]


class CategoryDetailSerializer(ModelSerializer):
    products = ProductModelSerializer(many=True, read_only=True)
    image = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'products']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class CategoryModelSerializer(ModelSerializer):
    image = SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

