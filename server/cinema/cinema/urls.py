"""
URL configuration for cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from movies import urls as movie_url
from showing import urls as showing_url
from order import urls as order_url
# from user import urls as user_url

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api_auth', include('rest_framework.urls')),
    path('movies/', include(movie_url)),
    path('showings/', include(showing_url)),
    path('orders/', include(order_url)),
    # path('auth/', include(user_url)),
    path('auth/', include('authentication.urls')),
    # path('auth/', include('rest_framework_simplejwt.urls')),
]
