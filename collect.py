from test import spf_check_task
from celery.result import AsyncResult

i = 1
with open("spf_jobs_id.txt", 'r') as f:
    for idd in f:
        spf = AsyncResult(idd.replace("\n", "").split(";")[1])
        if spf.state == 'SUCCESS':
            try:
                task_file_results = open("SPF.txt", 'a')
                task_file_results.write("%s\n" % spf.result)
                task_file_results.close()
            except UnicodeEncodeError:
                for character in spf.result:
                    try:
                        task_file_results = open("SPF.txt", 'a')
                        task_file_results.write(character)
                        task_file_results.close()
                    except UnicodeEncodeError:
                        continue
                task_file_results = open("SPF.txt", 'a')
                task_file_results.write("\n")
                task_file_results.close()
        else:
            task_file_results = open("SPF_ERRORS.txt", 'a')
            task_file_results.write(idd)
            task_file_results.close()
