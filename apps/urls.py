from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.views import (
    CreateOrderAPIView, ProductListAPIView, CategoryDetailAPIView,
    ProductDetailAPIView, CategoryListAPIView, ContactView,
    ManagerCreateView, LoginView, UserCreateByManagerView,
    TelegramWebhookView,
)

urlpatterns = [
    # todo Auth
    path('create-manager/', ManagerCreateView.as_view(), name='admin-manager-create'),
    path('create-user/', UserCreateByManagerView.as_view(), name='manager-user-create'),
    path('login/', LoginView.as_view(), name='login'),

    # todo Order
    path('orders/create/', CreateOrderAPIView.as_view(), name='order-create'),

    # todo Contact
    path("contact/", csrf_exempt(ContactView.as_view()), name="contact"),

    # todo Product Category
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # todo Telegram Webhook
    path('telegram/webhook/<str:bot_token>/', TelegramWebhookView.as_view(), name='telegram-webhook'),

]
