
from kombu import Exchange, Queue
import os

DEBUG = True
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
ROOT_URLCONF = 'CapValue.urls'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WSGI_APPLICATION = 'CapValue.wsgi.application'
SECRET_KEY = 'u@nup3l^ofar)mja-h6khvar^%))*$9^j%9q-9hg0#(3xyel=k'
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'authentication.Account'
GRAVATAR_DEFAULT_IMAGE = 'identicon'
GRAVATAR_DEFAULT_SIZE = '215'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.getcwd(), 'static_files')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [os.path.join(BASE_DIR, 'static/templates'), os.path.join(BASE_DIR, 'static_files/templates'), ],
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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE'               : 10,
    'page_size_query_param'   : 'page_size',
    'max_page_size'           : 10000,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'django_gravatar',
    'authentication',
    'djcelery',
    'job',
    'seed',
    'proxies',
    'emails',
    'isp',
    'team'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


if os.environ.get('PRODUCTION') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE'  : 'django.db.backends.mysql',
            'HOST'    : '127.0.0.1',
            'PORT'    : 3306,
            'NAME'    : 'CVC',
            'USER'    : 'soufiaane',
            'PASSWORD': 'soufiane0',
            'OPTIONS' : {
                'autocommit': True,
            },
        }
    }
elif os.environ.get('REMOTE') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME'  : 'db.sqlite3'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE'  : 'django.db.backends.mysql',
            'NAME'    : 'CVC',
            'USER'    : 'soufiaane',
            'PASSWORD': 'soufiane0',
            'HOST'    : 'cvc.ma',
            'PORT'    : '3306',
            'OPTIONS' : {
                'autocommit': True,
            },
        }
    }

CELERY_CONCURRENCY = 8
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'amqp'
CELERYD_HIJACK_ROOT_LOGGER = True
CELERY_HIJACK_ROOT_LOGGER = True
BROKER_URL = 'amqp://soufiaane:C@pV@lue2016@cvc.ma:5672/cvcHost'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
AMQP_SERVER = "cvc.ma"
AMQP_PORT = 5672
AMQP_USER = "soufiaane"
AMQP_PASSWORD = "C@pV@lue2016"
AMQP_VHOST = "/cvcHost"
CELERY_RESULT_SERIALIZER = 'json' #json pickle msgpack
CELERY_TASK_SERIALIZER = 'json'

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('Hotmail', Exchange('Hotmail'), routing_key='Hotmail'),
    Queue('Hotmail', Exchange('fb_crawler'), routing_key='fb_crawler'),
    Queue('Hotmail', Exchange('Temporary'), routing_key='Temporary'),
)
