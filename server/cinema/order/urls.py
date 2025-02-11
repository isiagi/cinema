from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, flutterwave_webhook

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('flutterwave-webhook/', flutterwave_webhook, name='flutterwave-webhook'),
    path('', include(router.urls)),
]
