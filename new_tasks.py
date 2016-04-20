from __future__ import absolute_import
from celery.utils.log import get_task_logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from celeryTasks.celerySettings import app
import time

logger = get_task_logger(__name__)
link = 'http://www.hotmail.com'
version = "old"
wait_timeout = 0
email_language = 'English'
inbox_count = 0


# region helper Functions
def check_first_run(browser):
    try:
        consumer_first_run_btn = browser.find_element_by_class_name("__Microsoft_Owa_ConsumerFirstRun_templates_cs_4")
        consumer_first_run_btn.click()
    except NoSuchElementException:
        pass


def look_for_pub(browser):
    try:
        browser.find_element_by_css_selector('iframe.OutlookAppUpsellFrame')
        script = 'var element1 = document.getElementById("notificationContainer");\
        element1.parentNode.removeChild(element1);\
        var element2 = document.getElementsByClassName("UI_Dialog_BG")[0];\
        element2.parentNode.removeChild(element2);\
        var element3 = document.getElementsByClassName("OutlookAppUpsellFrame")[0];\
         element3.parentNode.removeChild(element3);'
        browser.execute_script(script)
    except NoSuchElementException:
        pass
    except NoSuchWindowException:
        pass
    except Exception as e:
        print(type(e))
        pass


def wait_for_page(browser):
    try:
        look_for_pub(browser)
        while browser.execute_script('return document.readyState;') != 'complete':
            look_for_pub(browser)
    except:
        pass


def connect(browser, login, pswd):
    try:
        login_champ = browser.find_element_by_name("loginfmt")
        pswd_champ = browser.find_element_by_name("passwd")
        print("[#] Sending Email : %s" % login)
        login_champ.send_keys(login)
        print("[#] Sending Password : %s" % pswd)
        pswd_champ.send_keys(pswd)
        print("[#] Clicking Login Button")
        pswd_champ.submit()
    except Exception as e:
        print(type(e))
        pass


def check_if_verified(browser):
    try:
        btn__next_verified = browser.find_element_by_xpath('//*[@value="Next"]')
        btn__next_verified.click()
        print("[-] Email needs to be verified")
    except NoSuchElementException:
        pass

    try:
        btn__next_verified = browser.find_element_by_xpath('//*[@value="Suivant"]')
        btn__next_verified.click()
        print("[-] Email needs to be verified")
    except NoSuchElementException:
        pass

    try:
        email_blocked = browser.find_element_by_css_selector('div.serviceAbusePageContainer')
        if email_blocked.is_displayed():
            print("[-] Email is blocked")
            browser.quit()
            return False
    except NoSuchElementException:
        print("[-] Email is not blocked")


def check_version(browser):
    global version
    if "outlook" in browser.current_url:
        version = "new"
        print("[-] New Mail Version")
    else:
        print("[-] Old Mail Version")


def check_email_language(browser):
    global email_language
    try:
        if version == "new":
            settings_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_id("O365_MainLink_Settings"))
            if settings_btn.get_attribute("title") == "Open the Settings menu to access personal and app settings":
                email_language = "English"
                print("[-] Language is 'English'")
            elif settings_btn.get_attribute("title") == "Ouvrir le menu Paramètres pour accéder aux paramètres" \
                                                        "personnels et à ceux des applications":
                email_language = "French"
                print("[-] Language is 'French'")
        elif version == "old":
            folders_h1 = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_css_selector('h1.lnav_topItemLabel'))
            if folders_h1.text == "Folders":
                email_language = "English"
                print("[-] Language is 'English'")
            elif folders_h1.text == "Dossiers":
                email_language = "French"
                print("[-] Language is 'French'")
    except StaleElementReferenceException:
        check_email_language(browser)
    except Exception as e:
        print("/!\ (Error) Getting Mailbox Language !")
        print(type(e))
        raise


def configure_mailbox(browser):
    try:
        preview_pane = browser.find_element_by_css_selector("div._n_O1")
        if preview_pane.is_displayed():
            print("[-] Mailbox not yet configured !")
            check_first_run(browser)
            settings_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_id("O365_MainLink_Settings"))
            wait_for_page(browser)
            print("[#] Clicking settings button")
            check_first_run(browser)
            settings_btn.click()
            print("[#] Waiting for menu to show")
            check_first_run(browser)
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "div.o365cs-nav-contextMenu")))
            check_first_run(browser)
            if email_language == "English":
                display_settings = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Display settings"]'))
            else:
                display_settings = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Paramètres d\'affichage"]'))
            check_first_run(browser)
            wait_for_page(browser)
            check_first_run(browser)
            print("[#] Clicking display settings")
            display_settings.click()
            check_first_run(browser)
            print("[#] Waiting for display settings to shows")
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
            check_first_run(browser)
            if email_language == "English":
                hide_pane = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Hide reading pane"]'))
            else:
                hide_pane = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Masquer le volet de lecture"]'))
            check_first_run(browser)
            wait_for_page(browser)
            print("[#] Clicking Hide reading pane option")
            hide_pane.click()
            check_first_run(browser)
            time.sleep(1)
            if email_language == "English":
                ok_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Save"]'))
            else:
                ok_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//*[@aria-label="Enregistrer"]'))
            check_first_run(browser)
            wait_for_page(browser)
            print("[#] Clicking save button")
            ok_btn.click()
            check_first_run(browser)
            WebDriverWait(browser, wait_timeout).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.panelPopupShadow")))
            check_first_run(browser)
        else:
            print("[-] Mailbox already configured !")
    except NoSuchElementException:
        print("[-] Mailbox already configured !")
    except Exception as exc:
        print(type(exc))
        print("/!\ (Error) Check Display Settings")
# endregion


# region Old Version

# region MailBox Functions
def access_spam_folder_old(browser, spam_link):
    try:
        wait_for_page(browser)
        browser.get(spam_link)
        wait_for_page(browser)
    except Exception as ex:
        print("/!\ (Error) Accessink SPAM folder ")
        print(type(ex))
        raise


def open_menu_old(browser):
    try:
        if email_language == "English":
            menu_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
            wait_for_page(browser)
            logger.debug("[#] Click Menu")
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
            wait_for_page(browser)
        else:
            menu_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//*[@title=" Autres commandes"]'))
            wait_for_page(browser)
            logger.debug("[#] Click Menu")
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//*[@title=" Autres commandes"]')))
            wait_for_page(browser)
    except TimeoutException:
        menu_btn = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath('//*[@title="更多命令"]'))
        wait_for_page(browser)
        logger.debug("[#] Click Menu")
        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@title="更多命令"]')))
        wait_for_page(browser)

    menu_btn.click()
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))


def select_all_msgs_old(browser):
    wait_for_page(browser)
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
    logger.debug("Getting All Msgs checkbox")
    wait_for_page(browser)
    chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_id('msgChkAll'))
    wait_for_page(browser)
    logger.debug("Select all Msgs")
    chk_bx_bttn.click()
    wait_for_page(browser)
    logger.debug("CheckBox is clicked !")
# endregion


def report_old_version(browser, actions, keyword):
    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
    keyword_link = str(browser.current_url)[:str(browser.current_url).index(
            '.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&scat=1&sdr=4&satt=0'

    # region Spam Actions
    if ('RS' in actions) or ('NS' in actions) or ('SS' in actions):
        wait_for_page(browser)
        access_spam_folder_old(browser, spam_link)

    # region Mark Spam as read
    if ('RS' in actions) and ('SS' not in actions):  #
        print("[+] Read SPAM Actions")

        # region Controllers Settings
        try:
            wait_for_page(browser)
            browser.find_element_by_id("NoMsgs")
            last_page_checked = True
            print("[!] SPAM folder is empty, Skipping read SPAM actions!")
        except NoSuchElementException:
            wait_for_page(browser)
            next_page_disabled = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
            last_page = next_page_disabled.is_displayed()
            last_page_checked = False
        # endregion

        # region looping through pages
        while not last_page_checked:
            try:
                select_all_msgs_old(browser)

                open_menu_old(browser)

                # region Clicking MAR button
                logger.debug("[#] Clicking Mark as Read Button")
                mar_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsRead'))
                wait_for_page(browser)
                mar_btn.click()
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                except TimeoutException:
                    pass
                # endregion

                # region Checking if it was the last page
                last_page_checked = last_page if last_page else False
                next_page_link = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('nextPageLink'))
                if next_page_link.is_displayed():
                    logger.debug("Accessing Next Page")
                    wait_for_page(browser)
                    next_page_link.click()
                    wait_for_page(browser)
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.SelPrompt')))
                next_page_disabled = browser.find_element_by_css_selector('div.NextPageDisabled')
                last_page = next_page_disabled.is_displayed()
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                pass
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as read")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking SPAM as read\n")

    # endregion

    # region Mark as Not SPAM
    if ('NS' in actions) and ('SS' not in actions):  # Not SPAM
        print("[+] Mark as Not SPAM Actions")

        if 'RS' in actions:
            access_spam_folder_old(browser, spam_link)

        # region Controllers Settings
        wait_for_page(browser)

        try:
            browser.find_element_by_id("NoMsgs")
            still_results = False
        except NoSuchElementException:
            still_results = True
        # endregion

        # region looping through pages
        while still_results:
            try:
                select_all_msgs_old(browser)

                # region Clicking MANS button
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                wait_for_page(browser)
                not_spam_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                wait_for_page(browser)
                not_spam_btn.click()
                logger.debug("[!] 'Not Spam' Button Clicked !")
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                except TimeoutException:
                    pass
                # endregion

                # region Checking if it was the last page
                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                    print("[!] Last page !")
                except NoSuchElementException:
                    still_results = True
                # endregion
                pass
            except StaleElementReferenceException:
                pass
            except TimeoutException:
                pass
            except Exception as ex:
                print("/!\ (Error) Mark as not SPAM")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking e-mails as not spam\n")
    # endregion

    # region Mark SPAM as SAFE
    if 'SS' in actions:
        print("[+] Mark SPAM as safe actions :")

        # region Controllers Settings
        wait_for_page(browser)

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
                wait_for_page(browser)
                logger.debug("[-] Getting Email List Group !")
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                email_list = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                logger.debug("[-] Getting All Emails from Group")
                wait_for_page(browser)
                emails = email_list.find_elements_by_tag_name('li')
                logger.debug("[#] Clicking the first e-mail")
                wait_for_page(browser)
                emails[0].click()
                WebDriverWait(browser, wait_timeout).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer')))
                wait_for_page(browser)
                # endregion

                # region Clicking SS button
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                safe_link = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_css_selector('a.sfUnjunkItems'))
                wait_for_page(browser)
                safe_link.click()
                logger.debug("[!] E-mail marked as Safe")
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfUnjunkItems')))
                except TimeoutException:
                    pass

                wait_for_page(browser)
                # endregion

                # region Checking if it was the last page
                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                    logger.debug("[!] Last page !")
                except NoSuchElementException:
                    still_results = True
                # endregion

                pass
            except StaleElementReferenceException:
                pass
            except TimeoutException:
                # region Clicking MANS button
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                wait_for_page(browser)
                not_spam_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                wait_for_page(browser)
                not_spam_btn.click()
                logger.debug("[!] 'Not Spam' Button Clicked !")
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                except TimeoutException:
                    pass

                # region Checking if it was the last page
                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                    print("[!] Last page !")
                except NoSuchElementException:
                    still_results = True
                # endregion

                pass
                # endregion
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as safe!")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking SPAM as safe\n")
    # endregion

    # endregion

    # region Inbox Actions
    if ('RI' in actions) or ('FM' in actions) or ('AC' in actions) or ('CL' in actions):
        wait_for_page(browser)
        access_spam_folder_old(browser, keyword_link)

    # region Mark inbox as Read
    if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):
        print("[+] Mark INBOX as read Actions")

        # region Controllers Settings
        wait_for_page(browser)

        try:
            browser.find_element_by_id("NoMsgs")
            still_results = False
        except NoSuchElementException:
            still_results = True
        # endregion

        # region Looping through messages
        while still_results:
            try:
                select_all_msgs_old(browser)

                open_menu_old(browser)

                # region Clicking MAR button
                logger.debug("[#] Clicking Mark as Read Button")
                mar_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsRead'))
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                mar_btn.click()
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                except TimeoutException:
                    pass
                # endregion

                # region Checking if it was the last page
                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                    logger.debug("[!] Last page !")
                except NoSuchElementException:
                    still_results = True
                # endregion
                pass
            except StaleElementReferenceException:
                pass
            except TimeoutException:
                pass
            except Exception as ex:
                print("/!\ (Error) Mark INBOX as read")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking INBOX as read\n")
    # endregion

    # region Flag mail
    if ('FM' in actions) and ('AC' not in actions) and ('CL' not in actions):
        print("[+] Flag INBOX Actions")

        if 'RI' in actions:
            wait_for_page(browser)
            access_spam_folder_old(browser, keyword_link)

        # region Controllers Settings
        try:
            browser.find_element_by_id("NoMsgs")
            last_page_checked_flag = True
        except NoSuchElementException:
            wait_for_page(browser)
            next_page_disabled_flag = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
            last_page_flag = next_page_disabled_flag.is_displayed()
            last_page_checked_flag = False
        # endregion

        # region Looping through pages
        while not last_page_checked_flag:
            try:

                # region Selecting alls messages
                logger.debug("[-] Flaging Mails for this Page !")
                wait_for_page(browser)
                messages_ul = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                wait_for_page(browser)
                messages = messages_ul.find_elements_by_tag_name('li')
                # endregion

                # region Clicking through messages
                for i in range(len(messages)):
                    try:
                        flag = messages[i].find_element_by_css_selector('img.ia_i_p_1')
                        wait_for_page(browser)
                        flag.click()
                        wait_for_page(browser)
                        time.sleep(1)
                        logger.debug("[!] E-mail flagged")
                    except NoSuchElementException:
                        pass
                # endregion

                # region Checking if it was the last page
                last_page_checked_flag = last_page_flag if last_page_flag else False
                next_page_link = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('nextPageLink'))
                if next_page_link.is_displayed():
                    wait_for_page(browser)
                    next_page_link.click()
                    wait_for_page(browser)
                    logger.debug("[-] Accessing Next Page")
                    try:
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        WebDriverWait(browser, wait_timeout).until(
                            ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    except TimeoutException:
                        pass
                next_page_disabled_flag = browser.find_element_by_css_selector('div.NextPageDisabled')
                last_page_flag = next_page_disabled_flag.is_displayed()
                logger.debug("Last page : %s" % last_page_flag)
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                pass
            except Exception as ex:
                print("/!\ (Error) Flag INBOX  Error")
                print(type(ex))
                raise
        # endregion

        print("[!] Done Flaging Mails\n")
    # endregion

    # region Add Contact  / Click Links / Flag Mail
    if ('AC' in actions) or ('CL' in actions):

        # region Controllers Settings
        print("[+] Add Contact / Click Links / Flag Mail Actions: ")
        print("[-] Open Mail per Mil for Actions !")
        print("[-] Getting result for Subject : %s" % keyword)
        wait_for_page(browser)

        keyword_link_ac = WebDriverWait(browser, wait_timeout).until(lambda driver: str(browser.current_url)[
                                                                                    :str(
                                                                                        browser.current_url).index(
                                                                                        '.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0')
        browser.get(keyword_link_ac)

        try:
            wait_for_page(browser)
            browser.find_element_by_id("NoMsgs")
            last_page_checked_ac = True
            print("[!] INBOX folder is empty")
            print("[!] Skipping Add Contact / Click Links / Flag Mail actions")
        except NoSuchElementException:
            wait_for_page(browser)
            next_page_disabled_ac = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_css_selector('div.NextPageDisabled'))
            last_page_ac = next_page_disabled_ac.is_displayed()
            last_page_checked_ac = False
        # endregion

        # region Accessing first mail!
        if not last_page_checked_ac:
            wait_for_page(browser)
            print("Getting Email List Group !")
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
            email_list = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_css_selector('ul.mailList'))
            print("Getting All Emails from Group")
            wait_for_page(browser)
            emails = email_list.find_elements_by_tag_name('li')
            print("Clicking the First Email")
            wait_for_page(browser)
            time.sleep(1)
            emails[0].click()
            WebDriverWait(browser, wait_timeout).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div.ReadMsgContainer')))
            wait_for_page(browser)
        # endregion

        # region Looping through mails
        while not last_page_checked_ac:
            try:

                # region Flag Mail
                if 'FM' in actions:
                    try:
                        print("Flag Mail Action :")
                        print("Getting Flag Mail")
                        wait_for_page(browser)
                        message_header = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_elements_by_css_selector('div.MessageHeaderItem'))
                        wait_for_page(browser)
                        flag = message_header[3].find_element_by_css_selector('img.ia_i_p_1')
                        print("Clicking Flag !")
                        flag.click()
                        time.sleep(1)
                        wait_for_page(browser)
                        print("[-] E-mail Flagged !")  # TODO-CVC To count
                    except NoSuchElementException:
                        print("[!] Email already Flagged !")
                        pass
                    except Exception as ex:
                        print("/!\ (Error) Flag mail !")
                        print(type(ex))
                # endregion

                # region Trust email Content
                try:
                    print("Trust Email Content")
                    safe_btn = browser.find_element_by_css_selector('a.sfMarkAsSafe')
                    wait_for_page(browser)
                    safe_btn.click()
                    print("[-] E-mail content trusted !")
                    wait_for_page(browser)
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'a.sfMarkAsSafe')))
                except NoSuchElementException:
                    print("Email Content is Safe")
                    pass
                except Exception as ex:
                    print("/!\ (Error) Trust Email Error !")
                    print(type(ex))
                # endregion

                # region Add Contact
                if 'AC' in actions:
                    print("Add to Contact Action :")
                    try:
                        wait_for_page(browser)
                        print("Getting 'Add to Contact' Link")
                        add_contact_link = browser.find_element_by_css_selector('a.AddContact')
                        print("Clicking 'Add to Contact' Link")
                        wait_for_page(browser)

                        if (str(add_contact_link.text) == "Add to contacts") or (
                                    str(add_contact_link.text) == "Ajouter aux contacts") or (
                                    str(add_contact_link.text) == "添加至联系人"):
                            add_contact_link.click()
                            print("[-] From-Email added to contacts")
                            wait_for_page(browser)
                            try:
                                WebDriverWait(browser, wait_timeout).until(
                                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                                WebDriverWait(browser, wait_timeout).until(
                                    ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                            except TimeoutException:
                                pass
                    except NoSuchElementException:
                        print("Link Not Found !")
                        print('[!] Contact Already Exist')
                        pass
                    except Exception as ex:
                        print("/!\ (Error) Add Contact")
                        print(type(ex))
                # endregion

                # region Click Links
                if 'CL' in actions:
                    wait_for_page(browser)
                    print("Clicking the Link Action :")
                    print("Getting the Mail 'Body'")
                    body1 = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_css_selector('div.readMsgBody'))
                    body = body1.find_elements_by_tag_name('div')
                    try:
                        print("Getting the Link in the Mail !")
                        lnk = body[0].find_elements_by_tag_name('a')[1]
                    except Exception as ex:
                        print("[!] Link Not Found")
                        lnk = None
                        print(type(ex))
                    wait_for_page(browser)
                    if lnk is not None:
                        try:
                            print("link is Found : %s" % lnk.get_attribute('href'))
                            wait_for_page(browser)
                            print("Clicking the Link")
                            lnk.click()
                            print("[-] Link clicked ! ==> (%s)" % lnk.get_attribute('href'))
                            WebDriverWait(browser, wait_timeout).until(
                                lambda driver: len(browser.window_handles) > 1)
                            print("New Tab Opened !")
                            wait_for_page(browser)
                            print("Switching to the new Tab !")
                            browser.switch_to.window(browser.window_handles[1])
                            wait_for_page(browser)
                            print("Link Loaded")
                            print("Closing !")
                            browser.close()
                            wait_for_page(browser)
                            print("Going Back to Hotmail !")
                            browser.switch_to.window(browser.window_handles[0])
                            wait_for_page(browser)
                        except NoSuchWindowException:
                            pass
                        except Exception as ex:
                            print("/!\ (Error) Switching to new Tab")
                            print(type(ex))
                # endregion

                # region Checking if it was the last page
                last_page_checked_ac = last_page_ac if last_page_ac else False
                next_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_css_selector('a.rmNext'))
                wait_for_page(browser)
                next_btn_img = next_btn.find_element_by_tag_name('img')
                wait_for_page(browser)
                next_btn_attributes = next_btn_img.get_attribute('class')
                wait_for_page(browser)
                if str(next_btn_attributes).endswith('_d'):
                    last_page_ac = True
                    print("[!] Last page")
                else:
                    last_page_ac = False
                wait_for_page(browser)
                if not last_page_ac:
                    print("[!] Getting next e-mail ...")
                    bod = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_elements_by_tag_name('body'))
                    wait_for_page(browser)
                    bod[0].send_keys(Keys.CONTROL + ".")
                    wait_for_page(browser)
                time.sleep(1)
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ -(Error) Add Contact / Click Links / Flag Mail Timed Out")
                break
            except Exception as ex:
                print("/!\ (Error) Add Contact and/or Click Links Error !")
                print(type(ex))
                break
        # endregion
        print("[!] Done Add Contact / Click Links / Flag Mail\n")
    # endregion
    # endregion
    pass

# endregion


# region New Version

# region MailBox Functions
def filter_unread_new(browser):
    print("[-] Getting filter button")
    filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
    print("[#] Clicking filter button")
    filter_btn.click()
    print("[#] Waiting for Unread button")
    if email_language == "English":
        WebDriverWait(browser, wait_timeout).until(
            ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
        print("[-] Getting Unread button")
        unread_btn = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
    else:
        WebDriverWait(browser, wait_timeout).until(
            ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Non lu"]')))
        print("[-] Getting Unread button")
        unread_btn = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath('//span[@aria-label="Non lu"]'))
    print("[#] Clicking Unread button")
    unread_btn.click()


def get_inbox_count_new(browser):
    try:
        global inbox_count
        wait_for_page(browser)
        print("[+] Getting INBOX Count")
        if email_language == "English":
            inbox_span = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@title="Inbox"]'))
        else:
            inbox_span = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@title="Boîte de réception"]'))
        inbox_count = int(inbox_span.find_element_by_xpath('../div[2]/span').text)
    except ValueError:
        inbox_count = 0
    except Exception as ex:
        print("/!\ (Error) Getting INBOX Count")
        print(type(ex))
    finally:
        print("[!] INBOX count is: %s" % str(inbox_count))
        return inbox_count


def select_all_msgs_new(browser):
    logger.debug("[+] Select all messages")
    wait_for_page(browser)
    WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH,
                                                                                    '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
    logger.debug("[-] Getting All Msgs checkbox")
    wait_for_page(browser)
    chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
    wait_for_page(browser)
    logger.debug("[-] Select all Msgs")
    logger.debug("[-] Defining hover action")
    hover = ActionChains(browser).move_to_element(chk_bx_bttn)
    logger.debug("[#] Hover over the checkbox")
    hover.perform()
    logger.debug("[#] Waiting for visibility")
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
                                                                                 '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
    logger.debug("[#] Clicking Checkbox")
    chk_bx_bttn.find_element_by_tag_name("button").click()
    wait_for_page(browser)
    logger.debug("[!] End select all messages")


def open_menu_new(browser):
    if email_language == "English":
        menu_btn = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
    else:
        menu_btn = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath('//button[@title="Autres commandes"]'))
    menu_btn.click()
    WebDriverWait(browser, wait_timeout).until(
        ec.visibility_of_element_located(
            (By.XPATH, '//div[@aria-label="Context menu"]')))


def search_for_keyword_new(browser, subject):
    try:
        print("[+] Getting search results for subject: %s" % subject)
        wait_for_page(browser)
        if email_language == "English":
            logger.debug("Waiting for search inbox")
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Activate Search Textbox"]/span[2]')))
            logger.debug("Selecting search inbox")
            search_span = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath(
                    '//button[@aria-label="Activate Search Textbox"]/span[2]'))
            logger.debug("Clicking search inbox")
        else:
            logger.debug("Waiting for search inbox")
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Activer la zone de recherche"]/span[2]')))
            logger.debug("Selecting search inbox")
            search_span = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath(
                    '//button[@aria-label="Activer la zone de recherche"]/span[2]'))
            logger.debug("Clicking search inbox")
        search_span.click()

        logger.debug("Waiting for input")
        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div'
                       '/div[1]/div/form/div/input')))
        logger.debug("Selecting input")
        search_input = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath(
                '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]'
                '/div/form/div/input'))
        logger.debug("sending keyword value")
        search_input.send_keys(subject)
        logger.debug("pressing ENTER key")
        search_input.send_keys(Keys.ENTER)
        logger.debug("Waiting for results")
        if email_language == "English":
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Exit search"]')))
        else:
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Quitter la recherche"]')))
        wait_for_page(browser)
        print("[+] End search for subject: %s" % subject)
    except Exception as ex:
        print("/!\ (Error) Getting INBOX results for Subject: %s" % subject)
        print(type(ex))
        raise


def click_more_results_new(browser):
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/'
                   'div[2]/div[1]/div/div/div[2]/button')))
    more_results = WebDriverWait(browser, wait_timeout).until(
        lambda driver: browser.find_element_by_xpath('//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/'
                                                     'div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/'
                                                     'div[2]/button'))
    more_results.click()


def access_first_mail_new(browser):
    print("[+] Accessing first email")
    first_mail = WebDriverWait(browser, wait_timeout). \
        until(lambda driver: browser.find_element_by_css_selector('span.lvHighlightSubjectClass'))
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, 'span.lvHighlightSubjectClass')))
    first_mail.click()
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.CLASS_NAME, '_rp_01')))


def flag_mail_new(browser, actions):
    try:
        open_menu_new(browser)

        logger.debug("[#] Clicking Flag mail")

        if email_language == "English":
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                (By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
            flag_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@title="Flag for follow-up (Insert)"]'))
            flag_btn.click()
            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                (By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
        else:
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                (By.XPATH, '//span[@title="Indicateur de suivi (Inser)"]')))
            flag_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@title="Indicateur de suivi (Inser)"]'))
            flag_btn.click()
            WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                (By.XPATH, '//span[@title="Indicateur de suivi (Inser)"]')))

        logger.debug("[!] E-mail flagged !")  # TODO-CVC to Count
        if 'AC' not in actions:
            time.sleep(1)
    except StaleElementReferenceException:
        pass
    except TimeoutException:
        pass
    except Exception as ex:
        print("/!\ (Error) Flag Mail Error !")
        print(type(ex))
        raise


def add_contact_new(browser, actions):
    try:
        logger.debug("Getting contact SPAN")
        contact_span = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_xpath(
                '//*[@id="ItemHeader.SenderLabel"]/div[2]/div/span/div/span/span'))
        logger.debug("Hover over contact SPAN")
        hover = ActionChains(browser).move_to_element(contact_span)
        hover.perform()
        logger.debug("Clicking Contact SPAN")
        contact_span.click()
        try:
            logger.debug("Getting add contact buttons")
            if email_language == "English":
                add_contact_buttons = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_elements_by_xpath(
                        '//button[@aria-label="Add to contacts"]'))
            else:
                add_contact_buttons = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_elements_by_xpath(
                        '//button[@aria-label="Ajouter aux contacts"]'))
            logger.debug("looping through buttons")
            for add_contact_button in add_contact_buttons:
                add_contact_button.click()
                logger.debug("Add to contacts button is clicked")
                logger.debug("Waiting for Save contact button")
                if email_language == "English":
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                        (By.XPATH, '//button[@title="Save edit contact"]')))
                    logger.debug("Getting Save contact button")
                    save_contact_button = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@title="Save edit contact"]'))
                    logger.debug("Clicking save to contacts")
                    save_contact_button.click()
                    logger.debug('waiting for Popup to fade away')
                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                        (By.XPATH, '//button[@title="Save edit contact"]')))
                    logger.debug("[-] From-Email added to contacts")  # TODO-CVC to count
                else:
                    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                        (By.XPATH, '//button[@title="Enregistrer la modification du contact"]')))
                    logger.debug("Getting Save contact button")
                    save_contact_button = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@title="Enregistrer la modification du contact"]'))
                    logger.debug("Clicking save to contacts")
                    save_contact_button.click()
                    logger.debug('waiting for Popup to fade away')
                    WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                        (By.XPATH, '//button[@title="Enregistrer la modification du contact"]')))
                    logger.debug("[-] From-Email added to contacts")  # TODO-CVC to count
                if 'CL' not in actions:
                    time.sleep(1)
        except ElementNotVisibleException:
            print("[!] From-Email already Added !")
        except TimeoutException:
            print("[!] From-Email already Added !")
        except NoSuchElementException:
            pass
    except StaleElementReferenceException:
        pass
    except TimeoutException:
        print("/!\ (Error) Add Contact !")
    except Exception as ex:
        print("/!\ (Error) Add Contact !")
        print(type(ex))
        raise


def click_link_new(browser, actions):
    try:
        wait_for_page(browser)
        logger.debug("[-] Getting the Mail 'Body'")
        body = WebDriverWait(browser, wait_timeout).until(lambda driver:
                                                          browser.find_element_by_id('Item.MessageUniqueBody'))
        try:
            logger.debug("[-] Getting the Link in the Mail !")
            body_link = body.find_elements_by_tag_name('a')[1]
        except IndexError:
            print("/!\ (Warning) Link Not Found !")
            body_link = None
        except Exception as ex:
            print("/!\ (Warning) Link Not Found !")
            body_link = None
            print(type(ex))
        wait_for_page(browser)

        if body_link is not None:
            wait_for_page(browser)
            logger.debug("[-] Clicking the Link")
            while not body_link.is_displayed():
                pass
            body_link.click()
            WebDriverWait(browser, wait_timeout).until(lambda driver: len(browser.window_handles) > 1)
            logger.debug("[-] New Tab Opened !")
            wait_for_page(browser)
            logger.debug("[-] Switching to the new Tab !")
            browser.switch_to.window(browser.window_handles[1])
            wait_for_page(browser)
            logger.debug("[-] Link Loaded")
            logger.debug("[-] Closing !")
            browser.close()
            wait_for_page(browser)
            logger.debug("[-] Going Back to Hotmail !")
            browser.switch_to.window(browser.window_handles[0])
            wait_for_page(browser)
            print("[!] Link clicked ! ==> (%s)" % body_link.get_attribute('href'))
    except StaleElementReferenceException:
        pass
    except TimeoutException:
        pass
    except Exception as ex:
        print("/!\ (Error) Click Links !")
        print(type(ex))
        raise


def check_if_no_results_new(browser):
    no_results = True
    try:
        if email_language == "English":
            browser.find_element_by_xpath('//span[text()="We didn\'t find anything to show here."]')
        else:
            browser.find_element_by_xpath('//span[text()="Nous n’avons trouvé aucun élément à afficher ici."]')
    except NoSuchElementException:
        no_results = False
    except Exception as ex:
        print("/!\ (Error) Getting SPAM Results")
        print(type(ex))
    finally:
        wait_for_page(browser)
        return no_results


def access_spam_folder_new(browser, spam_link):
    print("[-] Accessing SPAM folder")
    browser.get(spam_link)
    wait_for_page(browser)

    if email_language == "English":
        browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
    else:
        browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
    wait_for_page(browser)
    time.sleep(1)


def get_spam_count_new(browser):
    spam_count = 0
    try:
        wait_for_page(browser)
        print("Getting spam Count")
        print("Getting Junk span")
        if email_language == "English":
            junk_span = WebDriverWait(browser, wait_timeout). \
                until(lambda driver: browser.find_element_by_xpath('//span[@title="Junk Email"]'))
        else:
            junk_span = WebDriverWait(browser, wait_timeout). \
                until(lambda driver: browser.find_element_by_xpath('//span[@title="Courrier indésirable"]'))
        print("%s" % junk_span.text)
        spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
    except ValueError:
        pass
    except Exception as ex:
        print("/!\ (Error) Getting SPAM Count")
        print(type(ex))
    finally:
        print("[!] SPAM count is : %s" % str(spam_count))
        return spam_count


def safe_spam_new(browser, spam_link, inbox_link):
    while get_spam_count_new(browser) > 0:
        try:
            # region Accessing 1st messages
            logger.debug("Getting Subject SPAN")
            first_mail = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//div[@unselectable="on"]/div/span'))
            logger.debug("Done ! Subject is ==> %s" % first_mail.text)
            logger.debug("Clicking Subject SPAN")
            if first_mail.is_displayed():
                first_mail.click()
            # endregion

            # region Clicking MANS button
            try:
                logger.debug("Getting Show Content button")
                show_content_btn = WebDriverWait(browser, 5).until(lambda driver: browser.find_element_by_xpath(
                    '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]'
                    '/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]'))

                logger.debug("Clicking Show Content")
                if show_content_btn.is_displayed():
                    show_content_btn.click()
                    logger.debug("[-] 'Show content' button clicked")
            except TimeoutException:
                logger.debug("! 'Show content' button not found !")

            try:
                logger.debug("Getting MANS button")
                if email_language == "English":
                    mans_btn = WebDriverWait(browser, 5).until(
                        lambda driver: browser.find_element_by_xpath('//span[text()="It\'s not spam"]'))
                else:
                    mans_btn = WebDriverWait(browser, 5).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//span[text()="Ceci n’est pas du courrier indésirable"]'))

                logger.debug("Clicking MANS button")
                if mans_btn.is_displayed():
                    mans_btn.click()
                    logger.debug("[-] 'Not SPAM' button clicked")
                else:
                    logger.debug("Getting MANS button")
                    if email_language == "English":
                        mans_btn = WebDriverWait(browser, 5).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                    else:
                        mans_btn = WebDriverWait(browser, 5).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Déplacer un message légitime dans la boîte de réception"]'))
                    logger.debug("Clicking MANS button")
                    # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                    if mans_btn.is_displayed():
                        mans_btn.click()
                        logger.debug("[-] 'Not SPAM' button clicked")
                        logger.debug("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                        logger.debug("Done !")
                        logger.debug("[-] Mark SPAM as Safe Button is Clicked")
            except TimeoutException:
                logger.debug("Getting MANS button")
                if email_language == "English":
                    mans_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                else:
                    mans_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@title="Déplacer un message légitime dans la boîte de réception"]'))
                logger.debug("Clicking MANS button")
                if mans_btn.is_displayed():
                    mans_btn.click()
                    logger.debug("[-] 'Not SPAM' button clicked")
                    logger.debug("Waiting for action to be performed")
                    WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                    logger.debug("Done !")
                    logger.debug("[-] Mark SPAM as Safe Button is Clicked")
            logger.debug("[!] Getting Next Mail")
            # endregion

        except StaleElementReferenceException:
            pass
        except TimeoutException:
            if email_language == "English":
                print("/!\ (Error) Mark SPAM as Read Time Out")
                browser.find_element_by_xpath('//span[text()="Inbox"]').click()
                time.sleep(2)
                wait_for_page(browser)
                browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
            else:
                print("/!\ (Error) Mark SPAM as Read Time Out")
                browser.find_element_by_xpath('//span[text()="Boîte de réception"]').click()
                time.sleep(2)
                wait_for_page(browser)
                browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
            wait_for_page(browser)
        except Exception as ex:
            logger.debug("/!\ (Error) Mark SPAM as Safe")
            print(type(ex))
            raise

# endregion


def report_new_version(browser, actions, subject):
    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
    inbox_link = spam_link.replace("/junkemail", "/inbox")

    # region Spam Actions
    if ('RS' in actions) or ('NS' in actions) or ('SS' in actions):
        access_spam_folder_new(browser, spam_link)

    # region Mark Spam as read
    if ('RS' in actions) and ('SS' not in actions):
        print("[+] Mark SPAM as read Actions :")
        filter_unread_new(browser)

        # region looping through results
        while not check_if_no_results_new(browser):
            try:
                select_all_msgs_new(browser)

                open_menu_new(browser)

                # region Clicking MAR button
                logger.debug("[!] Getting Menu button")
                if email_language == "English":
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
                        '//button[@aria-label="Mark as read (Q)"]'))
                else:
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//button[@aria-label="Marquer comme lu (Q)"]'))
                logger.debug("[#] Clicking MAR button")
                mar_bttn.click()
                logger.debug("[!] Selection Marked as READ")
                time.sleep(1)
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                if email_language == "English":
                    print("/!\ (Error) Mark SPAM as Read Time Out")
                    browser.find_element_by_xpath('//span[text()="Inbox"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
                    wait_for_page(browser)
                else:
                    print("/!\ (Error) Mark SPAM as Read Time Out")
                    browser.find_element_by_xpath('//span[text()="Boîte de réception"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
                    wait_for_page(browser)

                filter_unread_new(browser)
                continue
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as read")
                print(type(ex))
                raise
        # endregion
        print("[!] Done marking SPAM as Read!\n")
    # endregion

    # region Mark as Not SPAM
    if ('NS' in actions) and ('SS' not in actions):
        print("[+] Mark as not SPAM action")

        if 'RS' in actions:
            access_spam_folder_new(browser, spam_link)

        # region looping through pages
        while get_spam_count_new(browser) > 0:
            try:
                wait_for_page(browser)
                select_all_msgs_new(browser)

                # region Clicking MANS button
                try:
                    if email_language == "English":
                        print("Clicking Mark as not SPAM Button")
                        print("Getting MANS button")
                        mans_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                        wait_for_page(browser)
                        print("Waiting for MANS button")
                        WebDriverWait(browser, 3).until(ec.visibility_of_element_located(
                            (By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                        print("Clicking MANS button")
                        mans_btn.click()
                        print("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
                            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/div[1]/span').text == "Junk Email")
                        print("Sending ESC key")
                        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                        print("Waiting for invisibility of element !")
                        WebDriverWait(browser, 3).until(
                            ec.invisibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        print("[-] E-mail marked as not SPAM !")
                    else:
                        print("Clicking Mark as not SPAM Button")
                        print("Getting MANS button")
                        mans_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Déplacer un message légitime dans la boîte de réception"]'))
                        wait_for_page(browser)
                        print("Waiting for MANS button")
                        WebDriverWait(browser, 3).until(ec.visibility_of_element_located(
                            (By.XPATH,
                             '//button[@title="Déplacer un message légitime dans la boîte de réception"]')))
                        print("Clicking MANS button")
                        mans_btn.click()
                        print("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
                            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/div[1]/span').text == "Junk Email")
                        print("Sending ESC key")
                        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                        print("Waiting for invisibility of element !")
                        WebDriverWait(browser, 3).until(
                            ec.invisibility_of_element_located((By.XPATH, '//*[@title="Autres commandes"]')))
                        print("[-] E-mail marked as not SPAM !")
                except TimeoutException:
                    pass
                print("Done !")
                # endregion

                if email_language == "English":
                    print("/!\ (Error) Mark SPAM as Read Time Out")
                    browser.find_element_by_xpath('//span[text()="Inbox"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
                    wait_for_page(browser)
                else:
                    print("/!\ (Error) Mark SPAM as Read Time Out")
                    browser.find_element_by_xpath('//span[text()="Boîte de réception"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
                    wait_for_page(browser)

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
                break
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as Read")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking as not SPAM\n")
    # endregion

    # region Mark SPAM as Safe
    if 'SS' in actions:
        print("[+] Mark SPAM as Safe Actions")
        safe_spam_new(browser, spam_link, inbox_link)
        print("[!] Done marking SPAM as Safe !\n")
    # endregion

    # endregion

    # region Inbox Actions

    # region Accessing INBOX folder
    if ('AC' in actions) or ('CL' in actions) or ('FM' in actions):
        try:
            print("[-] Accessing INBOX folder")
            browser.get(inbox_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (Error) Getting INBOX list")
            print(type(ex))
    # endregion

    # region Mark inbox as Read
    if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):
        print("[+] Mark INBOX as read Actions :")

        filter_unread_new(browser)

        # region looping through results
        while get_inbox_count_new(browser) > 0:
            try:
                select_all_msgs_new(browser)

                open_menu_new(browser)

                # region Clicking MAR button
                if email_language == "English":
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Mark as read (Q)"]'))
                else:
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Marquer comme lu (Q)"]'))

                mar_bttn.click()
                print("[!] Selection Marked as READ")
                # endregion

                pass
            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Mark INBOX as Read Timed Out")
                browser.get(spam_link)
                wait_for_page(browser)
                browser.get(inbox_link)
                wait_for_page(browser)
                filter_unread_new(browser)
            except Exception as ex:
                print("/!\ (Error) Mark INBOX as read")
                print(type(ex))
                raise
        # endregion

        print("[!] Done marking INBOX as read !\n")
    # endregion

    # region Add contact Inbox / click Links / Flag Mail
    if ('AC' in actions) or ('CL' in actions) or ('FM' in actions):
        print("[+] Add Contact / Click Links / Flag Mail Actions: ")

        browser.get(spam_link)
        wait_for_page(browser)
        browser.get(inbox_link)
        wait_for_page(browser)

        # region Controller Settings
        search_for_keyword_new(browser, subject)
        no_results = True
        time.sleep(2)
        try:
            noresults_span = browser.find_element_by_class_name("_lvv_c1")
            no_results = noresults_span.is_displayed()
        except NoSuchElementException:
            no_results = False
        except Exception as e:
            print(type(e))
            raise
        # endregion

        if no_results:
            print("[!] No results found for subject: %s" % subject)
        else:
            click_more_results_new(browser)

            access_first_mail_new(browser)

            # region Getting loop settings
            if email_language == "English":
                next_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//button[@title="Next"]'))
            else:
                next_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//button[@title="Suivant"]'))
            last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
            last_page_checked = last_page
            # endregion

            # region Looping through results
            while not last_page_checked:
                if 'FM' in actions:
                    flag_mail_new(browser, actions)
                if 'AC' in actions:
                    add_contact_new(browser, actions)
                if 'CL' in actions:
                    click_link_new(browser, actions)

                # region Checking if it was the last page
                last_page_checked = last_page if last_page else False
                last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                logger.debug("[#] Getting next Mail ...")
                next_btn.click()
                time.sleep(1)
                # endregion

            # endregion
            pass
        print("[!] Done Add Contact / Click Links / Flag Mail\n")
    # endregion
    # endregion
    pass

# endregion


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, **kwargs):
    # region Settings
    actions = str(kwargs.get('actions', None)).split(',')
    subject = kwargs.get('subject', None)
    global wait_timeout
    wait_timeout = kwargs.get('wait_timeout', 15)
    hide_browser = kwargs.get('hide_browser', False)
    mail_args = kwargs.get('email', None)
    mail = mail_args['login']
    pswd = mail_args['password']
    proxy_args = kwargs.get('proxy', None)

    if proxy_args is not None:
        proxy = proxy_args['ip_address']
        port = str(proxy_args['ip_port'])
    else:
        proxy = None
        port = None

    if proxy is not None and port is not None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s:%s' % (proxy, port))
        browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-startup-window')
        browser = webdriver.Chrome(executable_path="chromedriver")
    browser.maximize_window()
    if hide_browser:
        browser.set_window_position(-2000, 0)
    global link
    # endregion

    print("\n******\nStarting JOB for :\n*-Actions: %s\n*-Subject: %s\n*-Email: %s\n*-Password: %s\n*-Proxy: %s\n*-"
          "Port: %s\n******\n" % (kwargs.get('actions', None), subject, mail, pswd, proxy, port))

    # try:
    print('[+] Opening Hotmail')
    browser.get(link)
    print('[!] Hotmail Opened')

    print("[+] Starting Connection")
    connect(browser, mail, pswd)
    print("[!] End Connection")

    print("[+] Checking if Account is blocked")
    check_if_verified(browser)
    print("[!] End account blocked check")

    if 'https://account.live.com/' in browser.current_url:
        browser.get(link)

    print("[+] Checking email version")
    check_version(browser)
    print("[!] End checking email version")

    print("[+] Checking email language")
    check_email_language(browser)
    print("[!] End checking email language")

    if version == "old":
        print("(###) Starting actions for OLD e-mail version\n")
        report_old_version(browser, actions, subject)
    else:
        print("(###) Starting actions for NEW e-mail version\n")

        print("[+] Setting mailbox display")
        configure_mailbox(browser)
        print("[+] End setting mailbox display")

        print("[+] Starting Actions")
        report_new_version(browser, actions, subject)
        print("[+] End Actions")

    print("###************************************************************************###")
    print('        [!] [-] Finished Actions for %s [-] (!)' % mail)
    print("###************************************************************************###")
    browser.quit()
