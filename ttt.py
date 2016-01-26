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
            with open("facebook_results.txt", "a") as myfile:
                myfile.write(id + "\n")
            logger.error('Job finished for ' + link + '. ID IS: ' + id)
    except Exception as exc:
        pass
    finally:
        browser.quit()
