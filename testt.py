from test import spf_check_task
from celery.result import AsyncResult
import os

i = 1
with open("domains.txt", 'r') as f:
    for domain in f:
        try:
            spf_task = spf_check_task.apply_async((str(i), domain.replace("\n", "")), queue="SPF")
            task_file_id = open("results_id.txt", 'a')
            task_file_id.write("%s;%s;%s\n" % (str(i), spf_task.id, domain.replace("\n", "")))
            task_file_id.close()
        except Exception as e:
            print(type(e))
        finally:
            i += 1

with open("results_id.txt", 'r') as f:
    for idd in f:
        spf = AsyncResult(idd.replace("\n", "").split(";")[1])
        if spf.state == 'SUCCESS':
            try:
                task_file_results = open("SPF_results.txt", 'a')
                task_file_results.write("%s\n" % spf.result)
                task_file_results.close()
            except UnicodeEncodeError:
                for character in spf.result:
                    try:
                        task_file_results = open("SPF_results.txt", 'a')
                        task_file_results.write(character)
                        task_file_results.close()
                    except UnicodeEncodeError:
                        continue
                task_file_results = open("SPF_results.txt", 'a')
                task_file_results.write("\n")
                task_file_results.close()
        else:
            task_file_results = open("domains_ERRORS.txt", 'a')
            task_file_results.write(idd.replace("\n", "").split(";")[2] + "\n")
            task_file_results.close()

os.remove("results_id.txt")