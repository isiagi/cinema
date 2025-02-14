from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, flutterwave_webhook

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')  # Changed from 'orders' to ''

urlpatterns = [
    path('webhook/', flutterwave_webhook, name='flutterwave-webhook'),  # Made path clearer
    path('', include(router.urls)),
]
