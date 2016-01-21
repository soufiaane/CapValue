import copy
import os

from django.core.wsgi import get_wsgi_application
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'Capvalue.settings.SuppressDeprecated'
}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapValue.settings")
application = get_wsgi_application()
