from __future__ import absolute_import
from celery.utils.log import get_task_logger
from selenium import webdriver
from celery import Celery

app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')
logger = get_task_logger(__name__)


@app.task(name='report_task')
def reportTask(link):
    browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
    try:
        browser.get(link)
        id = browser.current_url.replace('https://www.facebook.com/', '')
        if not id.startswith('profile'):
            with open("facebook_results_newlist.txt", "a") as myfile:
                myfile.write(id + "\n")
            logger.error('(*)Job finished for ' + link + '. ID IS: ' + id)
    except Exception:
        pass
    finally:
        browser.quit()


@app.task(name='report_hotmail', bind=True, max_retries=5)
def reportHotmail(self, job, email):
    try:
        print(job.__dict__)
        print(email.__dict__)
        logger.error('Reported Email')
    except Exception as e:
        logger.error("maybe do some clenup here....")
        self.retry(e=e)