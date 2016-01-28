from __future__ import absolute_import
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from celery import Celery
from celery.utils.log import get_task_logger
from selenium.webdriver.support import expected_conditions as EC

logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')


@app.task(name='report_hotmail', bind=True, max_retries=5)
def reportHotmail(self, job_id, job_actions, email, password, **kwargs):
    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
    browser = webdriver.Chrome(executable_path="chromedriver")

    # browser.maximize_window()

    def waiit():
        while browser.execute_script('return document.readyState;') != 'complete':
            pass
        return

    def look_for_pub():
        try:
            close = browser.find_element_by_css_selector('a.close')
            close.click()
        except Exception:
            pass

    try:
        # logger.error('ID: ' + str(job_id) + ' Actions: ' + job_actions + ' Email: ' + email + ' password: ' + password)
        link = 'https://www.outlook.com'
        browser.get(link)

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

        login_champ.send_keys(email)
        pswd_champ.send_keys(password)
        login_btn.click()
        waiit()
        look_for_pub()
        # Goto Junk
        junk_url = str(browser.current_url)[:str(browser.current_url).rindex('/')] + '/?fid=fljunk'
        browser.get(junk_url)
        look_for_pub()
        email_list = browser.find_element_by_css_selector('ul.mailList')
        emails = email_list.find_elements_by_tag_name('li')
        emails[0].click()
        logger.error('Now What ??')

    except Exception as e:
        logger.error('Error')
        self.retry(args=[self, job_id, job_actions, email, password], countdown=2, exc=e, max_retries=5, kwargs=kwargs)

    finally:
        browser.quit()
