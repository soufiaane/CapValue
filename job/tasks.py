from __future__ import absolute_import
from CapValue.celery_settings import app


@app.task(name='report_task')
def reportTask(self, link):
    pass


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, job, email):
    try:
        print("x")
    except Exception:
        self.retry(ex=ex)


@app.task(name='smtp_yahoo', bind=True, max_retries=5)
def smtpYahoo(self, email, password, to):
    pass

@app.task(name='fb_crawler', bind=True, max_retries=5)
def fb_crawler(self, file, header, line, mail):
    pass