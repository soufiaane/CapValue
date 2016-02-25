import json

from tasks import report_hotmail

with open('test.txt') as f:
    lines = f.readlines()
    for line in lines:
        email = json.loads(line.replace('\n', ''))
        report_hotmail.apply_async(('AC', 'reverse mortgage', email), queue='Test')
