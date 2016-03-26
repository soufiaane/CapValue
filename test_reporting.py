from tasks import report_hotmail

# report_hotmail(actions='AC,FM,CL', subject='Insurance', email={'login': 'report-serv4@hotmail.com', 'password': 'capvalue2016'}, proxy=None)
# report_hotmail(actions='SS,AC,FM', subject='Art', email={'login': 'report-serv2@hotmail.com', 'password': 'capvalue2016'}, proxy=None)
report_hotmail(actions='RS', subject='Art', email={'login': 'test-soufyane26@hotmail.com', 'password': 'capvalue2016'}, proxy=None)


# report_hotmail.apply_async(kwargs={'actions': 'SS,AC,FM,CL', 'subject': 'Art',
#                                                   'email': {'login': 'test-soufyane26@hotmail.com',
#                                                           'password': 'capvalue2016'}, 'proxy': None}, queue='ikhalladi1')
