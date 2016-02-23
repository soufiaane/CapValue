import django.core.handlers.wsgi
import os,sys


application = get_wsgi_application()
application = DjangoWhiteNoise(application)

# sys.path.append('/var/www/cvc.ma')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapValue.settings")
# application = django.core.handlers.wsgi.WSGIHandler()



