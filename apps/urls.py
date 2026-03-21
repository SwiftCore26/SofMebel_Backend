from django.urls import path

from apps.views.product import ProductListAPIView, CategoryDetailAPIView, ProductDetailAPIView, CategoryListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),
]
