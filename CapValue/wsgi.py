import os, sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/cvctools')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapValue.settings")

application = get_wsgi_application()
