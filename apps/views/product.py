from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.filters import ProductFilter
from apps.models import Product, Category
from apps.pagination import CustomPagination
from apps.serializers import ProductModelSerializer, CategoryDetailSerializer, CategoryModelSerializer


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
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'rating']


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryDetailAPIView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    pagination_class = CustomPagination
