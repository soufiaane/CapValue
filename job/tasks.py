from __future__ import absolute_import
from CapValue.celery_settings import app


@app.task(name='report_task', bind=True)
def reportTask(self, link):
    pass


@app.task(name='report_hotmail', bind=True, max_retries=5)
def reportHotmail(self, job, email):
    pass
