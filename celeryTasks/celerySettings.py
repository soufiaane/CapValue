from __future__ import absolute_import

from celery import Celery

app = Celery('CapValue',
             broker='amqp://cvcadmin:CapValue2016@tools.cvc.ma/cvcHost',
             backend='redis://:CapValue2016@tools.cvc.ma:6379/0',
             include=['tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Europe/Oslo',
    CELERY_ENABLE_UTC=True,
)

if __name__ == '__main__':
    app.start()
