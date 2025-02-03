from django.contrib import admin
from django.urls import path, include
from movies import urls as movie_url
from showing import urls as showing_url
from order import urls as order_url
from user import urls as user_url

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api_auth', include('rest_framework.urls')),
    path('movies/', include(movie_url)),
    path('showings/', include(showing_url)),
    path('orders/', include(order_url)),
    path('auth/', include(user_url)),
    # path('auth/', include('rest_framework_simplejwt.urls')),
]
