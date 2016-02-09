from __future__ import absolute_import
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from celery.utils.log import get_task_logger
from selenium import webdriver
from celery import Celery
import time

logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')


@app.task(name='report_hotmail', bind=True, max_retries=5)
def reportHotmail(self, job, email):
    # region Settings
    PROXY = "67.21.35.254:8674"
    ACTIONS = job['actions'].split(',')
    logger.error('Job Started :')
    logger.error('Actions: ' + job['actions'])
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    service_args = ['--proxy=%s' % PROXY, '--proxy-type=http']
    browser = webdriver.Chrome(executable_path="chromedriver")
    browser.maximize_window()

    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)
    # browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)

    def look_for_pub():
        try:
            browser.find_element_by_css_selector('iframe.OutlookAppUpsellFrame')
            script = 'var element1 = document.getElementById("notificationContainer");element1.parentNode.removeChild(element1);\
            var element2 = document.getElementsByClassName("UI_Dialog_BG")[0];element2.parentNode.removeChild(element2);\
            var element3 = document.getElementsByClassName("OutlookAppUpsellFrame")[0];element3.parentNode.removeChild(element3);'
            browser.execute_script(script)
        except Exception:
            print('')

    def waiit():
        try:
            while browser.execute_script('return document.readyState;') != 'complete':
                look_for_pub()
        except:
            pass
    # endregion
    try:
        # region Connection
        link = 'http://www.hotmail.com'
        browser.get(link)
        default_window = browser.window_handles[0]

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

        login_champ.send_keys(email['email'])
        logger.error('Sending Email: ' + email['email'])
        pswd_champ.send_keys(email['password'])
        logger.error('Sending Password: ' + email['password'])
        login_btn.click()
        waiit()
        look_for_pub()
        # endregion

        # region IsVerified ?
        try:
            btn__next_verified = browser.find_element_by_xpath('//*[@value="Suivant"]')
            btn__next_verified.click()
        except NoSuchElementException:
            logger.error('Verification Not needed')
            pass
        waiit()
        look_for_pub()
        junk_url = str(browser.current_url)[:str(browser.current_url).rindex('/')] + '/?fid=fljunk'
        inbox_url = junk_url.replace('fljunk', 'flinbox')
        waiit()
        look_for_pub()
        # endregion

        # region Spam Actions
        try:
            spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
        except Exception:
            spam_count = 0
        logger.error('Total Spam: ' + str(spam_count))

        if spam_count > 0:
            browser.get(junk_url)
            waiit()
            look_for_pub()
            if 'RS' in ACTIONS: # Mark Spam as read
                logger.error('**** Marking SPAM AS READ ****')
                while (not browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()) or spam_count > 0:
                    browser.find_element_by_id('msgChkAll').click()
                    time.sleep(1)
                    logger.error('Select All Messages')
                    browser.find_element_by_xpath('//*[@title=" Autres commandes"]').click()
                    time.sleep(1)
                    logger.error('Click Menu')
                    browser.find_element_by_id('MarkAsRead').click()
                    logger.error('Click Mark As Read')
                    time.sleep(1)
                    if ('NS' in ACTIONS): # Not SPAM
                        logger.error('**** Marking As Not SPAM ****')
                        browser.find_element_by_id('MarkAsNotJunk').click()
                        waiit()
                        look_for_pub()
                        browser.get(junk_url)
                    else:
                        browser.find_element_by_id('nextPageLink').click()
                    try:
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        logger.error('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0

            if ('NS' in ACTIONS) and ('RS' not in ACTIONS): # Not SPAM
                while (not browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()) or spam_count > 0:
                    browser.find_element_by_id('msgChkAll').click()
                    time.sleep(1)
                    browser.find_element_by_id('MarkAsNotJunk').click()
                    waiit()
                    look_for_pub()
                    browser.get(junk_url)
                    waiit()
                    look_for_pub()
                    try:
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        logger.error('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0
            elif ('SS' in ACTIONS) and ('RS' not in ACTIONS) and ('NS' not in ACTIONS): # Mark SPAM as Safe
                try:
                    email_list = browser.find_element_by_css_selector('ul.mailList')
                    emails = email_list.find_elements_by_tag_name('li')
                    emails[0].click()
                    waiit()
                    look_for_pub()
                except Exception:
                    pass
                while spam_count > 0:
                    # Mark Safe
                    try:
                        safe_link = browser.find_element_by_css_selector('a.sfUnjunkItems')
                        safe_link.click()
                    except:
                        pass

                    try:
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        print('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0

                    try:
                        email_list = browser.find_element_by_css_selector('ul.mailList')
                        emails = email_list.find_elements_by_tag_name('li')
                        emails[0].click()
                        waiit()
                        look_for_pub()
                    except Exception:
                        pass
        else:
            logger.error('Nothing to do here : ')
        # endregion

        # region Inbox Actions

        if not str(browser.current_url).endswith('inbox'): browser.get(inbox_url)
        waiit()
        look_for_pub()
        keywork_link = str(browser.current_url)[:str(browser.current_url).index('default.aspx')] + '/?fid=flsearch&srch=1&skws=' + job['keywords'] + '&sdr=4&satt=0'
        browser.get(keywork_link)
        waiit()
        look_for_pub()

        # region Mark inbox as Read
        if 'RI' in ACTIONS: # Mark inbox as Read
            new_link = str(browser.current_url).replace('&sdr=4&satt=0', '&scat=1&sdr=4&satt=0')
            browser.get(new_link)
            waiit()
            look_for_pub()

            try:
                browser.find_element_by_id('NoMsgs')
                no_results = True
            except NoSuchElementException:
                no_results = False

            while not no_results:
                time.sleep(1)
                browser.find_element_by_id('msgChkAll').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@title=" Autres commandes"]').click()
                time.sleep(1)
                browser.find_element_by_id('MarkAsRead').click()
                time.sleep(1)
                browser.get(new_link)
                waiit()
                look_for_pub()
                try:
                    browser.find_element_by_id('NoMsgs')
                    no_results = True
                except NoSuchElementException:
                    no_results = False
                    continue
        # endregion

        # region Add contact Inbox / click Links
        elif ('AC' in ACTIONS) or ('CL' in ACTIONS):  # Add contact Inbox
            try:
                browser.get(keywork_link)
                waiit()
                look_for_pub()
                emails = browser.find_elements_by_css_selector('li.c-MessageRow')
                waiit()
                look_for_pub()
                emails[0].find_elements_by_tag_name('span')[1].click()
                waiit()
                look_for_pub()
                next_btn = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img'))
                next_btn_attributes = next_btn.get_attribute('class')
                last_msg = True if str(next_btn_attributes).endswith('_d') else False
                waiit()
                look_for_pub()

                try:
                    while not last_msg:
                        try:
                            # region Add Contact
                            if 'AC' in ACTIONS:
                                try:
                                    add_contact_link = browser.find_element_by_css_selector('a.AddContact')
                                    add_contact_link.click()
                                    time.sleep(0.5)
                                    print('Contact Added')
                                except NoSuchElementException:
                                    print('Contact Already Exist')
                                    pass
                            # endregion

                            # region Click Links
                            if 'CL' in ACTIONS:
                                body1 = browser.find_element_by_css_selector('div.readMsgBody')
                                body = body1.find_elements_by_tag_name('div')
                                try:
                                    lnk = body[0].find_elements_by_tag_name('a')[1]
                                except Exception:
                                    lnk = None
                                waiit()
                                look_for_pub()
                                if lnk is not None:
                                    lnk.click()
                                    waiit()
                                    browser.switch_to.window(browser.window_handles[1])
                                    print(browser.title)
                                    browser.close()
                                    browser.switch_to.window(browser.window_handles[0])
                                    waiit()
                                    look_for_pub()
                            # endregion

                            waiit()
                            look_for_pub()
                            bod = browser.find_elements_by_tag_name('body')[0]
                            bod.send_keys(Keys.CONTROL + ';')
                            time.sleep(1)
                            waiit()
                            look_for_pub()
                        except NoSuchElementException as nse:
                            print(nse)
                            continue
                        except StaleElementReferenceException as se:
                            print(se)
                            continue
                        finally:
                            time.sleep(1)
                            try:
                                next_btn = browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img')
                            except Exception as x:
                                print(type(x))
                                next_btn = None
                            next_btn_attributes = next_btn.get_attribute('class') if next_btn else ''
                            last_msg = True if str(next_btn_attributes).endswith('_d') else False

                except NoSuchElementException:
                    pass
                except StaleElementReferenceException:
                    pass

            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
            except Exception:
                pass
        # endregion

        # region Flag mail
        elif 'FM' in ACTIONS: # Flag mail
            browser.get(keywork_link)
            waiit()
            look_for_pub()
            last_page = browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()
            last_page_checked = False
            while (not last_page) and (not last_page_checked):
                messages = browser.find_element_by_css_selector('ul.mailList').find_elements_by_tag_name('li')
                for msg in messages:
                    try:
                        flag = msg.find_element_by_css_selector('img.ia_i_p_1')
                        flag.click()
                        time.sleep(0.5)
                    except NoSuchElementException:
                        pass
                last_page_checked = last_page
                browser.find_element_by_id('nextPageLink').click()
                waiit()
                time.sleep(1)
                last_page = browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()
        # endregion

        # endregion

        logger.error('Now What ??')
        browser.get(keywork_link)
        waiit()
        look_for_pub()

    except Exception as exc:
        logger.error(type(exc))

    finally:
        browser.quit()
