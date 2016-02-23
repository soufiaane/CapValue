from configurations.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapValue.settings")
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
