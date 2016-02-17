from __future__ import absolute_import
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from celery.utils.log import get_task_logger
from selenium.webdriver.common.by import By
from selenium import webdriver
from celery import Celery
import time

logger = get_task_logger(__name__)
app = Celery('CapValue', broker='amqp://soufiaane:C@pV@lue2016@cvc.ma/cvcHost')


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, job, email):

    # region Settings
    proxy = "192.154.210.119"
    wait_timeout = 10
    port = "29954"
    actions = job['actions'].split(',')
    keyword = job['keywords']
    logger.error('Job Started :')
    logger.error('Actions: ' + job['actions'])
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
        logger.error("End Connection")
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
        logger.error("End of Verification Region")
        # endregion

        # region Spam Actions

        # region Mark Spam as read
        if ('RS' in actions) and ('SS' not in actions):  #

            # region Controllers Settings
            logger.error("(*) Read SPAM' Actions")
            logger.error("- Getting SPAM Folder")
            waiit()

            try:
                nav_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector("ul.indentedleftnavlist"))
                waiit()
                spam_list = nav_list.find_elements_by_tag_name("li")[3]
                waiit()
                spam_list.click()
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.XPATH, '//*[@placeholder="Search Junk"]')))
            except Exception as ex:
                logger.error(" /!\ - Clicking SPAM list Error")
                logger.error(type(ex))

            try:
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
                    logger.error("/!\ - Error Timed Oult")
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
                nav_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector("ul.indentedleftnavlist"))
                waiit()
                spam_list = nav_list.find_elements_by_tag_name("li")[3]
                waiit()
                spam_list.click()
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.XPATH, '//*[@placeholder="Search Junk"]')))
                waiit()
            except Exception as ex:
                logger.error(" /!\ - Clicking SPAM list Error")
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
                    logger.error("/!\ - Error Timed Oult")
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
                nav_list = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_css_selector("ul.indentedleftnavlist"))
                waiit()
                spam_list = nav_list.find_elements_by_tag_name("li")[3]
                waiit()
                spam_list.click()
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.XPATH, '//*[@placeholder="Search Junk"]')))
                waiit()
            except Exception as ex:
                logger.error(" /!\ - Clicking SPAM list Error")
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
                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
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
                    logger.error("/!\ - Error Timed Oult")
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
                    logger.error("/!\ - Error Timed Oult")
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
                    logger.error("/!\ - Error Timed Oult")
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
                            time.sleep(0.75)
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
                            add_contact_link.click()
                            waiit()
                            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.AddContact')))
                            logger.error('Contact Added')
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
                        bod[0].send_keys(Keys.CONTROL + ';')
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

            logger.error("- Done Add Contact and/or Click Links !\n")
        # endregion

        # endregion

        logger.error(' (!) - Finished Actions for %s' % mail)
        return True

    # region Exceptions
    except Exception as ex:
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# OUPS !! #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error(type(ex))
        self.retry(ex=ex)
    # endregion

    finally:
        logger.error("Quiting %s" % mail)
        browser.quit()
