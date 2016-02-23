import os

import dj_database_url
from configurations import Configuration
from kombu import Exchange, Queue, serialization


class Dev(Configuration):
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    ROOT_URLCONF = 'CapValue.urls'
    WSGI_APPLICATION = 'CapValue.wsgi.application'
    ALLOWED_HOSTS = ['*']
    AUTH_USER_MODEL = 'authentication.Account'
    GRAVATAR_DEFAULT_IMAGE = 'identicon'
    GRAVATAR_DEFAULT_SIZE = '215'
    ROLEPERMISSIONS_MODULE = 'CapValue.roles'
    DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'CVC', 'USER': 'soufiaane', 'PASSWORD': 'soufiane0', 'HOST': 'cvc.ma', 'PORT': '3306', 'OPTIONS': {'autocommit': True, }, }}
    REST_FRAMEWORK = {'UNAUTHENTICATED_USER': None, 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 10, 'page_size_query_param': 'page_size', 'max_page_size': 10000, 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer',)}

    # region Installed Apps
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'rest_framework',
        'django_gravatar',
        'rolepermissions',
        'authentication',
        'djcelery',
        'job',
        'seed',
        'proxies',
        'emails',
        'isp',
        'team'
    )
    # endregion

    # region MiddleWares
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    # endregion

    # region Static Files
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(os.getcwd(), 'staticfiles')
    STATICFILES_DIRS = ('static',)
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [os.path.join(BASE_DIR, 'static/templates'), ], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', ], }, }, ]
    # endregion

    # region Celery Settings
    CELERY_CONCURRENCY = 1
    CELERY_ACCEPT_CONTENT = ['json']
    # CELERY_RESULT_BACKEND = 'redis://:C@pV@lue2016@cvc.ma:6379/0'
    BROKER_URL = 'amqp://soufiaane:C@pV@lue2016@cvc.ma:5672/cvcHost'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACKS_LATE = True
    CELERYD_PREFETCH_MULTIPLIER = 1

    CELERY_REDIS_HOST = 'cvc.ma'
    CELERY_REDIS_PORT = 6379
    CELERY_REDIS_DB = 0
    CELERY_RESULT_BACKEND = 'redis'
    CELERY_RESULT_PASSWORD = "C@pV@lue2016"
    REDIS_CONNECT_RETRY = True

    AMQP_SERVER = "cvc.ma"
    AMQP_PORT = 5672
    AMQP_USER = "soufiaane"
    AMQP_PASSWORD = "C@pV@lue2016"
    AMQP_VHOST = "/cvcHost"
    CELERYD_HIJACK_ROOT_LOGGER = True
    CELERY_HIJACK_ROOT_LOGGER = True
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('Hotmail', Exchange('Hotmail'), routing_key='Hotmail'),
        Queue('fb_crawler', Exchange('fb_crawler'), routing_key='fb_crawler'),
        Queue('Temporary', Exchange('Temporary'), routing_key='Temporary'),
    )
    # endregion


class Prod(Configuration):
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASES = {'default': {}}
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
    REST_FRAMEWORK = {'UNAUTHENTICATED_USER': None, 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 10, 'page_size_query_param': 'page_size', 'max_page_size': 10000, 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer',)}

    # region Installed Apps
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'rest_framework',
        'django_gravatar',
        'rolepermissions',
        'authentication',
        'djcelery',
        'job',
        'seed',
        'proxies',
        'emails',
        'isp',
        'team'
    )
    # endregion

    # region MiddleWares
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    # endregion

    # region Divers
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    ROOT_URLCONF = 'CapValue.urls'
    WSGI_APPLICATION = 'CapValue.wsgi.application'
    ALLOWED_HOSTS = ['*']
    AUTH_USER_MODEL = 'authentication.Account'
    GRAVATAR_DEFAULT_IMAGE = 'identicon'
    GRAVATAR_DEFAULT_SIZE = '215'
    ROLEPERMISSIONS_MODULE = 'CapValue.roles'
    # endregion

    # region Static Files
    PROJECT_ROOT = BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
    STATIC_ROOT = os.path.join(os.getcwd(), 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [os.path.join(STATIC_ROOT, 'templates'), ], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', ], }, }, ]
    # endregion

    # region Celery Settings
    CELERY_CONCURRENCY = 1
    CELERY_ACCEPT_CONTENT = ['json']
    # CELERY_RESULT_BACKEND = 'redis://:C@pV@lue2016@cvc.ma:6379/0'
    BROKER_URL = 'amqp://soufiaane:C@pV@lue2016@cvc.ma:5672/cvcHost'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACKS_LATE = True
    CELERYD_PREFETCH_MULTIPLIER = 1

    CELERY_REDIS_HOST = 'cvc.ma'
    CELERY_REDIS_PORT = 6379
    CELERY_REDIS_DB = 0
    CELERY_RESULT_BACKEND = 'redis'
    CELERY_RESULT_PASSWORD = "C@pV@lue2016"
    REDIS_CONNECT_RETRY = True

    AMQP_SERVER = "cvc.ma"
    AMQP_PORT = 5672
    AMQP_USER = "soufiaane"
    AMQP_PASSWORD = "C@pV@lue2016"
    AMQP_VHOST = "/cvcHost"
    CELERYD_HIJACK_ROOT_LOGGER = True
    CELERY_HIJACK_ROOT_LOGGER = True
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('Hotmail', Exchange('Hotmail'), routing_key='Hotmail'),
        Queue('fb_crawler', Exchange('fb_crawler'), routing_key='fb_crawler'),
        Queue('Temporary', Exchange('Temporary'), routing_key='Temporary'),
    )
    # endregion


class Test(Configuration):
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
