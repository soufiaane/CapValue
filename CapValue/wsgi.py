import os

from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapValue.settings")
from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
