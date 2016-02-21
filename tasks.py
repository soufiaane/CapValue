# region Imports
from __future__ import absolute_import
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from celery.utils.log import get_task_logger
from selenium.webdriver.common.by import By
from selenium import webdriver
from celery import Celery
import time

# endregion

# region Setup
logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost', backend='redis://:C@pV@lue2016@cvc.ma:6379/0')
app.conf.update(CELERY_ACCEPT_CONTENT=['json'])


# endregion


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, job, email):
    # region Settings
    proxy = "192.154.210.119"
    version = "old"
    wait_timeout = 10
    port = "29954"
    actions = str(job['actions'].split(',')).strip()
    keyword = job['keywords']
    logger.info('Job Started :')
    logger.info('Actions: %s\n' % job['actions'])
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s:%s' % (proxy, port))
    service_args = ['--proxy=%s:%s' % (proxy, port), '--proxy-type=http']
    print(service_args)
    browser = webdriver.Chrome(executable_path="chromedriver")
    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)
    # browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    browser.maximize_window()

    mail = email['email']
    pswd = email['password']
    link = 'http://www.hotmail.com'
    # endregion

    try:

        # region helper Functions
        def look_for_pub():
            try:
                browser.find_element_by_css_selector('iframe.OutlookAppUpsellFrame')
                script = 'var element1 = document.getElementById("notificationContainer");element1.parentNode.removeChild(element1);\
                    var element2 = document.getElementsByClassName("UI_Dialog_BG")[0];element2.parentNode.removeChild(element2);\
                    var element3 = document.getElementsByClassName("OutlookAppUpsellFrame")[0];element3.parentNode.removeChild(element3);'
                browser.execute_script(script)
            except NoSuchElementException:
                pass

        def waiit():
            try:
                look_for_pub()
                while browser.execute_script('return document.readyState;') != 'complete':
                    look_for_pub()
            except Exception as exxc:
                print(type(exxc))
                pass

        # endregion

        # region Connection
        logger.info("(*) Starting Connection")
        logger.info("- Opening Hotmail")
        browser.get(link)

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@name="SI"]')

        login_champ.send_keys(mail)
        logger.info("- Sending Email : %s" % mail)
        pswd_champ.send_keys(pswd)
        logger.info("- Sending Password : %s" % pswd)
        login_btn.click()
        logger.info("- Clicking Login Button")
        waiit()
        look_for_pub()
        logger.info("End Connection\n")
        # endregion

        # region IsVerified ?
        try:
            btn__next_verified = browser.find_element_by_xpath('//*[@value="Suivant"]')
            logger.info("(!) Email needs to be verified")
            btn__next_verified.click()
        except NoSuchElementException:
            pass
        waiit()
        look_for_pub()
        # endregion

        # region Check Version
        logger.info("(!) Checking mail version")
        logger.info("Current URL : %s" % browser.current_url)
        if "outlook" in browser.current_url:
            logger.info("(!) New Version\n")
            version = "new"
        else:
            logger.info("(!) Old Version\n")
        # endregion

        # region Old Version
        if version == "old":
            logger.info("(###) Starting actions for old e-mail version")

            # ***********************************************************************

            # region Spam Actions

            # region Mark Spam as read
            if ('RS' in actions) and ('SS' not in actions):  #

                # region Controllers Settings
                logger.info("(*) Read SPAM Actions")
                waiit()
                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    # logger.info("- Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error("/!\ (Error) Accessink SPAM folder ")
                    logger.error(type(ex))

                try:
                    waiit()
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked = True
                    logger.info("(!) SPAM folder is empty, Skipping read SPAM actions!")
                except NoSuchElementException:
                    waiit()
                    next_page_disabled = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
                    last_page = next_page_disabled.is_displayed()
                    last_page_checked = False
                # endregion

                # region looping through pages
                while not last_page_checked:
                    try:

                        # region Selecting alls messages
                        logger.info("- Marking SPAM as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        # logger.info("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        # logger.info("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        # logger.info("CheckBox is clicked !")
                        # endregion

                        # region Clicking menu
                        # logger.info("Getting Menu Button")

                        try:
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                            waiit()
                            # logger.info("Click Menu")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                            waiit()
                            # TODO-CVC French version
                        except TimeoutException:
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="更多命令"]'))
                            waiit()
                            # logger.info("Click Menu")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="更多命令"]')))
                            waiit()

                        menu_btn.click()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                        # endregion

                        # region Clicking MAR button
                        logger.info("+ Clicking Mark as Read Button")  # TODO-CVC Counter
                        mar_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsRead'))
                        waiit()
                        mar_btn.click()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        except TimeoutException:
                            pass
                        # logger.info("Done !")
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked = last_page if last_page else False
                        next_page_link = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('nextPageLink'))
                        if next_page_link.is_displayed():
                            # logger.info("Accessing Next Page")
                            waiit()
                            next_page_link.click()
                            waiit()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.SelPrompt')))
                        next_page_disabled = browser.find_element_by_css_selector('div.NextPageDisabled')
                        last_page = next_page_disabled.is_displayed()
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as read")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking SPAM as read\n")

            # endregion

            # region Mark as Not SPAM
            if ('NS' in actions) and ('SS' not in actions):  # Not SPAM

                # region Controllers Settings
                logger.info("(*) Mark as Not SPAM Actions")
                waiit()

                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.Error("/!\ (Error) Accessink SPAM folder ")
                    logger.Error(type(ex))

                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                except NoSuchElementException:
                    still_results = True
                # endregion

                # region looping through pages
                while still_results:
                    try:

                        # region Selecting alls messages
                        logger.info("- Marking as not SPAM for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        # logger.info("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        # logger.info("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        # logger.info("CheckBox is clicked !")
                        # endregion

                        # region Clicking MANS button
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                        waiit()
                        not_spam_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                        waiit()
                        not_spam_btn.click()
                        logger.info("(!) 'Not Spam' Button Clicked !")
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        except TimeoutException:
                            pass
                        # endregion

                        # region Checking if it was the last page
                        try:
                            browser.find_element_by_id("NoMsgs")
                            still_results = False
                            logger.info("(!) Last page !")
                        except NoSuchElementException:
                            still_results = True
                            # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.Error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.Error("/!\ (Error) Mark as not SPAM")
                        logger.Error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking e-mails as not spam\n")
            # endregion

            # region Mark SPAM as SAFE
            if 'SS' in actions:

                # region Controllers Settings
                logger.info("(*) Mark SPAM as safe actions :")
                waiit()
                # logger.info("- Getting SPAM Folder")

                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    # logger.info("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error("/!\ (ERROR) Accessink SPAM folder")
                    logger.error(type(ex))

                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                except NoSuchElementException:
                    still_results = True
                # endregion

                # region looping through mails
                while still_results:
                    try:

                        # region Accessing first mail
                        waiit()
                        # logger.info("Getting Email List Group !")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                        email_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                        # logger.info("Getting All Emails from Group")
                        waiit()
                        emails = email_list.find_elements_by_tag_name('li')
                        # logger.info("- Clicking the first e-mail")
                        waiit()
                        emails[0].click()
                        WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer')))
                        waiit()
                        # endregion

                        # region Clicking SS button
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                        safe_link = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('a.sfUnjunkItems'))
                        waiit()
                        safe_link.click()
                        logger.info("- E-mail marked as Safe")  # TODO-CVC
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                        except TimeoutException:
                            pass
                        waiit()
                        # endregion

                        # region Checking if it was the last page
                        try:
                            browser.find_element_by_id("NoMsgs")
                            still_results = False
                            logger.info("(!) Last page !")
                        except NoSuchElementException:
                            still_results = True
                            # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as safe!")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking SPAM as safe\n")
            # endregion

            # endregion

            # ***********************************************************************

            # region Inbox Actions

            # region Mark inbox as Read
            if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):

                # region Controllers Settings
                logger.info("(*) Mark INBOX as read Actions")
                logger.info("- Getting unread messages for Subject: %s" % keyword)
                waiit()

                keyword_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&scat=1&sdr=4&satt=0'
                browser.get(keyword_link)
                waiit()

                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                except NoSuchElementException:
                    still_results = True
                # endregion

                # region Looping through messages
                while still_results:
                    try:

                        # region Selecting alls messages
                        logger.info("- Marking INBOX as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        # logger.info("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        # logger.info("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        # logger.info("CheckBox is clicked !")
                        # endregion

                        # region Clicking menu
                        try:
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                            waiit()
                            # logger.info("Click Menu")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                            waiit()
                            # TODO-CVC French version
                        except TimeoutException:
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="更多命令"]'))
                            waiit()
                            # logger.info("Click Menu")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="更多命令"]')))
                            waiit()
                        menu_btn.click()
                        # endregion

                        # region Clicking MAR button
                        logger.info("- Clicking Mark as Read Button")  # TODO-CVC
                        mar_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsRead'))
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                        mar_btn.click()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        except TimeoutException:
                            pass
                        # logger.info("Done !")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            browser.find_element_by_id("NoMsgs")
                            still_results = False
                            logger.info("(!) Last page !")
                        except NoSuchElementException:
                            still_results = True
                            # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as read")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking INBOX as read\n")
            # endregion

            # region Flag mail
            if ('FM' in actions) and ('AC' not in actions) and ('CL' not in actions):

                # region Controllers Settings
                logger.info("(*) Flag INBOX Actions")
                logger.info("- Getting result for Subject: %s" % keyword)
                waiit()

                keyword_link_flag = WebDriverWait(browser, wait_timeout).until(lambda driver: str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0')
                browser.get(keyword_link_flag)

                try:
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked_flag = True
                except NoSuchElementException:
                    waiit()
                    next_page_disabled_flag = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
                    last_page_flag = next_page_disabled_flag.is_displayed()
                    last_page_checked_flag = False
                # endregion

                # region Looping through pages
                while not last_page_checked_flag:
                    try:

                        # region Selecting alls messages
                        logger.info("- Flaging Mails for this Page !")
                        waiit()
                        messages_ul = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                        waiit()
                        messages = messages_ul.find_elements_by_tag_name('li')
                        # endregion

                        # region Clicking through messages
                        for i in range(len(messages)):
                            try:
                                flag = messages[i].find_element_by_css_selector('img.ia_i_p_1')
                                waiit()
                                flag.click()  # TODO-CVC Count this
                                waiit()
                                time.sleep(1)
                                logger.info("- E-mail flagged")
                            except NoSuchElementException:
                                pass
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked_flag = last_page_flag if last_page_flag else False
                        next_page_link = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('nextPageLink'))
                        if next_page_link.is_displayed():
                            waiit()
                            next_page_link.click()
                            waiit()
                            logger.info("(!) Accessing Next Page")
                            try:
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            except TimeoutException:
                                pass
                        next_page_disabled_flag = browser.find_element_by_css_selector('div.NextPageDisabled')
                        last_page_flag = next_page_disabled_flag.is_displayed()
                        logger.info("Last page : %s" % last_page_flag)
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Flag INBOX  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done Flaging Mails\n")
            # endregion

            # region Add Contact  / Click Links / Flag Mail
            if ('AC' in actions) or ('CL' in actions):

                # region Controllers Settings
                logger.info("(*) Add Contact / Click Links / Flag Mail Actions: ")
                # logger.info("- Open Mail per Mil for Actions !")
                logger.info("- Getting result for Subject : %s" % keyword)
                waiit()

                keyword_link_ac = WebDriverWait(browser, wait_timeout).until(lambda driver: str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0')
                browser.get(keyword_link_ac)

                try:
                    waiit()
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked_ac = True
                    logger.info("(!) INBOX folder is empty")
                    logger.info("(!) Skipping Add Contact / Click Links / Flag Mail actions")
                except NoSuchElementException:
                    waiit()
                    next_page_disabled_ac = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
                    last_page_ac = next_page_disabled_ac.is_displayed()
                    last_page_checked_ac = False
                # endregion

                # region Accessing first mail!
                if not last_page_checked_ac:
                    waiit()
                    # logger.info("Getting Email List Group !")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                    email_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                    # logger.info("Getting All Emails from Group")
                    waiit()
                    emails = email_list.find_elements_by_tag_name('li')
                    # logger.info("Clicking the First Email")
                    waiit()
                    time.sleep(1)
                    emails[0].click()
                    WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer')))
                    waiit()
                # endregion

                # region Looping through mails
                while not last_page_checked_ac:
                    try:

                        # region Flag Mail
                        if 'FM' in actions:
                            try:
                                # logger.info("Flag Mail Action :")
                                # logger.info("Getting Flag Mail")
                                waiit()
                                message_header = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_css_selector('div.MessageHeaderItem'))
                                waiit()
                                flag = message_header[3].find_element_by_css_selector('img.ia_i_p_1')
                                # logger.info("Clicking Flag !")
                                flag.click()
                                time.sleep(1)
                                waiit()
                                logger.info("- E-mail Flagged !")  # TODO-CVC To count
                            except NoSuchElementException:
                                logger.warning("(!) Email already Flagged !")
                                pass
                            except Exception as ex:
                                logger.info("/!\ (Error) Flag mail !")
                                logger.info(type(ex))
                        # endregion

                        # region Trust email Content
                        try:
                            # logger.info("Trust Email Content")
                            safe_btn = browser.find_element_by_css_selector('a.sfMarkAsSafe')
                            waiit()
                            safe_btn.click()
                            logger.info("- E-mail content trusted !")
                            waiit()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfMarkAsSafe')))
                        except NoSuchElementException:
                            # logger.info("Email Content is Safe")
                            pass
                        except Exception as ex:
                            logger.error("/!\ (Error) Trust Email Error !")
                            logger.info(type(ex))
                        # endregion

                        # region Add Contact
                        if 'AC' in actions:
                            # logger.info("Add to Contact Action :")
                            try:
                                waiit()
                                # logger.info("Getting 'Add to Contact' Link")
                                add_contact_link = browser.find_element_by_css_selector('a.AddContact')
                                # logger.info("Clicking 'Add to Contact' Link")
                                waiit()

                                if (str(add_contact_link.text) == "Add to contacts") or (str(add_contact_link.text) == "Ajouter aux contacts") or (str(add_contact_link.text) == "添加至联系人"):
                                    add_contact_link.click()
                                    logger.info("- From-Email added to contacts")
                                    waiit()
                                    try:
                                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                        WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                    except TimeoutException:
                                        pass
                            except NoSuchElementException:
                                # logger.info("Link Not Found !")
                                logger.warning('(!) Contact Already Exist')
                                pass
                            except Exception as ex:
                                logger.error("/!\ (Error) Add Contact")
                                logger.error(type(ex))
                        # endregion

                        # region Click Links
                        if 'CL' in actions:
                            waiit()
                            # logger.info("Clicking the Link Action :")
                            # logger.info("Getting the Mail 'Body'")
                            body1 = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.readMsgBody'))
                            body = body1.find_elements_by_tag_name('div')
                            try:
                                # logger.info("Getting the Link in the Mail !")
                                lnk = body[0].find_elements_by_tag_name('a')[1]
                            except Exception as ex:
                                logger.warning("(!) Link Not Found")
                                lnk = None
                                logger.info(type(ex))
                            waiit()
                            if lnk is not None:
                                try:
                                    # logger.info("link is Found : %s" % lnk.get_attribute('href'))
                                    waiit()
                                    # logger.info("Clicking the Link")
                                    lnk.click()
                                    logger.info("- Link clicked ! ==> (%s)" % lnk.get_attribute('href'))
                                    WebDriverWait(browser, wait_timeout).until(lambda driver: len(browser.window_handles) > 1)
                                    # logger.info("New Tab Opened !")
                                    waiit()
                                    # logger.info("Switching to the new Tab !")
                                    browser.switch_to.window(browser.window_handles[1])
                                    waiit()
                                    # logger.info("Link Loaded")
                                    # logger.info("Closing !")
                                    browser.close()
                                    waiit()
                                    # logger.info("Going Back to Hotmail !")
                                    browser.switch_to.window(browser.window_handles[0])
                                    waiit()
                                except Exception as ex:
                                    logger.error("/!\ (Error) Switching to new Tab")
                                    logger.error(type(ex))
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked_ac = last_page_ac if last_page_ac else False
                        next_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('a.rmNext'))
                        waiit()
                        next_btn_img = next_btn.find_element_by_tag_name('img')
                        waiit()
                        next_btn_attributes = next_btn_img.get_attribute('class')
                        waiit()
                        if str(next_btn_attributes).endswith('_d'):
                            last_page_ac = True
                            logger.info("(!) Last page")
                        else:
                            last_page_ac = False
                        waiit()
                        if not last_page_ac:
                            logger.info("(!) Getting next e-mail ...")
                            bod = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_tag_name('body'))
                            waiit()
                            bod[0].send_keys(Keys.CONTROL + '.')
                            waiit()
                        time.sleep(1)
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ -(Error) Add Contact / Click Links / Flag Mail Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Add Contact and/or Click Links Error !")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done Add Contact / Click Links / Flag Mail\n")
                # endregion
                # endregion

                # ***********************************************************************
        # endregion

        # ***********************************************************************

        # region New Version
        elif version == "new":
            logger.info("(###) Starting actions for EW e-mail version")

            # region Configure Mail BOX
            try:
                waiit()
                preview_pane = browser.find_element_by_css_selector("div.vResize")
                if preview_pane.is_displayed():
                    # logger.info("- Mailbox not yet configured !")
                    # logger.info("- Configureing !")
                    # logger.info("- Getting settings button")
                    settings_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id("O365_MainLink_Settings"))
                    waiit()
                    # logger.info("- Clicking settings button")
                    settings_btn.click()
                    # logger.info("- Waiting for menu to show")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.o365cs-nav-contextMenu")))
                    # logger.info("- Getting display settings")
                    display_settings = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Display settings"]'))
                    waiit()
                    # logger.info("- Clicking display settings")
                    display_settings.click()
                    # logger.info("- Waiting for display settings to shows")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
                    # logger.info("- Getting Hide reading pane option")
                    hide_pane = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Hide reading pane"]'))
                    waiit()
                    # logger.info("- Clicking Hide reading pane option")
                    hide_pane.click()
                    time.sleep(1)
                    # logger.info("- Getting save button")
                    ok_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Save"]'))
                    waiit()
                    # logger.info("- Clicking save button")
                    ok_btn.click()
                    # logger.info("- Waiting for Settings pane to fade away")
                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
                    # else:
                    # logger.info("- Mailbox already configured !")
            except NoSuchElementException:
                # logger.info("- Mailbox already configured !")
                pass
            except Exception as ex:
                logger.error("/!\ (Error) Check Display Settings")
                logger.error(type(ex))
            # logger.info("- Done configuring mailbox !\n")
            # endregion

            # ***********************************************************************

            # region Spam Actions

            # region Mark Spam as read
            if ('RS' in actions) and ('SS' not in actions):
                logger.warning("/!\ Mark SPAM as read are disabled for new version of mailboxes !")
                logger.warning("/!\ Skipping marking SPAM as read !\n")
            # endregion

            # region Mark as Not SPAM
            if ('NS' in actions) and ('SS' not in actions):  # Not SPAM

                # region Controllers Settings
                logger.info("(*) Mark as not SPAM action")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing SPAM folder
                try:
                    # logger.info("- Getting SPAM folder")
                    waiit()
                    # logger.info("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error("/!\ (Error) Accessink SPAM folder")
                    logger.error(type(ex))
                # endregion

                # region Checking results
                spam_count = 0
                try:
                    waiit()
                    # logger.info("Getting spam Count")
                    # logger.info("Getting Junk span")
                    junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    # logger.info("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error("/!\ (Error) Getting SPAM Count")
                    logger.error(type(ex))
                    spam_count = 0
                finally:
                    logger.info("(!) SPAM count is : %s" % str(spam_count))  # TODO-CVC to Count
                # endregion

                # endregion

                # region looping through pages
                while spam_count > 0:
                    try:

                        # region Selecting alls messages
                        logger.info("(!) Marking SPAM as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        # logger.info("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                        waiit()
                        # logger.info("Select all Msgs")
                        # logger.info("Defining hover action")
                        hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                        # logger.info("Hover over the checkbox")
                        hover.perform()
                        # logger.info("Hover Done")
                        # logger.info("Waiting for visibility")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        # logger.info("Element is visible")
                        # logger.info("Clicking Checkbox")
                        chk_bx_bttn.find_element_by_tag_name("button").click()
                        waiit()
                        # endregion

                        # region Clicking MANS button
                        try:
                            # logger.info("Clicking Mark as not SPAM Button")
                            # logger.info("Getting MANS button")
                            mans_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                            waiit()
                            # logger.info("Waiting for MANS button")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                            # logger.info("Clicking MANS button")
                            mans_btn.click()
                            # logger.info("Waiting for action to be performed")
                            WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/div[1]/span').text == "Junk Email")
                            # logger.info("Sending ESC key")
                            ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                            # logger.info("Waiting for invisibility of element !")
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                            logger.info("- E-mail marked as not SPAM !")
                        except TimeoutException:
                            pass
                        # logger.info("Done !")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            # logger.info("Getting spam Count")
                            # logger.info("Getting Junk span")
                            junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                            # logger.info("%s" % junk_span.text)
                            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            spam_count = 0
                        except Exception as ex:
                            logger.error("/!\ (Error) Getting SPAM Count")
                            logger.error(type(ex))
                            spam_count = 0
                        finally:
                            logger.info("New SPAM count is : %s" % str(spam_count))
                            browser.get(inbox_link)
                            waiit()
                            browser.get(spam_link)
                            waiit()
                            # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as Read")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking as not SPAM\n")
            # endregion

            # region Mark SPAM as Safe
            if 'SS' in actions:

                # region Controllers Settings
                logger.info("(*) Mark SPAM as Safe Actions")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing SPAM folder
                try:
                    # logger.info("- Getting SPAM folder")
                    browser.get(inbox_link)
                    waiit()
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error("/!\ (Error) Accessing SPAM folder")
                    logger.error(type(ex))
                # endregion

                # region Checking results
                spam_count = 0
                try:
                    waiit()
                    # logger.info("Getting spam Count")
                    # logger.info("Getting Junk span")
                    junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    # logger.info("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error("/!\ (Error) Getting SPAM Count")
                    logger.error(type(ex))
                    spam_count = 0
                logger.info("(!) SPAM count is : %s" % str(spam_count))
                # endregion

                # endregion

                # region looping through pages
                while spam_count > 0:
                    try:
                        # region Accessing 1st messages
                        # logger.info("Getting Subject SPAN")
                        first_mail = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//div[@unselectable="on"]/div/span'))
                        # logger.info("Done ! Subject is ==> %s" % first_mail.text)
                        # logger.info("Clicking Subject SPAN")
                        if first_mail.is_displayed():
                            first_mail.click()
                        # endregion

                        # region Clicking MANS button
                        try:
                            # logger.info("Getting Show Content button")
                            show_content_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]'))
                            # logger.info("Clicking Show Content")
                            # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]')))
                            if show_content_btn.is_displayed():
                                show_content_btn.click()
                                logger.info("- 'Show content' button clicked")
                        except Exception as ex:
                            logger.critical("/!\ (Error) Clicking 'Show content' button")
                            logger.critical(type(ex))
                            pass

                        # logger.info("Getting MANS button")
                        mans_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Move a message that isn\'t Junk to the Inbox"]'))

                        # logger.info("Clicking MANS button")
                        # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                        if mans_btn.is_displayed():
                            mans_btn.click()
                            logger.info("- 'Not SPAM' button clicked")

                        # logger.info("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                        # logger.info("Done !")
                        # logger.info("- Mark SPAM as Safe Button is Clicked")
                        # logger.info("(!) Getting Next Mail")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            logger.info("Getting spam Count")
                            junk_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Junk Email"]'))
                            logger.info("Getting Junk span")
                            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            spam_count = 0
                        except Exception as ex:
                            logger.error("/!\ (Error) Getting SPAM Count")
                            logger.error(type(ex))
                            spam_count = 0
                        logger.info("(!) New SPAM count is : %s" % str(spam_count))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Mark SPAM as Safe  Timed Out")
                        browser.get(inbox_link)
                        waiit()
                        browser.get(spam_link)
                        waiit()
                        pass
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as Safe")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done marking SPAM as Safe !\n")
            # endregion

            # endregion

            # ***********************************************************************

            # region Inbox Actions

            # region Mark inbox as Read
            if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):

                # region Controllers Settings
                logger.info("(*) Mark INBOX as read Actions :")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing INBOX folder
                try:
                    # logger.info("- Getting INBOX folder")
                    browser.get(inbox_link)
                    waiit()
                except Exception as ex:
                    logger.error("/!\ (Error) Getting INBOX list")
                    logger.error(type(ex))
                # endregion

                # region Filtering results
                # logger.info("Getting filter button")
                filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
                # logger.info("Clicking filter button")
                filter_btn.click()
                # logger.info("Waiting for Unread button")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
                # logger.info("Getting for Unread button")
                unread_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
                # logger.info("Clicking Unread button")
                unread_btn.click()
                # endregion

                # region Checking results
                inbox_count = 0
                try:
                    waiit()
                    # logger.info("Getting INBOX Count")
                    # logger.info("Getting Inbox span")
                    inbox_span = browser.find_element_by_xpath('//span[@title="Inbox"]')
                    # logger.info("%s" % inbox_span.text)
                    inbox_count = int(inbox_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error("/!\ (Error) Getting SPAM Count")
                    logger.error(type(ex))
                    inbox_count = 0
                logger.info("(!) INBOX count is : %s" % str(inbox_count))
                # endregion

                # endregion

                # region looping through results
                while inbox_count > 0:
                    try:

                        # region Selecting alls messages
                        logger.info("(!) Marking INBOX as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        # logger.info("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                        waiit()
                        # logger.info("Select all Msgs")
                        # logger.info("Defining hover action")
                        hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                        # logger.info("Hover over the checkbox")
                        hover.perform()
                        # logger.info("Hover Done")
                        # logger.info("Waiting for visibility")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        # logger.info("Element is visible")
                        # logger.info("Clicking Checkbox")
                        chk_bx_bttn.find_element_by_tag_name("button").click()
                        waiit()
                        # endregion

                        # region Clicking MAR button
                        # logger.info("Getting Menu button")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                        # logger.info("Clicking menu button")
                        menu_btn.click()
                        # logger.info("Waiting for MAR button")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@aria-label="Mark as read (Q)"]')))
                        # logger.info("Getting MAR button")
                        mar_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@aria-label="Mark as read (Q)"]'))
                        # logger.info("Clicking MAR button")
                        mar_bttn.click()
                        logger.info("(!) Selection Marked as READ")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            # logger.info("Getting INBOX Count")
                            inbox_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Inbox"]'))
                            # logger.info("Getting Inbox span")
                            inbox_count = int(inbox_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            inbox_count = 0
                        except Exception as ex:
                            logger.error("/!\ (Error) Getting SPAM Count")
                            logger.error(type(ex))
                            inbox_count = 0
                        logger.info("(!) New INBOX count is: %s" % str(inbox_count))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Mark INBOX as Read Timed Out")
                        browser.get(spam_link)
                        waiit()
                        browser.get(inbox_link)
                        waiit()
                        # region Filtering results
                        # logger.info("Getting filter button")
                        filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
                        # logger.info("Clicking filter button")
                        filter_btn.click()
                        # logger.info("Waiting for Unread button")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
                        # logger.info("Getting for Unread button")
                        unread_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
                        # logger.info("Clicking Unread button")
                        unread_btn.click()
                        # logger.info("Done !")
                        # endregion
                        pass
                    except Exception as ex:
                        logger.error("/!\ (Error) Mark SPAM as read")
                        logger.error(type(ex))
                        break
                # endregion
                logger.info("(!) Done marking as not SPAM !\n")

            # endregion

            # region Add contact Inbox / click Links / Flag Mail
            if ('AC' in actions) or ('CL' in actions) or ('FM' in actions):

                # region Controllers Settings

                logger.info("(*) Add Contact / Click Links / Flag Mail Actions: ")

                # region Accessing INBOX Keyword results TODO-CVC What if there is no results ??
                try:
                    logger.info("(!) Getting results for Subject: %s" % keyword)
                    waiit()
                    # logger.info("Waiting for search inbox")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@aria-label="Activate Search Textbox"]/span[2]')))
                    # logger.info("Selecting search inbox")
                    search_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@aria-label="Activate Search Textbox"]/span[2]'))
                    # logger.info("Clicking search inbox")
                    search_span.click()

                    # logger.info("Waiting for input")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input')))
                    # logger.info("Selecting input")
                    search_input = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input'))
                    # logger.info("sending keyword value")
                    search_input.send_keys(keyword)
                    # logger.info("pressing ENTER key")
                    search_input.send_keys(Keys.ENTER)
                    # logger.info("Waiting for results")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Exit search"]')))
                    waiit()
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button')))
                    more_results = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button'))
                    more_results.click()
                    # logger.info("Done")
                except Exception as ex:
                    logger.error("/!\ (Error) Getting INBOX results for Subject: %s" % keyword)
                    logger.error(type(ex))
                # endregion

                # region Accessing 1st messages
                # logger.info("Getting Subject SPAN")
                first_mail = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.senderText'))
                # logger.info("Clicking Subject SPAN")
                first_mail.click()
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Reply"]')))
                # logger.info("Done!")
                # endregion

                # region Getting loop settings
                # logger.info("Getting Newt button")
                next_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Next"]'))
                last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                last_page_checked = last_page
                # endregion

                # region Looping through results
                while not last_page_checked:
                    try:

                        # region Flag mail
                        if 'FM' in actions:
                            # logger.info("(*) - Flag mail action:")
                            # logger.info("Clicking menu")
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                            menu_btn.click()
                            # logger.info("Clicking Flag mail")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                            flag_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Flag for follow-up (Insert)"]'))
                            flag_btn.click()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                            logger.info("- E-mail flagged !")  # TODO-CVC to Count
                            if 'AC' not in actions:
                                time.sleep(1)
                                # logger.info("Done")
                        # endregion

                        # region add contact
                        if 'AC' in actions:
                            # logger.info("(*) - Add Contact action:")
                            # logger.info("Getting contact SPAN")
                            contact_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="ItemHeader.SenderLabel"]/div[2]/div/span/div/span/span'))
                            # logger.info("Hover over contact SPAN")
                            hover = ActionChains(browser).move_to_element(contact_span)
                            hover.perform()
                            # logger.info("Clicking Contact SPAN")
                            contact_span.click()
                            try:
                                # logger.info("Getting add contact buttons")
                                add_contact_buttons = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_xpath('//button[@aria-label="Add to contacts"]'))
                                # logger.info("looping through buttons")
                                for add_contact_button in add_contact_buttons:
                                    add_contact_button.click()
                                    # logger.info("Add to contacts button is clicked")
                                    # logger.info("Waiting for Save contact button")
                                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Save edit contact"]')))
                                    # logger.info("Getting Save contact button")
                                    save_contact_button = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Save edit contact"]'))
                                    # logger.info("Clicking save to contacts")
                                    save_contact_button.click()
                                    # logger.info('waiting for Popup to fade away')
                                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//button[@title="Save edit contact"]')))
                                    logger.info("- From-Email added to contacts")  # TODO-CVC to count
                                    if 'FM' not in actions:
                                        time.sleep(1)
                            except ElementNotVisibleException:
                                logger.warning("From-Email already Added !")
                            except TimeoutException:
                                logger.warning("From-Email already Added !")
                            except NoSuchElementException:
                                pass
                        # endregion

                        # region click Link
                        if 'CL' in actions:
                            waiit()
                            # logger.info("(*) Clicking the Link Action :")
                            # logger.info("Getting the Mail 'Body'")
                            body = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('Item.MessageUniqueBody'))
                            try:
                                # logger.info("Getting the Link in the Mail !")
                                link = body.find_elements_by_tag_name('a')[1]
                            except Exception as ex:
                                logger.warning("/!\ (Warning) Link Not Found !")
                                link = None
                                logger.info(type(ex))
                            waiit()
                            if link is not None:
                                try:
                                    # logger.info("link is Found ==> %s")
                                    waiit()
                                    # logger.info("Clicking the Link")
                                    while not link.is_displayed():
                                        pass
                                    link.click()
                                    WebDriverWait(browser, wait_timeout).until(lambda driver: len(browser.window_handles) > 1)
                                    # logger.info("New Tab Opened !")
                                    waiit()
                                    # logger.info("Switching to the new Tab !")
                                    browser.switch_to.window(browser.window_handles[1])
                                    waiit()
                                    # logger.info("Link Loaded")
                                    # logger.info("Closing !")
                                    browser.close()
                                    waiit()
                                    # logger.info("Going Back to Hotmail !")
                                    browser.switch_to.window(browser.window_handles[0])
                                    waiit()
                                    logger.info("- Link clicked ! ==> (%s)" % link.get_attribute('href'))
                                except Exception as ex:
                                    logger.error("/!\ (Error) Switching to new Tab")
                                    logger.error(type(ex))
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked = last_page if last_page else False
                        last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                        logger.info("(!) Getting next Mail ...")
                        next_btn.click()
                        time.sleep(1)
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ (Error) Add Contact and/or Click Links Timed Out")
                        break
                    except Exception as ex:
                        logger.error("/!\ (Error) Add Contact and/or Click Links Error !")
                        logger.error(type(ex))
                        break
                # endregion

                logger.info("(!) Done Add Contact / Click Links / Flag Mail\n")
                # endregion

                # endregion

                # endregion

                # ***********************************************************************
        # endregion

        return True
    # region Exceptions
    except Exception as exc:
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# OUPS !! #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error(type(exc))
        self.retry(exc=exc)
    # endregion

    # region Finally
    finally:
        logger.info("###************************************************************************###")
        logger.info('              (!) - Finished Actions for %s - (!)' % mail)
        logger.info("###************************************************************************###")
        browser.quit()
        # endregion
