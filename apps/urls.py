from django.urls import path

from apps.views.product import ProductListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
]
