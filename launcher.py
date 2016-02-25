import json

from tasks import report_hotmail

while True:
    email = json.loads('{"email":"ginny-jwaters@hotmail.com","password":"capvalue2015"}')
    job = report_hotmail.apply_async(('AC', 'reverse mortgage', email), queue='Test')
    while True:
        print(job.status)
