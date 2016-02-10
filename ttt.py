from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

while True:

    # region Settings
    ACTIONS = 'AC'.split(',')  # RS,NS
    PROXY = "67.21.35.254:8674"
    Keyword = 'Validate'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    service_args = ['--proxy=%s' % PROXY, '--proxy-type=http']
    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)
    # browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path="chromedriver")
    browser.maximize_window()


    def look_for_pub():
        try:
            browser.find_element_by_css_selector('iframe.OutlookAppUpsellFrame')
            script = 'var element1 = document.getElementById("notificationContainer");element1.parentNode.removeChild(element1);\
            var element2 = document.getElementsByClassName("UI_Dialog_BG")[0];element2.parentNode.removeChild(element2);\
            var element3 = document.getElementsByClassName("OutlookAppUpsellFrame")[0];element3.parentNode.removeChild(element3);'
            browser.execute_script(script)
        except Exception:
            logger.error('')


    def look_for_unblock():
        try:
            btn_unblock = browser.find_element_by_xpath('//*[@id="notificationContainer"]/div/div/div/div/div[2]/button')
            handles_before = browser.window_handles
            btn_unblock.click()
            WebDriverWait(browser, 1).until(lambda browser: len(handles_before) != len(browser.window_handles))
            logger.error('# Unblock Clicked')
        except NoSuchElementException:
            pass


    def waiit():
        try:
            look_for_pub()
            look_for_unblock()
            while browser.execute_script('return document.readyState;') != 'complete':
                look_for_pub()
                look_for_unblock()
        except:
            pass


    # endregion

    try:

        # region Connection
        email = 'AriannalVansicex3185@hotmail.com'
        pswd = 'lhnreqb54'
        link = 'http://www.hotmail.com'
        browser.get(link)
        if 'ERR_PROXY_CONNECTION_FAILED' in str(browser.page_source):
            logger.error('problem PROXY')
            break
        default_window = browser.window_handles[0]

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

        login_champ.send_keys(email)
        pswd_champ.send_keys(pswd)
        login_btn.click()
        waiit()
        look_for_pub()
        # endregion

        # region IsVerified ?
        try:
            btn__next_verified = browser.find_element_by_xpath('//*[@value="Suivant"]')
            btn__next_verified.click()
        except Exception as ex:
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
            waiit()
            spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
        except Exception:
            spam_count = 0
        logger.error('Total Spam: ' + str(spam_count))

        if spam_count > 0:
            browser.get(junk_url)
            waiit()
            if 'RS' in ACTIONS:  # Mark Spam as read
                while (not browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()) or spam_count > 0:
                    waiit()
                    browser.find_element_by_id('msgChkAll').click()
                    time.sleep(1)
                    waiit()
                    try:
                        browser.find_element_by_xpath('//*[@title=" Autres commandes"]').click()
                    except NoSuchElementException:
                        try:
                            browser.find_element_by_xpath('//*[@title="More commands"]').click()
                            pass
                        except NoSuchElementException:
                            pass
                    time.sleep(1)
                    waiit()
                    browser.find_element_by_id('MarkAsRead').click()
                    waiit()
                    time.sleep(1)
                    if ('NS' in ACTIONS):  # Not SPAM
                        waiit()
                        browser.find_element_by_id('MarkAsNotJunk').click()
                        waiit()
                        browser.get(junk_url)
                    else:
                        waiit()
                        browser.find_element_by_id('nextPageLink').click()
                    try:
                        waiit()
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        logger.error('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0
            if ('NS' in ACTIONS) and ('RS' not in ACTIONS):  # Not SPAM
                while (not browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()) or spam_count > 0:
                    waiit()
                    browser.find_element_by_id('msgChkAll').click()
                    time.sleep(1)
                    waiit()
                    browser.find_element_by_id('MarkAsNotJunk').click()
                    waiit()
                    browser.get(junk_url)
                    waiit()
                    try:
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        logger.error('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0
            elif ('SS' in ACTIONS) and ('RS' not in ACTIONS) and ('NS' not in ACTIONS):  # Mark SPAM as Safe
                try:
                    waiit()
                    email_list = browser.find_element_by_css_selector('ul.mailList')
                    emails = email_list.find_elements_by_tag_name('li')
                    emails[0].click()
                    waiit()
                except Exception as ex:
                    logger.error(type(ex))
                    pass
                while spam_count > 0:
                    # Mark Safe
                    try:
                        waiit()
                        safe_link = browser.find_element_by_css_selector('a.sfUnjunkItems')
                        safe_link.click()
                        waiit()
                    except Exception as ex:
                        logger.error(type(ex))
                        pass

                    try:
                        waiit()
                        spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
                        logger.error('Total Spam: ' + str(spam_count))
                    except Exception:
                        spam_count = 0

                    try:
                        waiit()
                        email_list = browser.find_element_by_css_selector('ul.mailList')
                        emails = email_list.find_elements_by_tag_name('li')
                        emails[0].click()
                        waiit()
                    except Exception as ex:
                        logger.error(type(ex))
        else:
            logger.error('Nothing to do here : ')
        # endregion

        # region Inbox Actions

        if not str(browser.current_url).endswith('inbox'): browser.get(inbox_url)
        waiit()
        keywork_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=flsearch&srch=1&skws=' + Keyword + '&sdr=4&satt=0'
        browser.get(keywork_link)
        waiit()

        # region Mark inbox as Read
        if 'RI' in ACTIONS:  # Mark inbox as Read
            new_link = str(browser.current_url).replace('&sdr=4&satt=0', '&scat=1&sdr=4&satt=0')
            browser.get(new_link)
            waiit()
            try:
                browser.find_element_by_id('NoMsgs')
                no_results = True
            except NoSuchElementException:
                no_results = False

            while not no_results:
                time.sleep(1)
                waiit()
                browser.find_element_by_id('msgChkAll').click()
                time.sleep(1)
                waiit()
                try:
                    browser.find_element_by_xpath('//*[@title=" Autres commandes"]').click()
                    waiit()
                except NoSuchElementException:
                    try:
                        browser.find_element_by_xpath('//*[@title="More commands"]').click()
                        waiit()
                        pass
                    except NoSuchElementException:
                        pass
                time.sleep(1)
                waiit()
                browser.find_element_by_id('MarkAsRead').click()
                time.sleep(1)
                waiit()
                browser.get(new_link)
                waiit()
                try:
                    browser.find_element_by_id('NoMsgs')
                    no_results = True
                except NoSuchElementException:
                    no_results = False
                    pass
        # endregion

        # region Add contact Inbox / click Links
        if ('AC' in ACTIONS) or ('CL' in ACTIONS):  # Add contact Inbox
            try:
                browser.get(keywork_link)
                waiit()
                emails = browser.find_elements_by_css_selector('li.c-MessageRow')
                waiit()
                emails[0].find_elements_by_tag_name('span')[1].click()
                waiit()
                next_btn = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img'))
                waiit()
                next_btn_attributes = next_btn.get_attribute('class')
                waiit()
                last_msg = True if str(next_btn_attributes).endswith('_d') else False
                waiit()
                try:
                    while not last_msg:
                        try:
                            # region Add Contact
                            if 'AC' in ACTIONS:
                                try:
                                    waiit()
                                    add_contact_link = browser.find_element_by_css_selector('a.AddContact')
                                    add_contact_link.click()
                                    time.sleep(1)
                                    waiit()
                                    logger.error('Contact Added')
                                except NoSuchElementException:
                                    logger.error('Contact Already Exist')
                                    pass
                            # endregion

                            # region Trust email Content
                            try:
                                browser.find_element_by_css_selector('a.sfMarkAsSafe').click()
                                time.sleep(1)
                                waiit()
                            except NoSuchElementException:
                                pass
                            # endregion

                            # region Flag Mail
                            if 'FM' in ACTIONS:
                                waiit()
                                try:
                                    flag = browser.find_elements_by_css_selector('div.MessageHeaderItem')[3].find_element_by_css_selector('img.ia_i_p_1')
                                    flag.click()
                                    waiit()
                                    time.sleep(0.5)
                                except NoSuchElementException:
                                    pass
                            # endregion

                            # region Click Links
                            if 'CL' in ACTIONS:
                                waiit()
                                body1 = browser.find_element_by_css_selector('div.readMsgBody')
                                body = body1.find_elements_by_tag_name('div')
                                try:
                                    lnk = body[0].find_elements_by_tag_name('a')[1]
                                except Exception:
                                    lnk = None
                                waiit()
                                if lnk is not None:
                                    waiit()
                                    lnk.click()
                                    waiit()
                                    if len(browser.window_handles) > 0:
                                        browser.switch_to.window(browser.window_handles[1])
                                        waiit()
                                        browser.close()
                                        waiit()
                                        browser.switch_to.window(browser.window_handles[0])
                                        waiit()
                                    else:
                                        time.sleep(1)
                                        lnk.click()
                                        time.sleep(1)
                                        waiit()
                                        if len(browser.window_handles) > 0:
                                            browser.switch_to.window(browser.window_handles[1])
                                            waiit()
                                            browser.close()
                                            waiit()
                                            browser.switch_to.window(browser.window_handles[0])
                                            waiit()
                            # endregion
                            bod = browser.find_elements_by_tag_name('body')[0]
                            bod.send_keys(Keys.CONTROL + ';')
                            time.sleep(1)
                            waiit()
                        except NoSuchElementException as ex:
                            logger.error(type(ex))
                            continue
                        except StaleElementReferenceException as ex:
                            logger.error(type(ex))
                            continue
                        finally:
                            time.sleep(1)
                            waiit()
                            try:
                                next_btn = browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img')
                            except Exception as ex:
                                logger.error(type(ex))
                                next_btn = None
                            next_btn_attributes = next_btn.get_attribute('class') if next_btn else ''
                            last_msg = True if str(next_btn_attributes).endswith('_d') else False

                except NoSuchElementException as ex:
                    logger.error(type(ex))
                    continue
                except StaleElementReferenceException as ex:
                    logger.error(type(ex))
                    continue

            except NoSuchElementException as ex:
                logger.error(type(ex))
                continue
            except StaleElementReferenceException as ex:
                logger.error(type(ex))
                continue
            except Exception as ex:
                logger.error(type(ex))
                continue
        # endregion

        # region Flag mail
        if 'FM' in ACTIONS:  # Flag mail
            waiit()
            browser.get(keywork_link)
            waiit()
            last_page = browser.find_element_by_css_selector('div.NextPageDisabled').is_displayed()
            last_page_checked = False
            while (not last_page_checked):
                waiit()
                messages = browser.find_element_by_css_selector('ul.mailList').find_elements_by_tag_name('li')
                for msg in messages:
                    try:
                        waiit()
                        flag = msg.find_element_by_css_selector('img.ia_i_p_1')
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
        # endregion

        # endregion

        logger.error('Now What ??')
        waiit()
        look_for_pub()
    except Exception as ex:
        logger.error(type(ex))
    finally:
        browser.quit()
