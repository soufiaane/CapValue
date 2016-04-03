from tasks import report_hotmail

report_hotmail(actions='SS,AC,FM,CL', subject='M5', email={'login': 'loup_nim2315@outlook.com', 'password': 'capvalue2015'}, proxy=None)
# report_hotmail(actions='SS', subject='Art', email={'login': 'report-serv2@hotmail.com', 'password': 'capvalue2016'}, proxy=None)
# report_hotmail(actions='SS', subject='Art', email={'login': 'test-soufyane26@hotmail.com', 'password': 'capvalue2016'}, proxy=None)

# report_hotmail.apply_async(kwargs={'actions': 'SS,AC,FM,CL', 'subject': 'M5',
#                                    'email': {'login': 'loup_nim2315@outlook.com', 'password': 'capvalue2015'},
#                                    'proxy': None}, queue='abelabbess4')