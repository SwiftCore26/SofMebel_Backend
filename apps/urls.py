from django.urls import path

from apps.views.product import ProductListAPIView, CategoryDetailAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('category/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),

]
