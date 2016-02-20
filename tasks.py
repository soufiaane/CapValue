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
    logger.error('Job Started :')
    logger.error('Actions: %s\n' % job['actions'])
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
            except Exception as exc:
                print(type(exc))
                pass

        # endregion

        # region Connection
        logger.error("Starting Connection")
        logger.error("Accessing Hotmail")
        browser.get(link)

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@name="SI"]')

        login_champ.send_keys(mail)
        logger.error("Sending Email : %s" % mail)
        pswd_champ.send_keys(pswd)
        logger.error("Sending Password : %s" % pswd)
        login_btn.click()
        logger.error("Clicking Login Button")
        waiit()
        look_for_pub()
        logger.error("End Connection\n")
        # endregion

        # region IsVerified ?
        logger.error("Checking if verified")
        try:
            btn__next_verified = browser.find_element_by_xpath('//*[@value="Suivant"]')
            logger.error("Email need to be verified")
            btn__next_verified.click()
        except NoSuchElementException:
            logger.error("Email is Verified")
            pass
        waiit()
        look_for_pub()
        logger.error("End of Verification Region\n")
        # endregion

        # region Check Version
        logger.error("Checking mail version")
        logger.error("Current URL : %s" % browser.current_url)
        if "outlook" in browser.current_url:
            logger.error("- New Version")
            version = "new"
        else:
            logger.error("- Old Version")
        logger.error("End of Checking mail version\n")
        # endregion

        # region Old Version
        if version == "old":
            logger.error("Starting actions for Old mail version")

            # ***********************************************************************

            # region Spam Actions

            # region Mark Spam as read
            if ('RS' in actions) and ('SS' not in actions):  #

                # region Controllers Settings
                logger.error("(*) Read SPAM' Actions")
                logger.error("- Getting SPAM Folder")
                waiit()

                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    logger.error("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM list Error")
                    logger.error(type(ex))

                try:
                    waiit()
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked = True
                    logger.error("SPAM folder is empty !")
                    logger.error("Skipping read SPAM actions!")
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
                        logger.error("Marking SPAM as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        logger.error("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        logger.error("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        logger.error("CheckBox is clicked !")
                        # endregion

                        # region Clicking menu
                        logger.error("Getting Menu Button")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        waiit()
                        logger.error("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        waiit()
                        menu_btn.click()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                        # endregion

                        # region Clicking MAR button
                        logger.error("Clicking Mark as Read Button")
                        mar_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsRead'))
                        waiit()
                        mar_btn.click()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        except TimeoutException:
                            pass
                        logger.error("Done !")
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked = last_page if last_page else False
                        next_page_link = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('nextPageLink'))
                        if next_page_link.is_displayed():
                            logger.error("Accessing Next Page")
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
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as read  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking SPAM as read !\n")

            # endregion

            # region Mark as Not SPAM
            if ('NS' in actions) and ('SS' not in actions):  # Not SPAM

                # region Controllers Settings
                logger.error("(*) Mark as Not SPAM Actions")
                logger.error("- Getting SPAM Folder")
                waiit()

                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    logger.error("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM list Error")
                    logger.error(type(ex))

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
                        logger.error("Marking as not SPAM for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        logger.error("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        logger.error("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        logger.error("CheckBox is clicked !")
                        # endregion

                        # region Clicking MANS button
                        logger.error("Clicking 'Not Spam' Button !")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                        waiit()
                        not_spam_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                        waiit()
                        not_spam_btn.click()
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
                        except NoSuchElementException:
                            still_results = True
                        logger.error("last page : %s" % str(not still_results))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Mark as not SPAM")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking as not SPAM !\n")
            # endregion

            # region Mark SPAM as SAFE
            if 'SS' in actions:

                # region Controllers Settings
                logger.error("(*) Mark SPAM as safe actions :")
                logger.error("- Getting SPAM Folder")
                waiit()

                try:
                    waiit()
                    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
                    logger.error("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM list Error")
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
                        logger.error("Getting Email List Group !")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                        email_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                        logger.error("Getting All Emails from Group")
                        waiit()
                        emails = email_list.find_elements_by_tag_name('li')
                        logger.error("Clicking the First Email")
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
                        logger.error("Marking Email as Safe")
                        safe_link.click()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                        except TimeoutException:
                            pass
                        waiit()
                        logger.error("Email Marked as Safe")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            browser.find_element_by_id("NoMsgs")
                            still_results = False
                        except NoSuchElementException:
                            still_results = True
                        logger.error("last page : %s" % str(not still_results))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as safe Error !")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking SPAM as safe !\n")
            # endregion

            # endregion

            # ***********************************************************************

            # region Inbox Actions

            # region Mark inbox as Read
            if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):

                # region Controllers Settings
                logger.error("(*) Mark INBOX as read Actions")
                logger.error("- Getting unread messages for Keyword : %s" % keyword)
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
                        logger.error("Marking INBOX as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        logger.error("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        logger.error("Select all Msgs")
                        chk_bx_bttn.click()
                        waiit()
                        logger.error("CheckBox is clicked !")
                        # endregion

                        # region Clicking menu
                        logger.error("Getting Menu Button")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        waiit()
                        logger.error("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        waiit()
                        menu_btn.click()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                        # endregion

                        # region Clicking MAR button
                        logger.error("Clicking Mark as Read Button")
                        mar_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('MarkAsRead'))
                        waiit()
                        mar_btn.click()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        except TimeoutException:
                            pass
                        logger.error("Done !")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            browser.find_element_by_id("NoMsgs")
                            still_results = False
                        except NoSuchElementException:
                            still_results = True
                        logger.error("last page : %s" % str(not still_results))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as read  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking INBOX as read !\n")
            # endregion

            # region Flag mail
            if ('FM' in actions) and ('AC' not in actions) and ('CL' not in actions):

                # region Controllers Settings
                logger.error("(*) Flag INBOX Actions")
                logger.error("- Getting result for Keyword : %s" % keyword)
                waiit()

                keyword_link_flag = WebDriverWait(browser, wait_timeout).until(lambda driver: str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0')
                browser.get(keyword_link_flag)

                try:
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked_flag = True
                    logger.error("SPAM folder is empty !")
                    logger.error("Skipping read SPAM actions!")
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
                        logger.error("Flaging Mails for this Page !")
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
                                flag.click()
                                waiit()
                                time.sleep(1)
                            except NoSuchElementException:
                                pass
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked_flag = last_page_flag if last_page_flag else False
                        next_page_link = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('nextPageLink'))
                        if next_page_link.is_displayed():
                            logger.error("Accessing Next Page")
                            waiit()
                            next_page_link.click()
                            waiit()
                            try:
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            except TimeoutException:
                                pass
                        next_page_disabled_flag = browser.find_element_by_css_selector('div.NextPageDisabled')
                        last_page_flag = next_page_disabled_flag.is_displayed()
                        logger.error("Last page : %s" % last_page_flag)
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Flag INBOX  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done Flaging Mails !\n")
            # endregion

            # region Add contact Inbox / click Links
            if ('AC' in actions) or ('CL' in actions):

                # region Controllers Settings
                logger.error("(*) Add Contact and/or Click Links are in Selected Actions")
                logger.error("- Open Mail per Mail for Actions !")
                logger.error("- Getting result for Keyword : %s" % keyword)
                waiit()

                keyword_link_ac = WebDriverWait(browser, wait_timeout).until(lambda driver: str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0')
                browser.get(keyword_link_ac)

                try:
                    waiit()
                    browser.find_element_by_id("NoMsgs")
                    last_page_checked_ac = True
                    logger.error("INBOX folder is empty !")
                    logger.error("Skipping Add Contact and/or Click Links actions!")
                except NoSuchElementException:
                    waiit()
                    next_page_disabled_ac = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
                    last_page_ac = next_page_disabled_ac.is_displayed()
                    last_page_checked_ac = False
                # endregion

                # region Accessing first mail!
                if not last_page_checked_ac:
                    waiit()
                    logger.error("Getting Email List Group !")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                    email_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                    logger.error("Getting All Emails from Group")
                    waiit()
                    emails = email_list.find_elements_by_tag_name('li')
                    logger.error("Clicking the First Email")
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
                                logger.error("Flag Mail Action :")
                                logger.error("Getting Flag Mail")
                                waiit()
                                message_header = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_css_selector('div.MessageHeaderItem'))
                                waiit()
                                flag = message_header[3].find_element_by_css_selector('img.ia_i_p_1')
                                logger.error("Clicking Flag !")
                                flag.click()
                                time.sleep(1)
                                waiit()
                                logger.error("Email Flagged !")
                            except NoSuchElementException:
                                logger.error("Email already Flagged !")
                                pass
                            except Exception as ex:
                                logger.error(" /!\ - Flag mail Error !")
                                logger.error(type(ex))
                        # endregion

                        # region Trust email Content
                        try:
                            logger.error("Trust Email Content")
                            safe_btn = browser.find_element_by_css_selector('a.sfMarkAsSafe')
                            waiit()
                            safe_btn.click()
                            logger.error("Email Trusted !")
                            waiit()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfMarkAsSafe')))
                        except NoSuchElementException:
                            logger.error("Email Content is Safe")
                            pass
                        except Exception as ex:
                            logger.error(" /!\ - Trust Email Error !")
                            logger.error(type(ex))
                        # endregion

                        # region Add Contact
                        if 'AC' in actions:
                            logger.error("Add to Contact Action :")
                            try:
                                waiit()
                                logger.error("Getting 'Add to Contact' Link")
                                add_contact_link = browser.find_element_by_css_selector('a.AddContact')
                                logger.error("Clicking 'Add to Contact' Link")
                                waiit()

                                if (str(add_contact_link.text) == "Add to contacts") or (str(add_contact_link.text) == "Ajouter aux contacts"):
                                    add_contact_link.click()
                                    waiit()
                                    try:
                                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                        WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                    except TimeoutException:
                                        pass
                            except NoSuchElementException:
                                logger.error("Link Not Found !")
                                logger.error('Contact Already Exist')
                                pass
                            except Exception as ex:
                                logger.error(" /!\ - Add Contact Error !")
                                logger.error(type(ex))
                        # endregion

                        # region Click Links
                        if 'CL' in actions:
                            waiit()
                            logger.error("Clicking the Link Action :")
                            logger.error("Getting the Mail 'Body'")
                            body1 = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.readMsgBody'))
                            body = body1.find_elements_by_tag_name('div')
                            try:
                                logger.error("Getting the Link in the Mail !")
                                lnk = body[0].find_elements_by_tag_name('a')[1]
                            except Exception as ex:
                                logger.error("Link Not Found !")
                                lnk = None
                                logger.error(type(ex))
                            waiit()
                            if lnk is not None:
                                try:
                                    logger.error("link is Found : %s" % lnk.get_attribute('href'))
                                    waiit()
                                    logger.error("Clicking the Link")
                                    lnk.click()
                                    logger.error("Link clicked !")
                                    WebDriverWait(browser, wait_timeout).until(lambda driver: len(browser.window_handles) > 1)
                                    logger.error("New Tab Opened !")
                                    waiit()
                                    logger.error("Switching to the new Tab !")
                                    browser.switch_to.window(browser.window_handles[1])
                                    waiit()
                                    logger.error("Link Loaded")
                                    logger.error("Closing !")
                                    browser.close()
                                    waiit()
                                    logger.error("Going Back to Hotmail !")
                                    browser.switch_to.window(browser.window_handles[0])
                                    waiit()
                                except Exception as ex:
                                    logger.error("Error Switching to new Tab")
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
                        last_page_ac = True if str(next_btn_attributes).endswith('_d') else False
                        waiit()
                        if not last_page_ac:
                            logger.error("Getting Next MAIL !")
                            bod = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_tag_name('body'))
                            waiit()
                            bod[0].send_keys(Keys.CONTROL + '.')
                            waiit()
                            time.sleep(1)
                        logger.error("Last page : %s" % str(last_page_ac))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Add Contact and/or Click Links Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Add Contact and/or Click Links Error !")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done Add Contact and/or Click Links !")
            # endregion

            logger.error("\n")

            # endregion

            # ***********************************************************************

        # endregion

        # ***********************************************************************

        # region New Version
        elif version == "new":
            logger.error("Starting actions for New mail version")

            # region Configure Mail BOX
            try:
                waiit()
                preview_pane = browser.find_element_by_css_selector("div.vResize")
                if preview_pane.is_displayed():
                    logger.error("- Mailbox not yet configured !")
                    logger.error("- Configureing !")
                    logger.error("- Getting settings button")
                    settings_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id("O365_MainLink_Settings"))
                    waiit()
                    logger.error("- Clicking settings button")
                    settings_btn.click()
                    logger.error("- Waiting for menu to show")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.o365cs-nav-contextMenu")))
                    logger.error("- Getting display settings")
                    display_settings = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Display settings"]'))
                    waiit()
                    logger.error("- Clicking display settings")
                    display_settings.click()
                    logger.error("- Waiting for display settings to shows")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
                    logger.error("- Getting Hide reading pane option")
                    hide_pane = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Hide reading pane"]'))
                    waiit()
                    logger.error("- Clicking Hide reading pane option")
                    hide_pane.click()
                    time.sleep(1)
                    logger.error("- Getting save button")
                    ok_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@aria-label="Save"]'))
                    waiit()
                    logger.error("- Clicking save button")
                    ok_btn.click()
                    logger.error("- Waiting for Settings pane to fade away")
                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
                else:
                    logger.error("- Mailbox already configured !")
            except NoSuchElementException:
                logger.error("- Mailbox already configured !")
                pass
            except Exception as ex:
                logger.error("/!\ - Check Version Error")
                logger.error(type(ex))
            logger.error("- Done configuring mailbox !\n")
            # endregion

            # ***********************************************************************

            # region Spam Actions

            # region Mark Spam as read
            if ('RS' in actions) and ('SS' not in actions):
                logger.error("(*) Read SPAM Actions")
                logger.error("- Mark SPAM as read are disabled for new version of mailboxes !")
                logger.error("- Skipping marking SPAM as read !\n")
            # endregion

            # region Mark as Not SPAM
            if ('NS' in actions) and ('SS' not in actions):  # Not SPAM

                # region Controllers Settings
                logger.error("(*) Mark as not SPAM Actions")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing SPAM folder
                try:
                    logger.error("- Getting SPAM folder")
                    waiit()
                    logger.error("Accessink SPAM folder : %s" % spam_link)
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM list Error")
                    logger.error(type(ex))
                # endregion

                # region Checking results
                spam_count = 0
                try:
                    waiit()
                    logger.error("Getting spam Count")
                    logger.error("Getting Junk span")
                    junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    logger.error("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM Count Error")
                    logger.error(type(ex))
                    spam_count = 0
                finally:
                    logger.error("SPAM count is : %s" % str(spam_count))
                # endregion

                # endregion

                # region looping through pages
                while spam_count > 0:
                    try:

                        # region Selecting alls messages
                        logger.error("Marking SPAM as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        logger.error("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                        waiit()
                        logger.error("Select all Msgs")
                        logger.error("Defining hover action")
                        hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                        logger.error("Hover over the checkbox")
                        hover.perform()
                        logger.error("Hover Done")
                        logger.error("Waiting for visibility")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        logger.error("Element is visible")
                        logger.error("Clicking Checkbox")
                        chk_bx_bttn.find_element_by_tag_name("button").click()
                        waiit()
                        # endregion

                        # region Clicking MANS button
                        try:
                            logger.error("Clicking Mark as not SPAM Button")
                            logger.error("Getting MANS button")
                            mans_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                            waiit()
                            logger.error("Waiting for MANS button")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                            logger.error("Clicking MANS button")
                            mans_btn.click()
                            logger.error("Mark as not SPAM Button is Clicked")
                            logger.error("Waiting for action to be performed")
                            WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/div[1]/span').text == "Junk Email")
                            logger.error("Sending ESC key")
                            ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                            logger.error("Waiting for invisibility of element !")
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        except TimeoutException:
                            pass
                        logger.error("Done !")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            logger.error("Getting spam Count")
                            logger.error("Getting Junk span")
                            junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                            logger.error("%s" % junk_span.text)
                            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            spam_count = 0
                        except Exception as ex:
                            logger.error(" /!\ - Getting SPAM Count Error")
                            logger.error(type(ex))
                            spam_count = 0
                        finally:
                            logger.error("New SPAM count is : %s" % str(spam_count))
                            browser.get(inbox_link)
                            waiit()
                            browser.get(spam_link)
                            waiit()
                        logger.error("")
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as read  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking as not SPAM !")

            logger.error("\n")
            # endregion

            # region Mark SPAM as Safe
            if 'SS' in actions:

                # region Controllers Settings
                logger.error("(*) Mark SPAM as Safe Actions")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing SPAM folder
                try:
                    logger.error("- Getting SPAM folder")
                    browser.get(inbox_link)
                    waiit()
                    browser.get(spam_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM list Error")
                    logger.error(type(ex))
                # endregion

                # region Checking results
                spam_count = 0
                try:
                    waiit()
                    logger.error("Getting spam Count")
                    logger.error("Getting Junk span")
                    junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    logger.error("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM Count Error")
                    logger.error(type(ex))
                    spam_count = 0
                logger.error("SPAM count is : %s" % str(spam_count))
                # endregion

                # endregion

                # region looping through pages
                while spam_count > 0:
                    try:

                        # region Accessing 1st messages
                        logger.error("Getting Subject SPAN")
                        first_mail = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//div[@unselectable="on"]/div/span'))

                        logger.error("Done ! Subject is ==> %s" % first_mail.text)

                        logger.error("Clicking Subject SPAN")
                        if first_mail.is_displayed():
                            first_mail.click()
                        # endregion

                        # region Clicking MANS button
                        try:
                            logger.error("Getting Show Content button")
                            show_content_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]'))

                            logger.error("Clicking Show Content")
                            # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]')))
                            if show_content_btn.is_displayed():
                                show_content_btn.click()
                        except Exception as ex:
                            logger.critical(type(ex))
                            pass

                        logger.error("Getting MANS button")
                        mans_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Move a message that isn\'t Junk to the Inbox"]'))

                        logger.error("Clicking MANS button")
                        # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                        if mans_btn.is_displayed():
                            mans_btn.click()

                        logger.error("Mark SPAM as Safe Button is Clicked")
                        logger.error("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                        logger.error("Done !")
                        logger.error("Getting Next Mail")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            logger.error("Getting spam Count")
                            junk_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Junk Email"]'))
                            logger.error("Getting Junk span")
                            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            spam_count = 0
                        except Exception as ex:
                            logger.error(" /!\ - Getting SPAM Count Error")
                            logger.error(type(ex))
                            spam_count = 0
                        logger.error("New SPAM count is : %s" % str(spam_count))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error(" /!\ - Mark SPAM as Safe  Timed Out")
                        browser.get(inbox_link)
                        waiit()
                        browser.get(spam_link)
                        waiit()
                        pass
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as Safe  Error")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error("- Done marking SPAM as Safe !")

            logger.error("\n")
            # endregion

            # endregion

            # ***********************************************************************

            # region Inbox Actions

            # region Mark inbox as Read
            if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):

                # region Controllers Settings
                logger.error("(*) Mark INBOX as read Actions :")
                waiit()
                spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
                inbox_link = spam_link.replace("/junkemail", "/inbox")

                # region Accessing INBOX folder
                try:
                    logger.error("- Getting INBOX folder")
                    browser.get(inbox_link)
                    waiit()
                except Exception as ex:
                    logger.error(" /!\ - Getting INBOX list Error")
                    logger.error(type(ex))
                # endregion

                # region Filtering results
                logger.error("Getting filter button")
                filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
                logger.error("Clicking filter button")
                filter_btn.click()
                logger.error("Waiting for Unread button")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
                logger.error("Getting for Unread button")
                unread_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
                logger.error("Clicking Unread button")
                unread_btn.click()
                logger.error("Done !")
                # endregion

                # region Checking results
                inbox_count = 0
                try:
                    waiit()
                    logger.error("Getting INBOX Count")
                    logger.error("Getting Inbox span")
                    inbox_span = browser.find_element_by_xpath('//span[@title="Inbox"]')
                    logger.error("%s" % inbox_span.text)
                    inbox_count = int(inbox_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    logger.error(" /!\ - Getting SPAM Count Error")
                    logger.error(type(ex))
                    inbox_count = 0
                logger.error("INBOX count is : %s" % str(inbox_count))
                # endregion
                # endregion

                # region looping through results
                while inbox_count > 0:
                    try:

                        # region Selecting alls messages
                        logger.error("Marking INBOX as read for this page")
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        logger.error("Getting All Msgs checkbox")
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                        waiit()
                        logger.error("Select all Msgs")
                        logger.error("Defining hover action")
                        hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                        logger.error("Hover over the checkbox")
                        hover.perform()
                        logger.error("Hover Done")
                        logger.error("Waiting for visibility")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                        logger.error("Element is visible")
                        logger.error("Clicking Checkbox")
                        chk_bx_bttn.find_element_by_tag_name("button").click()
                        waiit()
                        # endregion

                        # region Clicking MAR button
                        logger.error("Getting Menu button")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                        logger.error("Clicking menu button")
                        menu_btn.click()
                        logger.error("Waiting for MAR button")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@aria-label="Mark as read (Q)"]')))
                        logger.error("Getting MAR button")
                        mar_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@aria-label="Mark as read (Q)"]'))
                        logger.error("Clicking MAR button")
                        mar_bttn.click()
                        logger.error("Waiting for action to be performed")
                        # endregion

                        # region Checking if it was the last page
                        try:
                            waiit()
                            logger.error("Getting INBOX Count")
                            inbox_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Inbox"]'))
                            logger.error("Getting Inbox span")
                            inbox_count = int(inbox_span.find_element_by_xpath('../div[2]/span').text)
                        except ValueError:
                            inbox_count = 0
                        except Exception as ex:
                            logger.error(" /!\ - Getting SPAM Count Error")
                            logger.error(type(ex))
                            inbox_count = 0
                        logger.error("New INBOX count is : %s" % str(inbox_count))
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error(" /!\ - Mark INBOX as Read Timed Out")
                        browser.get(spam_link)
                        waiit()
                        browser.get(inbox_link)
                        waiit()
                        # region Filtering results
                        logger.error("Getting filter button")
                        filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
                        logger.error("Clicking filter button")
                        filter_btn.click()
                        logger.error("Waiting for Unread button")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
                        logger.error("Getting for Unread button")
                        unread_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
                        logger.error("Clicking Unread button")
                        unread_btn.click()
                        logger.error("Done !")
                        # endregion
                        pass
                    except Exception as ex:
                        logger.error(" /!\ - Mark SPAM as read  Error")
                        logger.error(type(ex))
                        break
                # endregion
                logger.error("- Done marking as not SPAM !")

            logger.error("\n")
            # endregion

            # region Add contact Inbox / click Links / Flag Mail
            if ('AC' in actions) or ('CL' in actions) or ('FM' in actions):

                # region Controllers Settings

                # region Accessing INBOX Keyword results TODO-CVC What if there is no results ??
                try:
                    logger.error("- Getting Keyword results for %s" % keyword)
                    waiit()
                    logger.error("Waiting for search inbox")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@aria-label="Activate Search Textbox"]/span[2]')))
                    logger.error("Selecting search inbox")
                    search_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@aria-label="Activate Search Textbox"]/span[2]'))
                    logger.error("Clicking search inbox")
                    search_span.click()

                    logger.error("Waiting for input")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input')))
                    logger.error("Selecting input")
                    search_input = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input'))
                    logger.error("sending keyword value")
                    search_input.send_keys(keyword)
                    logger.error("pressing ENTER key")
                    search_input.send_keys(Keys.ENTER)
                    logger.error("Waiting for results")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Exit search"]')))
                    waiit()
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button')))
                    more_results = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button'))
                    more_results.click()
                    logger.error("Done")
                except Exception as ex:
                    logger.error(" /!\ - Getting INBOX list Error")
                    logger.error(type(ex))
                # endregion

                # region Accessing 1st messages
                logger.error("Getting Subject SPAN")
                first_mail = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector('div.senderText'))
                logger.error("Clicking Subject SPAN")
                first_mail.click()
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Reply"]')))
                logger.error("Done!")
                # endregion

                # region Getting loop settings
                logger.error("Getting Newt button")
                next_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Next"]'))
                last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                last_page_checked = last_page
                # endregion

                # region Looping through results
                while not last_page_checked:
                    try:

                        # region Flag mail
                        if 'FM' in actions:
                            logger.error("(*) - Flag mail action:")
                            logger.error("Clicking menu")
                            menu_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                            menu_btn.click()
                            logger.error("Clicking Flag mail")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                            flag_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//span[@title="Flag for follow-up (Insert)"]'))
                            flag_btn.click()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                            if 'AC' not in actions:
                                time.sleep(1)
                            logger.error("Done")
                        # endregion

                        # region add contact
                        if 'AC' in actions:
                            logger.error("(*) - Add Contact action:")
                            logger.error("Getting contact SPAN")
                            contact_span = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//*[@id="ItemHeader.SenderLabel"]/div[2]/div/span/div/span/span'))
                            logger.error("Hover over contact SPAN")
                            hover = ActionChains(browser).move_to_element(contact_span)
                            hover.perform()
                            logger.error("Clicking Contact SPAN")
                            contact_span.click()
                            try:
                                logger.error("Getting add contact buttons")
                                add_contact_buttons = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_elements_by_xpath('//button[@aria-label="Add to contacts"]'))
                                logger.error("looping through buttons")
                                for add_contact_button in add_contact_buttons:
                                    add_contact_button.click()
                                    logger.error("Add to contacts button is clicked")
                                    logger.error("Waiting for Save contact button")
                                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Save edit contact"]')))
                                    logger.error("Getting Save contact button")
                                    save_contact_button = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath('//button[@title="Save edit contact"]'))
                                    logger.error("Clicking save to contacts")
                                    save_contact_button.click()
                                    logger.error('waiting for Popup to fade away')
                                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, '//button[@title="Save edit contact"]')))
                                    if 'FM' not in actions:
                                        time.sleep(1)
                                    logger.error("Done adding to contacts")
                            except ElementNotVisibleException:
                                logger.error("Contact already Added !")
                            except TimeoutException:
                                logger.error("Contact already Added !")
                            except NoSuchElementException:
                                pass
                        # endregion

                        # region click Link
                        if 'CL' in actions:
                            waiit()
                            logger.error("(*) Clicking the Link Action :")
                            logger.error("Getting the Mail 'Body'")
                            body = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('Item.MessageUniqueBody'))
                            try:
                                logger.error("Getting the Link in the Mail !")
                                link = body.find_elements_by_tag_name('a')[1]
                            except Exception as ex:
                                logger.error(" /!\ Link Not Found !")
                                link = None
                                logger.error(type(ex))
                            waiit()
                            if link is not None:
                                try:
                                    logger.error("link is Found ==> %s" % link.get_attribute('href'))
                                    waiit()
                                    logger.error("Clicking the Link")
                                    while not link.is_displayed():
                                        pass
                                    link.click()
                                    logger.error("Link clicked !")
                                    WebDriverWait(browser, wait_timeout).until(lambda driver: len(browser.window_handles) > 1)
                                    logger.error("New Tab Opened !")
                                    waiit()
                                    logger.error("Switching to the new Tab !")
                                    browser.switch_to.window(browser.window_handles[1])
                                    waiit()
                                    logger.error("Link Loaded")
                                    logger.error("Closing !")
                                    browser.close()
                                    waiit()
                                    logger.error("Going Back to Hotmail !")
                                    browser.switch_to.window(browser.window_handles[0])
                                    waiit()
                                except Exception as ex:
                                    logger.error(" /!\ Error Switching to new Tab")
                                    logger.error(type(ex))
                        # endregion

                        # region Checking if it was the last page
                        last_page_checked = last_page if last_page else False
                        last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                        logger.error("Getting next Mail")
                        next_btn.click()
                        time.sleep(1)
                        # endregion

                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        logger.error("/!\ - Add Contact and/or Click Links and/or Flag Mail Error Timed Out")
                        break
                    except Exception as ex:
                        logger.error(" /!\ - Add Contact and/or Click Links and/or Flag Mail Error !")
                        logger.error(type(ex))
                        break
                # endregion

                logger.error('- Done Add Contact and/or Click Links and/or Flag Mail !')
                # endregion

            logger.error("\n")
            # endregion

            # endregion

            # ***********************************************************************

        # endregion

        return True
    # region Exceptions
    except Exception as ex:
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# OUPS !! #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error(type(ex))
        self.retry(ex=ex)
    # endregion

    # region Finally
    finally:
        logger.error("Quiting %s \n" % mail)
        browser.quit()
        logger.error("###************************************************************************###")
        logger.error('              (!) - Finished Actions for %s' % mail)
        logger.error("###************************************************************************###")
    logger.error("")
    # endregion
