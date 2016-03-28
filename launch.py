from test import spf_check_task
from celery.result import AsyncResult

i = 1
with open("domains.txt", 'r') as f:
    for domain in f:
        spf_task = spf_check_task.apply_async((str(i), domain.replace("\n", "")), queue="SPF63")
        task_file_id = open("spf_jobs_id.txt", 'a')
        task_file_id.write("%s;%s\n" % (str(i), spf_task.id))
        task_file_id.close()
        i += 1
