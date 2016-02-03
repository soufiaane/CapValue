from __future__ import absolute_import
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from celery import Celery
from celery.utils.log import get_task_logger
import os.path

logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')


#@app.task(name='fb_crawler', bind=True, max_retries=5)
def fb_crawler(file, header, lines):
    if not os.path.isfile(file+'[results]'):
        with open(file, "a") as myfile:
            myfile.write(header + ';FB mail\n')

    browser = webdriver.Chrome(executable_path="chromedriver")
    browser.get('https://www.facebook.com/')
    browser.find_element_by_id('email').send_keys('b004.mgh@gmail.com')
    browser.find_element_by_id('pass').send_keys('cvc@2016')
    browser.find_element_by_xpath('//*[@value="Connexion"]').click()
    while browser.execute_script('return document.readyState;') != 'complete':
        pass
    try:
        for line in lines:
            try:
                l = line.decode('ascii')
            except UnicodeDecodeError:
                continue
            try:
                mail = str(l).split(';')[0]
                browser.get('https://www.facebook.com/search/people/?q=' + mail.replace('@', '%40'))
                while browser.execute_script('return document.readyState;') != 'complete':
                    pass
                results = browser.find_element_by_id('all_search_results')
                link = results.find_elements_by_tag_name('a')[0]
                if str(link.get_attribute("href")).startswith('https://www.facebook.com/') and str(link.get_attribute("href")).endswith('?ref=br_rs'):
                    profile = str(link.get_attribute("href")).replace('https://www.facebook.com/', '').replace('?ref=br_rs', '') + '@facebook.com'
                    logger.error(profile)
                    with open(file+'[results]', "a") as myfile:
                        myfile.write(l + ';' + profile + '\n')
            except Exception:
                logger.error('No Results !')
                with open(file+'[results]', "a") as myfile:
                    myfile.write(l + '; \n')
    except NoSuchElementException:
        logger.error('No Results !')
    finally:
        browser.quit()
        # celery -A fb_crawler worker --loglevel=Error -Q fb_crawler --concurrency=1
