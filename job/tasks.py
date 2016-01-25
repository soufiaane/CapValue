from __future__ import absolute_import

from celery.utils.log import get_task_logger

from CapValue.celery_settings import app

logger = get_task_logger(__name__)


@app.task(name='report_task')
def reportTask(self, link):
    print('report_task')
    logger.info('Reported Email')
