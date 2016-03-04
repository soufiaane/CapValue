import os

import dj_database_url
from kombu import Exchange, Queue, serialization

# region Settings
DEBUG = True
SECRET_KEY = "iba5ht!u!_#8r6=lta=mdiux)aqxt37*9j%ijq$t4q4k1s2nbd"
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
# DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'NAME'    : 'cvc',
        'USER': 'cvcadmin',
        'PASSWORD': 'C@pV@Lue2016**-',
        'HOST'    : 'localhost',
        'PORT'    : '',
        'AUTOCOMMIT' : True,
    }
}
# endregion

# region Rest Framework
REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'page_size_query_param': 'page_size',
    'max_page_size': 10000,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
# endregion

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
    'django.core',
    'layout',
    'job',
    'seed',
    'proxy',
    'mail',
    'isp',
    'team',
    'shift',
    'planning',
    'notifications'
    # 'compressor',
    # 'djcelery'
)
# endregion

# region Static Files
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(os.getcwd(), 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [os.path.join(STATIC_ROOT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
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
    'django.middleware.security.SecurityMiddleware',
)
# endregion

"""
class Dev(Configuration):
    # region Settings
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
    # endregion

    # region Rest Framework
    REST_FRAMEWORK = {
        'UNAUTHENTICATED_USER'    : None,
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE'               : 10,
        'page_size_query_param'   : 'page_size',
        'max_page_size'           : 10000,
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        )
    }
    # endregion

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
        'compressor',
        'authentication',
        'djcelery',
        'layout',
        'job',
        'seed',
        'proxy',
        'mail',
        'isp',
        'team',
        'shift',
        'planning'
    )
    # endregion

    # region Static Files
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(os.getcwd(), 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder'
        ,)
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    TEMPLATES = [
        {
            'BACKEND' : 'django.template.backends.django.DjangoTemplates',
            'DIRS'    : [os.path.join(STATIC_ROOT, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS' : {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
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
        'django.middleware.security.SecurityMiddleware',
    )
    # endregion


class Prod(Configuration):
    # region Settings
    DEBUG = False
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
    DATABASES = {'default': {}}
    db_from_env = dj_database_url.config(conn_max_age=500)
    # endregion

    # region Rest Framework
    REST_FRAMEWORK = {
        'UNAUTHENTICATED_USER'    : None,
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE'               : 10,
        'page_size_query_param'   : 'page_size',
        'max_page_size'           : 10000,
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        )
    }
    # endregion

    # region Installed Apps
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'compressor',
        'rest_framework',
        'django_gravatar',
        'rolepermissions',
        'authentication',
        'djcelery',
        'layout',
        'job',
        'seed',
        'proxy',
        'mail',
        'isp',
        'team',
        'shift',
        'planning'
    )
    # endregion

    # region Static Files
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(os.getcwd(), 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    TEMPLATES = [
        {
            'BACKEND' : 'django.template.backends.django.DjangoTemplates',
            'DIRS'    : [os.path.join(STATIC_ROOT, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS' : {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
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
        'django.middleware.security.SecurityMiddleware',
    )
    # endregion


class Test(Configuration):
    # region Settings
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']
    WSGI_APPLICATION = 'CapValue.wsgi.application'
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
    # endregion
"""
