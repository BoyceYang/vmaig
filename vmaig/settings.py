# !/usr/bin/python
# -*-coding:utf-8-*-

"""
Django settings for vmaig project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y4f8-by)6o2pq)#+=$_@%(q#$+ndh_*vql9d2+54(^j*nwh%hm'

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
    'blog',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vmaig.urls'

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

WSGI_APPLICATION = 'vmaig.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# user model
# AUTH_USER_MODEL = "vmaig_auth.VmaigUser"

# 网站标题等内容配置
WEBSITE_TITLE = u'Vmaig'
WEBSITE_WELCOME = u'欢迎来到Vmaig'

# LOG配置
LOG_FILE = u'./all.log'

LOGGING = {
    u'version': 1,
    u'disable_existing_loggers': True,
    u'filters': {
        u'require_debug_false': {
            u'()': u'django.utils.log.RequireDebugFalse',
        }
    },
    u'formatters': {
        u'simple': {
            u'format': u'[%(levelname)s] %(module)s : %(message)s',
        },
        u'verbose': {
            u'format': u'[%(asctime)s] [%(levelname)s] %(module)s : %(message)s',
        },
    },
    u'handlers': {
        u'null': {
            u'level': u'DEBUG',
            u'class': u'logging.NullHandler',
        },
        u'console': {
            u'level': u'INFO',
            u'class': u'logging.StreamHandler',
            u'formatter': u'verbose',
        },
        u'file': {
            u'level': u'INFO',
            u'class': u'logging.FileHandler',
            u'formatter': u'verbose',
            u'filename': LOG_FILE,
            u'mode': u'a',
        },
        u'mail_admins': {
            u'level': u'ERROR',
            u'class': u'django.utils.log.AdminEmailHandler',
            u'filters': [u'require_debug_false']
        },
    },
    u'loggers': {
        u'': {
            u'handlers': [u'file', u'console'],
            u'level': u'INFO',
            u'propagate': True,
        },
        u'django': {
            u'handlers': [u'file', u'console'],
            u'level': u'DEBUG',
            u'propagate': True,
        },
        u'django.request': {
            u'handlers': [u'mail_admins', u'console'],
            u'level': u'ERROR',
            u'propagate': True,
        },
    },
}

# Cache配置
CACHES = {
    u'default': {
        u'BACKEND': u'django.core.cache.backends.locmem.LocMemCache',
        u'LOCATION': u'unique-snowflake',
        u'options': {
            u'MAX_ENTRIES': 1024,
        },
    },
    u'memcache': {
        u'BACKEND': u'django.core.cache.backends.memcached.MemcachedCache',
        u'LOCATION': u'127.0.0.1:11211',
        u'options': {
            u'MAX_ENTRIES': 1024,
        },
    },
}

# 分页配置
PAGE_NUM = 5
