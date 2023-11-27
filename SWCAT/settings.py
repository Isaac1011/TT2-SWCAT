"""
Django settings for SWCAT project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import openai
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=n%=9vqpl(3@l)t_9#e6l6r4e8nbm7q)z6chd6!x4_k_(1a!0x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crud',
    'zoom',
    'chatbot'
]

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'SWCAT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SWCAT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swcat_db_v2',
        'USER': 'root',
        'PASSWORD': 'admin77',
        'HOST': 'localhost',  # Puedes cambiarlo si tu base de datos está en un host remoto
        'PORT': '3306',       # Puerto por defecto de MySQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configurar el backend de autenticación
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

LOGIN_URL = '/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_ZOOM_KEY = 'rAbzdBQoSfieaFyUQf2gBA'
SOCIAL_AUTH_ZOOM_SECRET = 'HUCoLXp4bqTYofGgIMTqeMSLYoq0BGDU'
SOCIAL_AUTH_ZOOM_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',  # Esto solicita un token de actualización
}

CORS_ALLOW_ORIGIN = [
    'https://tu-dominio.com',  # Agrega tu dominio aquí
]


TU_ACCESS_TOKEN = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjMwZTVmZmQ5LTYzYjAtNDIwYi1hNjdjLTA1OGU5NmY5ZTYxZCJ9.eyJ2ZXIiOjksImF1aWQiOiJiOWU3N2EwOWQ0ZTBiMmRlYWY0NmMwZTAyNjE1MTdiNSIsImNvZGUiOiJZYldpM3BtUXhic2VqeGNwaDYzU0hTZGJzd3JfUjZvVWciLCJpc3MiOiJ6bTpjaWQ6ckFiemRCUW9TZmllYUZ5VVFmMmdCQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjoyNiwiYXVkIjoiaHR0cHM6Ly9vYXV0aC56b29tLnVzIiwidWlkIjoiYkRxZlVyd2xSbUtiMDR0SWw4NkJrZyIsIm5iZiI6MTcwMTEwNTAwMSwiZXhwIjoxNzAxMTA4NjAxLCJpYXQiOjE3MDExMDUwMDEsImFpZCI6IjFza1FfUVJlVGVxY24yZUVCcHRVeGcifQ.v5fs7OXGV0ny1sBdZWvQi_W56jOi4n5VTwhmgaD3addlhh6ikWDKMv7QIfX6C5XdTfFLXFvYCeeEWLNhvkG3eQ'


openai.api_key = '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'
