from pathlib import Path
from datetime import timedelta
import dj_database_url

import environ
import os
import logging.handlers

# Initialize Django-environ
env = environ.Env(DEBUG=(bool, False))

# Define a path to your project's .env file (optional)

# Load environment variables from the .env file (if it exists)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = os.path.join(BASE_DIR, ".env")
env.read_env(env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-o!0zjaxwzge&pew%1!h7)yh=n(o(kf*u4vnl_h(9$-)3!1=t9d"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['cinema-vmbf.onrender.com', 'localhost', '127.0.0.1', 'cinema-1-f6rw.onrender.com']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "movies",
    "showing",
    "user",
    "order",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # This should be as high as possible
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
     "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://www.emtcinemas.com',
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "https://cinema-vmbf.onrender.com"
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",

]

MIDDLEWARE.insert(3, "cinema.middlewares.Auth0Middleware")

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "cinema.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

WSGI_APPLICATION = "cinema.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


import environ
import os

# Initialize Django-environ
env = environ.Env(DEBUG=(bool, False))

# Define a path to your project's .env file (optional)
env_file = os.path.join(BASE_DIR, ".env")

FLUTTERWAVE_SECRET_KEY = 'FLWSECK_TEST-0e7756b790368aec82c444801b5cdfbd-X'
FLUTTERWAVE_SECRET_HASH = 'your-webhook-secret-hash'

# Load environment variables from the .env file (if it exists)
env.read_env(env_file)

# import logging
# db_logger = logging.getLogger('django.db.backends')
# db_logger.setLevel(logging.DEBUG)
# db_logger.addHandler(logging.StreamHandler())

# print("Database URL:", env("DATABASE_URL", default="not set"))

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=env("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,  # Explicitly require SSL for Render.com
        conn_health_checks=True,
        
    )
}



AUTH_USER_MODEL = "user.User"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH0
AUTH0_DOMAIN = 'dev-f8y06j0gk5hfjnvf.us.auth0.com'
AUTH0_CLIENT_ID = 'Kgoi1FExAsKNpnBIDq7yQ7OlLyHdmEef'
AUTH0_CLIENT_SECRET = 'Y28r0ZDOcU7VP4r_aPHNRi-wa5OkqEvmYFchpXMB9xRuH5kH1wOMOGweSGBbMKip'


