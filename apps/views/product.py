from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.filters import ProductFilter
from apps.models import Product, Category
from apps.serializers.product import ProductModelSerializer, CategoryDetailSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='category', type=str, description='Category slug'),
        OpenApiParameter(name='min_price', type=int),
        OpenApiParameter(name='max_price', type=int),
        OpenApiParameter(name='product_name', type=str),
    ]
)
class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class CategoryDetailAPIView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
