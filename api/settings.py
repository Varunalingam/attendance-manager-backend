"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import environ
import sys


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = BASE_DIR + '/logs'

environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sducb168d75^dhudu9nhig%p25#$u3(r8%8$o4a)q8%&58(al%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG') == 'True')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(processName)s:%(threadName)s][%(filename)s:%(lineno)d][%(asctime)s][%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'general-logfile': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'general_err.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 10,
        },
        'api-info-logfile': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'api_info.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 10,
        },
        'api-err-logfile': {
            'level': 'WARNING',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'api_err.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 10,
        },
        'api-test-logfile': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'api_test.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 10,
        },
        'api-views-logfile': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'api_views.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 10,
        },
        'bot-logfile': {
            'level': 'DEBUG',
            'filename': os.path.join(LOG_DIR, 'bot.log'),
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        },
        'train-logfile': {
            'level': 'DEBUG',
            'filename': os.path.join(LOG_DIR, 'train.log'),
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'ERROR',
            'handlers': ['general-logfile'],
            'propagate': True,
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['console', 'general-logfile'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'general-logfile'],
            'propagate': True,
        },
        '': {
            'level': 'WARNING',
            'handlers': ['api-err-logfile'],
            'propagate': True,
        },
        'api': {
            'level': 'DEBUG',
            'handlers': ['api-info-logfile'],
            'propagate': True
        },
        'api.tests': {
            'level': 'DEBUG',
            'handlers': ['api-test-logfile'],
            'propagate': True
        },
        'api.views': {
            'level': 'DEBUG',
            'handlers': ['api-views-logfile'],
            'propagate': True
        },
        'api.bot': {
            'level': 'DEBUG',
            'handlers': ['console', 'bot-logfile'],
            'propagate': True
        },
        'api.bot.a3c': {
            'level': 'DEBUG',
            'handlers': ['console', 'train-logfile'],
            'propagate': True
        },
    }
}

ALLOWED_HOSTS = ['*']

SESSION_COOKIE_SECURE = False

# CORS rules
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:9000'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attendance_manager',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
            'NAME': os.environ.get('DB_NAME'),
            "USER": os.environ.get('DB_USERNAME'),
            "PASSWORD": os.environ.get('DB_PASSWORD'),
            'OPTIONS': {
                'charset': os.environ.get('DB_CHARSET'),
            }
        }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'attendance_manager.Student'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
