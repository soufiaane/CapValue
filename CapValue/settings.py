import os

from kombu import Exchange, Queue

DEBUG = True
TEMPLATE_DEBUG = True
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
ROOT_URLCONF = 'CapValue.urls'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WSGI_APPLICATION = 'CapValue.wsgi.application'
SECRET_KEY = 'u@nup3l^ofar)mja-h6khvar^%))*$9^j%9q-9hg0#(3xyel=k'
ALLOWED_HOSTS = []
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/cvc.ma/static/'
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'static/templates'),)
AUTH_USER_MODEL = 'authentication.Account'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
GRAVATAR_DEFAULT_IMAGE = 'identicon'
GRAVATAR_DEFAULT_SIZE = '215'
ROLEPERMISSIONS_MODULE = 'CapValue.roles'
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGINATE_BY'             : 10
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
    'rest_framework_nested',
    'django_gravatar',
    'authentication',
    'djcelery',
    'job',
    'seed',
    'proxies',
    'emails'
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

if os.environ.get('IS_PRODUCTION') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE'  : 'django.db.backends.mysql',
            'NAME'    : 'CVC',
            'USER'    : 'soufiaane',
            'PASSWORD': 'soufiane0',
            'OPTIONS' : {
                'autocommit': True,
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE'  : 'mysql.connector.django',
            'NAME'    : 'CVC',
            'USER'    : 'soufiaane',
            'PASSWORD': 'soufiane0',
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
BROKER_URL = 'amqp://soufiaane:soufiane0@192.168.1.3:5672/cvchost'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
AMQP_SERVER = "192.168.1.3"
AMQP_PORT = 5672
AMQP_USER = "soufiaane"
AMQP_PASSWORD = "soufiane0"
AMQP_VHOST = "/cvchost"
