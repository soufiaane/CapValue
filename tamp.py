from job.tasks import fb_crawler
from fb_crawler import fb_crawler

file = 'emails_us.csv'
mail = ""

lines = [line.rstrip(b'\n').rstrip(b'\r') for line in open(file, 'rb')]
header = lines[0].decode('ascii')
mails = [lines[x:x + 10000] for x in range(1, len(lines), 10000)]

fb_crawler(file, header, mails[0])
# [fb_crawler.apply_async((file, header, line), queue='fb_crawler') for line in mails]

print(mails)
