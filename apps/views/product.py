import requests
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filters import ProductFilter
from apps.models import Product, Category
from apps.pagination import CustomPagination
from apps.serializers import ProductModelSerializer, CategoryDetailSerializer, CategoryModelSerializer

from root import settings


@extend_schema(
    tags=['Product-Category'],
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


@extend_schema(
    tags=['Product-Category'],
    request=ProductModelSerializer,
)
class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'


@extend_schema(
    tags=['Product-Category'],
    request=CategoryModelSerializer,
)
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(
    tags=['Product-Category'],
    request=CategoryModelSerializer,
)
class CategoryDetailAPIView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    pagination_class = CustomPagination
