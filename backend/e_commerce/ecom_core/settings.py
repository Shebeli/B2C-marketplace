import os
from datetime import timedelta

from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

from rest_framework.serializers import Serializer
from . import ipgs

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"},
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "app.log"),
            "formatter": "standard",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "errors.log"),
            "formatter": "verbose",
        },
        "django_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "order": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

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
    "financeops",
    # 3rd party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "django_extensions",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": "5432",
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

CORS_ALLOWED_ORIGINS = ["https://localhost:5173", "http://localhost:5173"]

CORS_EXPOSE_HEADERS = ["Retry-After", "X-Rate-Limit-Type"]

SMS_USERNAME = os.environ.get("SMS_USERNAME")
SMS_PASSWORD = os.environ.get("SMS_PASSWORD")
SMS_SENDER_PHONE_NUMBER = os.environ.get("SMS_PHONE")


REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

print(f"{REDIS_HOST} {REDIS_PORT}")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

SHELL_PLUS_SUBCLASSES_IMPORT = [Serializer]

OTP_LENGTH = os.environ.get("OTP_LENGTH", 6)
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


if not DEBUG:
    PAYMENT_CALLBACK_URL = os.environ.get("PAYMENT_CALLBACK_URL", None)
else:
    PAYMENT_CALLBACK_URL = "http://localhost:8000/"

if not PAYMENT_CALLBACK_URL:
    raise ImproperlyConfigured(
        "Enviroment variable PAYMENT_CALLBACK_URL should be provided"
    )

# hardcoded for now,
# should be inputted manually by other means such as env variables.
COMMISSION_RATE = 0.975

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_BEAT_SCHEDULE = {
    "check-ipg-status-every-10-minutes": {
        "task": "financeops.tasks.check_and_cache_ipg_status",
        "schedule": 600,
    },
}


# IPG related information
if DEBUG:
    ZIBAL_MERCHANT = "zibal"
else:
    ZIBAL_MERCHANT = os.environ.get("ZIBAL_MERCHANT")
    if not ZIBAL_MERCHANT:
        raise ImproperlyConfigured(
            "ZIBAL_MERCHANT env variable needs to be provided with a value."
        )

IPG_SERVICES_BASE_URL = {
    ipgs.ZIBAL: "https://gateway.zibal.ir/start/",
}
ZIBAL_IPG_IP = ["185.143.233.79"]
IPG_IPS = [ZIBAL_IPG_IP]
IPG_CHOICES = {
    ipgs.ZIBAL: "Zibal",
    ipgs.ASAN_PARDAKHT: "Asan Pardakht",
}

# SMS Cooldown Duration: The duration the user has to wait before
# requesting another verification code for the same phone number,
# in minutes.
SMS_COOLDOWN_DURATION = os.environ.get("SMS_COOLDOWN_DURATION", 2)

# SMS Verification Expiration: For how long a verification code is valid,
# in minutes.
SMS_VERIFY_EXP = os.environ.get("SMS_VERIFY_EXP", 15)
