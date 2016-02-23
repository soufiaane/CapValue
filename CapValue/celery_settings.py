from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import django
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flexisettings.settings")
os.environ.setdefault("FLEXI_WRAPPED_MODULE", "CapValue.settings")
django.setup()
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost', backend='redis://:C@pV@lue2016@cvc.ma:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
