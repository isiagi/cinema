from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ShowingViewSet

router = DefaultRouter()
router.register(r'showings', ShowingViewSet, basename='showing')

urlpatterns = [
    path('', include(router.urls)),  # Include all API routes
]
