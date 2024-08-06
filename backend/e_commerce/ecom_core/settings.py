import os
from datetime import timedelta

from pathlib import Path
from dotenv import load_dotenv

from rest_framework.serializers import Serializer

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zwnn7c841o)_)gbatefjd*01*d54ypos7#ew*4o16w%v^(4and"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # custom apps
    "ecom_user",
    "ecom_user_profile",
    "ecom_admin",
    "product",
    "order",
    # 3rd party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "django_extensions",
    "django_filters",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecom_core.urls"

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

WSGI_APPLICATION = "ecom_core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "e_commerce",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5433",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "ecom_user.EcomUser"

AUTHENTICATION_BACKENDS = [
    "ecom_user.authentication.EcomUserBackend",
    "ecom_admin.authentication.EcomAdminBackend",
]

REST_FRAMEWORK = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "ecom_user.authentication.EcomUserJWTAuthentication",
        "ecom_admin.authentication.EcomAdminJWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKEND": ["django_filters.rest_framework.DjangoFilterBackend"],
    "TOKEN_OBTAIN_SERIALIZER": "ecom_user.jwt.serializers.EcomUserTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "ecom_user.jwt.serializers.EcomUserTokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "ecom_user.jwt.serializers.EcomUserTokenVerifySerializer",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SMS_USERNAME = os.environ.get("SMS_USERNAME")
SMS_PASSWORD = os.environ.get("SMS_PASSWORD")
SMS_SENDER_PHONE_NUMBER = os.environ.get("SMS_PHONE")


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

if None in [REDIS_HOST, REDIS_PORT]:
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6379"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

SHELL_PLUS_SUBCLASSES_IMPORT = [Serializer]

OTP_LENGTH = os.environ.get("OTP_LENGTH")
if not OTP_LENGTH:
    OTP_LENGTH = 6
else:
    try:
        OTP_LENGTH = abs(int(OTP_LENGTH))
    except (ValueError, TypeError):
        raise ValueError("OTP_LENGTH env variable should be a positive integer")

DEFAULT_REQUIRED_SELLER_FIELDS = ["store_name", "store_description", "store_address"]

SPECTACULAR_SETTINGS = {
    "TITLE": "B2C Marketplace platform",
    "DESCRIPTION": """
    A backend web service acting as an intermediary service between sellers and customers where the sellers can create their own shops with their products in it, and the customers can purchase products from an individual shop or using the web service's product listing feature similar to an e-commerce application.
    """,
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'