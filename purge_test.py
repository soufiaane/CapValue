from __future__ import absolute_import
from celeryTasks.celerySettings import app


@app.task(name='spf_check_task', bind=True)
def spf_check_task(self, reputation, domain):
    print("%s%s" % (reputation, domain))
