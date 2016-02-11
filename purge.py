from __future__ import absolute_import
from celery.utils.log import get_task_logger
from celery import Celery

logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def reportHotmail(self, job, email):
    pass