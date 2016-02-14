from __future__ import absolute_import
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotVisibleException
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
    proxy = "67.21.35.254"
    wait_timeout = 10
    port = "8674"
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
                logger.error("REMOVING MODAL !!")
                browser.execute_script(script)
                logger.error('MODEL REMOVED !!')
            except NoSuchElementException:
                pass

        def waiit():
            try:
                look_for_pub()
                while browser.execute_script('return document.readyState;') != 'complete':
                    look_for_pub()
            except Exception:
                pass

        # endregion

        # region Connection
        logger.error("Starting Connection")
        logger.error("Accessing Hotmail")
        browser.get(link)

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

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
        junk_url = str(browser.current_url)[:str(browser.current_url).rindex('/')] + '/?fid=fljunk'
        inbox_url = junk_url.replace('fljunk', 'flinbox')
        waiit()
        look_for_pub()
        logger.error("End of Verification Region")
        # endregion

        # region Spam Actions
        try:
            waiit()
            spam_count = WebDriverWait(browser, wait_timeout).until(lambda browser: int(browser.find_elements_by_css_selector('span.count')[2].text))
            logger.error("Getting Spam count")
        except IndexError:
            spam_count = 0
        except ValueError:
            spam_count = 0
        except TimeoutException:
            spam_count = 0
        logger.error('Total Spam: %s' % str(spam_count))

        # region Spam Exist
        if spam_count > 0:
            logger.error("Spam Count > 0")
            browser.get(junk_url)
            logger.error("Accessing Spam Folder")
            waiit()
            if 'RS' in actions:  # Mark Spam as read
                logger.error("Starting Action 'Mark Spam as Read' !")
                while spam_count > 0:
                    try:
                        browser.get(junk_url)
                        logger.error("Marking Spam as read for this page")
                        waiit()
                        logger.error("Getting All Msgs checkbox")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        waiit()
                        chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('msgChkAll'))
                        waiit()
                        logger.error("Select all Msgs")
                        chk_bx_bttn.click()
                        logger.error("CheckBox is clicked !")
                        if spam_count >= 35:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.SelPrompt')))
                        # WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                        logger.error("Done")
                        try:
                            waiit()
                            logger.error("Getting Menu Button")
                            menu_btnn = browser.find_element_by_xpath('//*[@title=" Autres commandes"]')
                            waiit()
                            logger.error("Click Menu")
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title=" Autres commandes"]')))
                            waiit()
                            menu_btnn.click()
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                        except NoSuchElementException:
                            try:
                                logger.error("Getting Menu Button for English Version")
                                menu_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_xpath('//*[@title="More commands"]'))
                                waiit()
                                logger.error("Click Menu")
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                                waiit()
                                menu_btn.click()
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                            except TimeoutException:
                                logger.error("Menu Not Found ?")

                        logger.error("Clicking Mark as Read Button")
                        mar_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('MarkAsRead'))
                        waiit()
                        mar_btn.click()
                        logger.error("Done !")
                        waiit()
                        # WebDriverWait(browser, wait_timeout).until(lambda browser: int(browser.find_elements_by_css_selector('span.count')[2].text) < spam_count)
                        if 'NS' in actions:  # Not SPAM
                            logger.error("'Mark as Spam' is Selected !")
                            logger.error("We do it while we are here !")
                            logger.error("Clicking Mark As Not Spam !")
                            waiit()
                            manj_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('MarkAsNotJunk'))
                            waiit()
                            manj_btn.click()
                            waiit()
                            logger.error("Accessing Spam Folder to Get next Page !")
                            try:
                                WebDriverWait(browser, wait_timeout).until(lambda browser: int(browser.find_elements_by_css_selector('span.count')[2].text) < spam_count)
                            except ValueError:
                                spam_count = 0
                        else:
                            waiit()
                            logger.error("Accessing Next Page")
                            npl_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('nextPageLink'))
                            npl_btn.click()
                        try:
                            waiit()
                            logger.error("Getting new Spam Count !")
                            spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        except Exception as ex:
                            logger.error(type(ex))
                            logger.error("SPAM COUNT ERROR")
                            spam_count = 0
                        finally:
                            logger.error('Total Spam: %s' % str(spam_count))
                    except StaleElementReferenceException:
                        pass
                    except TimeoutException:
                        pass
            # region Mark as Not SPAM
            if ('NS' in actions) and ('RS' not in actions):  # Not SPAM
                logger.error("Starting 'Mark as Not Spam' Action !")
                waiit()
                try:
                    spam_span = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_elements_by_css_selector('span.count'))
                    spam_count = int(spam_span[2].text)
                    logger.error("Skipping 'Mark As Not SPAM' Actions !")
                except Exception as ex:
                    spam_count = 0
                    logger.error("Skipping 'Mark As Not SPAM' Actions !")
                    logger.error(type(ex))

                while spam_count > 0:
                    waiit()
                    logger.error("Marking As 'Not SPAM' for this page")
                    waiit()
                    logger.error("Selecting All Msgs !")
                    all_msgs_chkbx = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('msgChkAll'))
                    waiit()
                    all_msgs_chkbx.click()
                    waiit()
                    logger.error("Clicking 'Not Spam' Button !")
                    not_spam_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('MarkAsNotJunk'))
                    waiit()
                    not_spam_btn.click()
                    try:
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(lambda browser: int(browser.find_elements_by_css_selector('span.count')[2].text) < spam_count)
                        logger.error("Accessing SPAM Folder to get Next Page")
                        browser.get(junk_url)
                        waiit()
                        logger.error("Checking results !")
                        spam_span = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_elements_by_css_selector('span.count'))
                        spam_count = int(spam_span[2].text)
                        logger.error("SPAM COUNT: %s" % str(spam_count))
                    except ElementNotVisibleException:
                        pass
                    except StaleElementReferenceException:
                        pass
                    except ValueError as ex:
                        spam_count = 0
                        logger.error("Skipping 'Mark As Not SPAM' Actions !")
                    except Exception as ex:
                        spam_count = 0
                        logger.error("Skipping 'Mark As Not SPAM' Actions !")
                        logger.error(ex)
                        logger.error(type(ex))
            # endregion

            # region Mark SPAM as SAFE
            elif ('SS' in actions) and ('RS' not in actions) and ('NS' not in actions):  # Mark SPAM as Safe
                try:
                    waiit()
                    logger.error("Getting Email List Group !")
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                    email_list = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('ul.mailList'))
                    logger.error("Getting All Emails from Group")
                    waiit()
                    emails = email_list.find_elements_by_tag_name('li')
                    logger.error("Clicking the First Email")
                    waiit()
                    emails[0].click()
                    time.sleep(1)
                    waiit()
                except Exception as ex:
                    logger.error(type(ex))
                    pass
                while spam_count > 0:
                    # Mark Safe

                    try:
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                        safe_link = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('a.sfUnjunkItems'))
                        waiit()
                        logger.error("Marking Email as Safe")
                        safe_link.click()
                        time.sleep(1)
                        waiit()
                        logger.error("Email Marked as Safe")
                    except Exception as ex:
                        logger.error(type(ex))
                        pass

                    try:
                        waiit()
                        logger.error("Getting new SPAM COUNT")
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                    except IndexError:
                        spam_count = 0
                    except ValueError:
                        spam_count = 0
                    finally:
                        logger.error('Total Spam: %s' % str(spam_count))

                    try:
                        waiit()
                        logger.error("Getting Email List Group !")
                        email_list = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('ul.mailList'))
                        waiit()
                        logger.error("Getting All Emails from Group")
                        emails = email_list.find_elements_by_tag_name('li')
                        waiit()
                        logger.error("Clicking the First Email")
                        emails[0].click()
                        waiit()
                    except Exception as ex:
                        logger.error(type(ex))
                        # endregion
        # endregion
        # region Spam does not exist
        else:
            logger.error('There is no SPAM')
            logger.error('Skipping SPAM Actions !')
        # endregion

        # endregion

        # region Inbox Actions
        logger.error("Starting Inbox Actions !")
        if not str(browser.current_url).endswith('inbox'):
            browser.get(inbox_url)
        waiit()
        keywork_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0'
        logger.error("Accessing keyword '%s' Results" % keyword)
        browser.get(keywork_link)
        waiit()

        # region Mark inbox as Read
        if 'RI' in actions:  # Mark inbox as Read
            logger.error("Starting 'Mark Inbox As Read' Actions !")
            new_link = str(browser.current_url).replace('&sdr=4&satt=0', '&scat=1&sdr=4&satt=0')
            logger.error("Getting Unread Msgs Only !!")
            browser.get(new_link)
            waiit()
            try:
                browser.find_element_by_id('NoMsgs')
                logger.error("Results is Empty !")
                logger.error("Skipping 'Mark Inbox As Read' Actions !")
                no_results = True
            except NoSuchElementException:
                no_results = False

            while not no_results:
                logger.error("There are still results !")
                waiit()
                logger.error("Selecting All Msgs")
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_element_located((By.ID, 'msgChkAll')))
                waiit()
                check_all = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('msgChkAll'))
                waiit()
                check_all.click()
                waiit()
                try:
                    logger.error("Getting Menu Button for 'Mark inbox as Read' Action")
                    menu_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_xpath('//*[@title=" Autres commandes"]'))
                    waiit()
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                    waiit()
                    logger.error("Clicking Menu Button for 'Mark inbox as Read' Action")
                    menu_btn.click()
                    logger.error("Clicking Menu")
                    waiit()
                except NoSuchElementException:
                    try:
                        logger.error("Element Not Found! Try English Version")
                        logger.error("Getting Menu Button for 'Mark inbox as Read' Action")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        waiit()
                        logger.error("Clicking Menu Button for 'Mark inbox as Read' Action")
                        menu_btn.click()
                        logger.error("Clicking Menu")
                        waiit()
                        pass
                    except NoSuchElementException:
                        logger.error("Menu Not Found ??")
                        pass
                except TimeoutException:
                    try:
                        logger.error("Element Not Found! Try English Version")
                        logger.error("Getting Menu Button for 'Mark inbox as Read' Action")
                        menu_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        waiit()
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        logger.error("Clicking Menu Button for 'Mark inbox as Read' Action")
                        waiit()
                        menu_btn.click()
                        logger.error("Clicking Menu")
                        waiit()
                        pass
                    except TimeoutException:
                        logger.error("Menu Not Found ??")
                        pass
                waiit()
                logger.error("Marking Inbox As 'Read' !")
                mar_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_id('MarkAsRead'))
                waiit()
                mar_btn.click()
                waiit()
                logger.error("Accessing Result Page for Next Page !")
                browser.get(new_link)
                waiit()
                try:
                    browser.find_element_by_id('NoMsgs')
                    waiit()
                    logger.error("There are no Results")
                    logger.error("Skipping 'Mark Inbox As Read' Actions !")
                    no_results = True
                except NoSuchElementException:
                    no_results = False
                    pass
        # endregion

        # region Add contact Inbox / click Links
        if ('AC' in actions) or ('CL' in actions):  # Add contact Inbox
            logger.error("Add Contact and/or Click Links are in Selected Actions")
            logger.error("Open Mail per Mail for Actions !")

            try:
                logger.error("Getting keyword '%s' Results Page !" % keyword)
                browser.get(keywork_link)
                waiit()
                logger.error("Selecting First Mail Process")
                waiit()
                logger.error("Getting All Mails")
                waiit()
                emails = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_elements_by_css_selector('li.c-MessageRow'))
                waiit()
                logger.error("Done ! %s Mail Found" % str(len(emails)))
                try:
                    waiit()
                    while True:
                        waiit()
                        emails[0].click()
                        waiit()
                        try:
                            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer ')))
                            waiit()
                        except TimeoutException:
                            continue
                        except Exception as ex:
                            logger.error(type(ex))
                            pass

                    logger.error("Getting the Next Button !")
                    next_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img'))
                    waiit()
                    next_btn_attributes = next_btn.get_attribute('class')
                    waiit()
                    last_msg = True if str(next_btn_attributes).endswith('_d') else False
                    waiit()
                except StaleElementReferenceException:
                    last_msg = False
                    pass
                except TimeoutException:
                    last_msg = False
                    pass
                except Exception as ex:
                    last_msg = False
                    logger.error(type(ex))
                try:
                    while not last_msg:
                        logger.error("Not the last Message")
                        try:
                            # region Trust email Content
                            try:
                                logger.error("Trust Email Content")
                                mas_btn = browser.find_element_by_css_selector('a.sfMarkAsSafe')
                                waiit()
                                mas_btn.click()
                                logger.error("Email Trusted !")
                                waiit()
                                WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer')))
                            except NoSuchElementException:
                                logger.error("Email Content is Safe")
                                pass
                            except TimeoutException:
                                logger.error("Email Content is Safe")
                                pass
                            except ElementNotVisibleException:
                                logger.error("Email Content is Safe")
                                pass
                            # endregion

                            # region Add Contact
                            if 'AC' in actions:
                                logger.error("*- Add to Contact Action :")
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
                                except TimeoutException:
                                    logger.error("Link Not Found !")
                                    logger.error('Contact Already Exist')
                                    pass
                                except ElementNotVisibleException:
                                    logger.error("Link Not Found !")
                                    logger.error('Contact Already Exist')
                                    pass
                            # endregion

                            # region Flag Mail
                            if 'FM' in actions:
                                waiit()
                                logger.error("Flag Mail Action :")
                                try:
                                    logger.error("Getting Flag Mail")
                                    message_header = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_elements_by_css_selector('div.MessageHeaderItem'))
                                    waiit()
                                    flag = message_header[3].find_element_by_css_selector('img.ia_i_p_1')
                                    logger.error("Clicking Flag !")
                                    flag.click()
                                    waiit()
                                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'img.ia_i_p_1')))
                                    logger.error("Email Flagged !")
                                except NoSuchElementException:
                                    logger.error("Email already Flagged !")
                                    pass
                                except TimeoutException:
                                    logger.error("Email already Flagged !")
                                    pass
                            # endregion

                            # region Click Links
                            if 'CL' in actions:
                                waiit()
                                logger.error("Clicking the Link Action :")
                                logger.error("Getting the Mail 'Body'")
                                body1 = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('div.readMsgBody'))
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
                                        time.sleep(1)
                                        logger.error("Link clicked !")
                                        WebDriverWait(browser, wait_timeout).until(lambda browser: len(browser.window_handles) > 0)
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
                                        # logger.error("there is no NEW TAB !!!")
                                        # logger.error("trying Again !!!")
                                        # logger.error("Clicking the LINK !!!")
                                        # lnk.click()
                                        # waiit()
                                        # WebDriverWait(browser, wait_timeout).until(lambda browser: browser.window_handles > 0)
                                        # logger.error("Now IT WORKED !!")
                                        # logger.error("Switching to the new TAB !!")
                                        # browser.switch_to.window(browser.window_handles[1])
                                        # waiit()
                                        # logger.error("Link is Loaded !")
                                        # logger.error("Closing link !")
                                        # browser.close()
                                        # waiit()
                                        # logger.error("Going Back to Hotmail !")
                                        # browser.switch_to.window(browser.window_handles[0])
                                        # waiit()
                                logger.error("Done Clicking Links !!")
                            # endregion
                            logger.error("Getting Next MAIL !")
                            bod = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_elements_by_tag_name('body'))
                            waiit()
                            bod[0].send_keys(Keys.CONTROL + ';')
                            time.sleep(1)
                            waiit()
                        except NoSuchElementException as ex:
                            logger.error(type(ex))
                            continue
                        except StaleElementReferenceException as ex:
                            logger.error(type(ex))
                            continue
                        finally:
                            waiit()
                            try:
                                next_btn = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img'))
                            except Exception as ex:
                                logger.error(type(ex))
                                next_btn = None
                            next_btn_attributes = next_btn.get_attribute('class') if next_btn else ''
                            last_msg = True if str(next_btn_attributes).endswith('_d') else False

                except NoSuchElementException as ex:
                    logger.error(type(ex))
                    pass
                except StaleElementReferenceException as ex:
                    logger.error(type(ex))
                    pass

            except NoSuchElementException as ex:
                logger.error(type(ex))
                pass
            except StaleElementReferenceException as ex:
                logger.error(type(ex))
                pass
            except Exception as ex:
                logger.error(type(ex))
                pass
        # endregion

        # region Flag mail
        if ('FM' in actions) and (not (('AC' in actions) or ('CL' in actions))):  # Flag mail
            logger.error("'Flag Mail' Actions :")
            waiit()
            logger.error("Getting keyword '%s' Results !" % keyword)
            browser.get(keywork_link)
            waiit()
            next_page_disabled = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('div.NextPageDisabled'))
            last_page = next_page_disabled.is_displayed()
            last_page_checked = False
            while not last_page_checked:
                logger.error("Flaging Mails for this Page !")
                waiit()
                messages = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('ul.mailList').find_elements_by_tag_name('li'))
                for msg in range(len(messages)):
                    try:
                        messages = WebDriverWait(browser, wait_timeout).until(lambda browser: browser.find_element_by_css_selector('ul.mailList').find_elements_by_tag_name('li'))
                        waiit()
                        flag = messages[msg].find_element_by_css_selector('img.ia_i_p_1')
                        flag.click()
                        time.sleep(1)
                        waiit()
                    except NoSuchElementException:
                        pass
                waiit()
                last_page_checked = last_page if last_page else False
                if browser.find_element_by_id('nextPageLink').is_displayed():
                    browser.find_element_by_id('nextPageLink').click()
                time.sleep(1)
                waiit()
                last_page = browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()
            logger.error("Done Flaging Mails !")
        # endregion

        # endregion

        logger.error('Finished Actions for %s' % mail)
        waiit()
        look_for_pub()
    # region Finally + Exceptions
    except Exception as ex:
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# OUPS !! #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        logger.error(type(ex))
        self.retry(ex=ex)
    finally:
        logger.error("We Quit %s" % mail)
        browser.quit()
        # endregion
