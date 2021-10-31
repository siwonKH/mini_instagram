import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_FILE_DIRECTORY = r'C:/django_key/secret.txt'

with open(SECRET_FILE_DIRECTORY, encoding='utf-8') as f:
    secret = f.read()
    SECRET_KEY = secret.split('SECRET_KEY')[1].split('=')[1].split(';')[0].replace(" ", '')

    DATABASE_ENGINE = secret.split('DATABASE_ENGINE')[1].split('=')[1].split(';')[0].strip()
    DATABASE_NAME = secret.split('DATABASE_NAME')[1].split('=')[1].split(';')[0].strip()
    DATABASE_USER = secret.split('DATABASE_USER')[1].split('=')[1].split(';')[0].strip()
    DATABASE_PASS = secret.split('DATABASE_PASS')[1].split('=')[1].split(';')[0].strip()
    DATABASE_HOST = secret.split('DATABASE_HOST')[1].split('=')[1].split(';')[0].strip()
    DATABASE_PORT = secret.split('DATABASE_PORT')[1].split('=')[1].split(';')[0].strip()

    EMAIL_HOST = secret.split('EMAIL_HOST')[1].split('=')[1].split(';')[0].strip()
    EMAIL_PORT = secret.split('EMAIL_PORT')[1].split('=')[1].split(';')[0].strip()
    EMAIL_HOST_USER = secret.split('EMAIL_HOST_USER')[1].split('=')[1].split(';')[0].strip()
    EMAIL_HOST_PASSWORD = secret.split('EMAIL_HOST_PASSWORD')[1].split('=')[1].split(';')[0].strip()
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = '미니 인별그램 ' + f'<{EMAIL_HOST_USER}>'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'insta.apps.InstaConfig',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mini_instagram_v1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'mini_instagram_v1.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASS,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, r'insta/media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
LOGIN_URL = '/login'
SESSION_COOKIE_AGE = 86400

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
