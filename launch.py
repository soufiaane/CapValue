from test import spf_check_task

with open("Top1M Alexa.txt", 'r') as f:
    lines = f.readlines()
    i = 1
    for line in lines:
        domain = line.strip("\n")
        reput = str(i)
        spf_check_task.apply_async((domain, reput), queue="SPF2")
        i += 1
