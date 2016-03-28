from __future__ import absolute_import

from celery import Celery

app = Celery('CapValue', broker='amqp://cvcadmin:CapValue2016@192.168.0.166/cvcHost')

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_BACKEND='redis://:CapValue2016@192.168.0.166:6379/0',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYD_POOL_RESTARTS=True,
    CELERYD_PREFETCH_MULTIPLIER=1,
    CELERY_TRACK_STARTED=False,
    CELERY_ACKS_LATE=True
)

if __name__ == '__main__':
    app.start()
