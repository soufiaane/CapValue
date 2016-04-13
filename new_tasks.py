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
wait_timeout = 20
email_language = 'Unknown'
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
    except Exception as e:
        print(type(e))


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
    except Exception as e:
        print("/!\ (Error) Getting Mailbox Language !")
        print(type(e))


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
        print("/!\ (Error) Check Display Settings")
        print(type(exc))
# endregion


# region MailBox Functions
def mark_as_read_new(browser):
    pass


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
    print("(!) Marking INBOX as read for this page")
    wait_for_page(browser)
    WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH,
        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
    print("Getting All Msgs checkbox")
    wait_for_page(browser)
    chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
    wait_for_page(browser)
    print("Select all Msgs")
    print("Defining hover action")
    hover = ActionChains(browser).move_to_element(chk_bx_bttn)
    print("Hover over the checkbox")
    hover.perform()
    print("Hover Done")
    print("Waiting for visibility")
    WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
    print("Element is visible")
    print("Clicking Checkbox")
    chk_bx_bttn.find_element_by_tag_name("button").click()
    wait_for_page(browser)
# endregion


# region Old Version
def report_old_version(browser, actions):

    # region Spam Actions

    # region Mark Spam as read
    if ('RS' in actions) and ('SS' not in actions):  #

        # region Controllers Settings
        print("[+] Read SPAM Actions")
        wait_for_page(browser)
        try:
            wait_for_page(browser)
            spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
            print("[-] Accessink SPAM folder : %s" % spam_link)
            browser.get(spam_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (Error) Accessink SPAM folder ")
            print(type(ex))

        try:
            wait_for_page(browser)
            browser.find_element_by_id("NoMsgs")
            last_page_checked = True
            print("(!) SPAM folder is empty, Skipping read SPAM actions!")
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

                # region Selecting alls messages
                print("[-] Marking SPAM as read for this page")
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                print("Getting All Msgs checkbox")
                wait_for_page(browser)
                chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('msgChkAll'))
                wait_for_page(browser)
                print("Select all Msgs")
                chk_bx_bttn.click()
                wait_for_page(browser)
                print("CheckBox is clicked !")
                # endregion

                # region Clicking menu
                print("Getting Menu Button")

                try:
                    if email_language == "English":
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        wait_for_page(browser)
                        print("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        wait_for_page(browser)
                    else:
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//*[@title=" Autres commandes"]'))
                        wait_for_page(browser)
                        print("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.XPATH, '//*[@title=" Autres commandes"]')))
                        wait_for_page(browser)
                except TimeoutException:
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//*[@title="更多命令"]'))
                    wait_for_page(browser)
                    print("Click Menu")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.XPATH, '//*[@title="更多命令"]')))
                    wait_for_page(browser)

                menu_btn.click()
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                # endregion

                # region Clicking MAR button
                print("+ Clicking Mark as Read Button")  # TODO-CVC Counter
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
                print("Done !")
                # endregion

                # region Checking if it was the last page
                last_page_checked = last_page if last_page else False
                next_page_link = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('nextPageLink'))
                if next_page_link.is_displayed():
                    print("Accessing Next Page")
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
                print("/!\ (Error) Timed Out")
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as read")
                print(type(ex))
                break
        # endregion

        print("(!) Done marking SPAM as read\n")

    # endregion

    # region Mark as Not SPAM
    if ('NS' in actions) and ('SS' not in actions):  # Not SPAM

        # region Controllers Settings
        print("[+] Mark as Not SPAM Actions")
        wait_for_page(browser)

        try:
            wait_for_page(browser)
            spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
            browser.get(spam_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (Error) Accessink SPAM folder ")
            print(type(ex))

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
                print("[-] Marking as not SPAM for this page")
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                print("Getting All Msgs checkbox")
                wait_for_page(browser)
                chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('msgChkAll'))
                wait_for_page(browser)
                print("Select all Msgs")
                chk_bx_bttn.click()
                wait_for_page(browser)
                print("CheckBox is clicked !")
                # endregion

                # region Clicking MANS button
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                wait_for_page(browser)
                not_spam_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                wait_for_page(browser)
                not_spam_btn.click()
                print("(!) 'Not Spam' Button Clicked !")
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
                    print("(!) Last page !")
                except NoSuchElementException:
                    still_results = True
                    # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
            except Exception as ex:
                print("/!\ (Error) Mark as not SPAM")
                print(type(ex))
                break
        # endregion

        print("(!) Done marking e-mails as not spam\n")
    # endregion

    # region Mark SPAM as SAFE
    if 'SS' in actions:

        # region Controllers Settings
        print("[+] Mark SPAM as safe actions :")
        wait_for_page(browser)
        print("[-] Getting SPAM Folder")

        try:
            wait_for_page(browser)
            spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/?fid=fljunk'
            print("Accessink SPAM folder : %s" % spam_link)
            browser.get(spam_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (ERROR) Accessink SPAM folder")
            print(type(ex))

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
                print("Getting Email List Group !")
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mailList')))
                email_list = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_css_selector('ul.mailList'))
                print("Getting All Emails from Group")
                wait_for_page(browser)
                emails = email_list.find_elements_by_tag_name('li')
                print("[-] Clicking the first e-mail")
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
                print("[-] E-mail marked as Safe")  # TODO-CVC
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
                    print("(!) Last page !")
                except NoSuchElementException:
                    still_results = True
                    # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
                # region Clicking MANS button
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.ID, 'MarkAsNotJunk')))
                wait_for_page(browser)
                not_spam_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsNotJunk'))
                wait_for_page(browser)
                not_spam_btn.click()
                print("(!) 'Not Spam' Button Clicked !")
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
                    print("(!) Last page !")
                except NoSuchElementException:
                    still_results = True
                    # endregion
                    # endregion
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as safe!")
                print(type(ex))
                break
        # endregion

        print("(!) Done marking SPAM as safe\n")
    # endregion

    # endregion

    # region Inbox Actions

    # region Mark inbox as Read
    if ('RI' in actions) and ('CL' not in actions) and ('AC' not in actions):

        # region Controllers Settings
        print("[+] Mark INBOX as read Actions")
        print("[-] Getting unread messages for Subject: %s" % keyword)
        wait_for_page(browser)

        keyword_link = str(browser.current_url)[:str(browser.current_url).index(
            '.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&scat=1&sdr=4&satt=0'
        browser.get(keyword_link)
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

                # region Selecting alls messages
                print("[-] Marking INBOX as read for this page")
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.FilterSelector')))
                print("Getting All Msgs checkbox")
                wait_for_page(browser)
                chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('msgChkAll'))
                wait_for_page(browser)
                print("Select all Msgs")
                chk_bx_bttn.click()
                wait_for_page(browser)
                print("CheckBox is clicked !")
                # endregion

                # region Clicking menu
                try:
                    if email_language == "English":
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//*[@title="More commands"]'))
                        wait_for_page(browser)
                        print("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.XPATH, '//*[@title="More commands"]')))
                        wait_for_page(browser)
                    else:
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//*[@title=" Autres commandes"]'))
                        wait_for_page(browser)
                        print("Click Menu")
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.XPATH, '//*[@title=" Autres commandes"]')))
                        wait_for_page(browser)
                except TimeoutException:
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//*[@title="更多命令"]'))
                    wait_for_page(browser)
                    print("Click Menu")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.XPATH, '//*[@title="更多命令"]')))
                    wait_for_page(browser)
                menu_btn.click()
                # endregion

                # region Clicking MAR button
                print("[-] Clicking Mark as Read Button")  # TODO-CVC
                mar_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_id('MarkAsRead'))
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.ID, 'MarkAsRead')))
                mar_btn.click()
                try:
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    WebDriverWait(browser, wait_timeout).until(
                        ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                except TimeoutException:
                    pass
                print("Done !")
                # endregion

                # region Checking if it was the last page
                try:
                    browser.find_element_by_id("NoMsgs")
                    still_results = False
                    print("(!) Last page !")
                except NoSuchElementException:
                    still_results = True
                    # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
                continue
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as read")
                print(type(ex))
                break
        # endregion

        print("(!) Done marking INBOX as read\n")
    # endregion

    # region Flag mail
    if ('FM' in actions) and ('AC' not in actions) and ('CL' not in actions):

        # region Controllers Settings
        print("[+] Flag INBOX Actions")
        print("[-] Getting result for Subject: %s" % keyword)
        wait_for_page(browser)

        keyword_link_flag = str(browser.current_url)[:str(browser.current_url).index(
            '.com')] + '.com/?fid=flsearch&srch=1&skws=' + keyword + '&sdr=4&satt=0'
        browser.get(keyword_link_flag)
        wait_for_page(browser)

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
                print("[-] Flaging Mails for this Page !")
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
                        flag.click()  # TODO-CVC Count this
                        wait_for_page(browser)
                        time.sleep(1)
                        print("[-] E-mail flagged")
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
                    print("(!) Accessing Next Page")
                    try:
                        WebDriverWait(browser, wait_timeout).until(
                            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                        WebDriverWait(browser, wait_timeout).until(
                            ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div.c_h_flyingDots')))
                    except TimeoutException:
                        pass
                next_page_disabled_flag = browser.find_element_by_css_selector('div.NextPageDisabled')
                last_page_flag = next_page_disabled_flag.is_displayed()
                print("Last page : %s" % last_page_flag)
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
                break
            except Exception as ex:
                print("/!\ (Error) Flag INBOX  Error")
                print(type(ex))
                break
        # endregion

        print("(!) Done Flaging Mails\n")
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
            print("(!) INBOX folder is empty")
            print("(!) Skipping Add Contact / Click Links / Flag Mail actions")
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
                        print("(!) Email already Flagged !")
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
                        print('(!) Contact Already Exist')
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
                        print("(!) Link Not Found")
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
                    print("(!) Last page")
                else:
                    last_page_ac = False
                wait_for_page(browser)
                if not last_page_ac:
                    print("(!) Getting next e-mail ...")
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

        print("(!) Done Add Contact / Click Links / Flag Mail\n")
    # endregion
    # endregion

    pass
# endregion


# region New Version
def report_new_version(browser, actions):
    spam_link = str(browser.current_url)[:str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
    inbox_link = spam_link.replace("/junkemail", "/inbox")

    # region Spam Actions

    # region Mark Spam as read
    if ('RS' in actions) and ('SS' not in actions):
        # region Controllers Settings
        print("[+] Mark SPAM as read Actions :")
        wait_for_page(browser)
        spam_link = str(browser.current_url)[
                    :str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
        inbox_link = spam_link.replace("/junkemail", "/inbox")

        # region Accessing SPAM folder
        print("[-] Getting SPAM folder")
        browser.get(spam_link)
        wait_for_page(browser)
        if email_language == "English":
            browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
        else:
            browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
        wait_for_page(browser)
        time.sleep(1)
        # endregion

        # region Filtering results
        print("Getting filter button")
        filter_btn = WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
        print("Clicking filter button")
        filter_btn.click()
        print("Waiting for Unread button")
        if email_language == "English":
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
            print("Getting for Unread button")
            unread_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
            print("Clicking Unread button")
            unread_btn.click()
        else:
            WebDriverWait(browser, wait_timeout).until(
                ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Non lu"]')))
            print("Getting for Unread button")
            unread_btn = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath('//span[@aria-label="Non lu"]'))
            print("Clicking Unread button")
            unread_btn.click()
        # endregion

        # region Checking results
        try:
            if email_language == "English":
                noresult_span = browser.find_element_by_xpath(
                    '//span[text()="We didn\'t find anything to show here."]')
            else:
                noresult_span = browser.find_element_by_xpath(
                    '//span[text()="Nous n’avons trouvé aucun élément à afficher ici."]')
            wait_for_page(browser)
            no_results = noresult_span.is_displayed()
        except NoSuchElementException:
            no_results = False
        except Exception as ex:
            print("/!\ (Error) Getting SPAM Results")
            print(type(ex))
            no_results = True
        # endregion

        # endregion

        # region looping through results
        while not no_results:
            try:
                # region Checking results
                try:
                    if email_language == "English":
                        noresult_span = browser.find_element_by_xpath(
                            '//span[text()="We didn\'t find anything to show here."]')
                    else:
                        noresult_span = browser.find_element_by_xpath(
                            '//span[text()="Nous n’avons trouvé aucun élément à afficher ici."]')
                    wait_for_page(browser)
                    no_results = noresult_span.is_displayed()
                except NoSuchElementException:
                    no_results = False
                except Exception as ex:
                    print("/!\ (Error) Getting SPAM Results")
                    print(type(ex))
                    no_results = True
                    break
                # endregion

                # region Selecting alls messages
                print("(!) Marking SPAM as read for this page")
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH,
                                                                                                '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                print("Getting All Msgs checkbox")
                wait_for_page(browser)
                chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath(
                        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                wait_for_page(browser)
                print("Select all Msgs")
                print("Defining hover action")
                hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                print("Hover over the checkbox")
                hover.perform()
                print("Hover Done")
                print("Waiting for visibility")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
                                                                                             '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                print("Element is visible")
                print("Clicking Checkbox")
                chk_bx_bttn.find_element_by_tag_name("button").click()
                wait_for_page(browser)
                # endregion

                # region Clicking MAR button
                print("Getting Menu button")
                if email_language == "English":
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                    print("Clicking menu button")
                    menu_btn.click()
                    print("Waiting for MAR button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located(
                            (By.XPATH, '//button[@aria-label="Mark as read (Q)"]')))
                    print("Getting MAR button")
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Mark as read (Q)"]'))
                    print("Clicking MAR button")
                    mar_bttn.click()
                else:
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//button[@title="Autres commandes"]'))
                    print("Clicking menu button")
                    menu_btn.click()
                    print("Waiting for MAR button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located(
                            (By.XPATH, '//button[@aria-label="Marquer comme lu (Q)"]')))
                    print("Getting MAR button")
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Marquer comme lu (Q)"]'))
                    print("Clicking MAR button")
                    mar_bttn.click()
                print("(!) Selection Marked as READ")
                time.sleep(1)
                # endregion
            except StaleElementReferenceException:
                pass
            except TimeoutException:
                if email_language == "English":
                    print("/!\ (Error) Mark SPAM as Read Timed Out")
                    browser.find_element_by_xpath('//span[text()="Inbox"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Junk Email"]').click()
                    wait_for_page(browser)
                else:
                    print("/!\ (Error) Mark SPAM as Read Timed Out")
                    browser.find_element_by_xpath('//span[text()="Boîte de réception"]').click()
                    time.sleep(1)
                    wait_for_page(browser)
                    browser.find_element_by_xpath('//span[text()="Courrier indésirable"]').click()
                    wait_for_page(browser)

                # region Filtering results
                print("Getting filter button")
                filter_btn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath(
                        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/button'))
                print("Clicking filter button")
                filter_btn.click()
                if email_language == "English":
                    print("Waiting for Unread button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Unread"]')))
                    print("Getting for Unread button")
                    unread_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//span[@aria-label="Unread"]'))
                    print("Clicking Unread button")
                    unread_btn.click()
                    print("Done !")
                else:
                    print("Waiting for Unread button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Non lu"]')))
                    print("Getting for Unread button")
                    unread_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//span[@aria-label="Non lu"]'))
                    print("Clicking Unread button")
                    unread_btn.click()
                    print("Done !")
                # endregion

                # region Checking results
                try:
                    if email_language == "English":
                        noresult_span = browser.find_element_by_xpath(
                            '//span[text()="We didn\'t find anything to show here."]')
                        break
                    else:
                        noresult_span = browser.find_element_by_xpath(
                            '//span[text()="Nous n’avons trouvé aucun élément à afficher ici."]')
                    wait_for_page(browser)
                    no_results = noresult_span.is_displayed()
                except NoSuchElementException:
                    no_results = False
                except Exception as ex:
                    print("/!\ (Error) Getting SPAM Results")
                    print(type(ex))
                    no_results = True
                    break
                    # endregion

            except Exception as ex:
                print("/!\ (Error) Mark SPAM as read")
                print(type(ex))
                break
        # endregion
        print("(!) Done marking SPAM as Read!\n")
    # endregion

    # region Mark as Not SPAM
    if ('NS' in actions) and ('SS' not in actions):

        # region Controllers Settings
        print("[+] Mark as not SPAM action")
        wait_for_page(browser)
        spam_link = str(browser.current_url)[
                    :str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
        inbox_link = spam_link.replace("/junkemail", "/inbox")

        # region Accessing SPAM folder
        try:
            print("[-] Getting SPAM folder")
            wait_for_page(browser)
            print("Accessink SPAM folder : %s" % spam_link)
            browser.get(spam_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (Error) Accessink SPAM folder")
            print(type(ex))
        # endregion

        # region Checking results
        spam_count = 0
        try:
            wait_for_page(browser)
            print("Getting spam Count")
            print("Getting Junk span")
            if email_language == "English":
                junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
            else:
                junk_span = browser.find_element_by_xpath('//span[@title="Courrier indésirable"]')
            print("%s" % junk_span.text)
            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
        except ValueError:
            pass
        except Exception as ex:
            print("/!\ (Error) Getting SPAM Count")
            print(type(ex))
            spam_count = 0
        finally:
            print("(!) SPAM count is : %s" % str(spam_count))  # TODO-CVC to Count
        # endregion

        # endregion

        # region looping through pages
        while spam_count > 0:
            try:

                # region Selecting alls messages
                print("(!) Marking SPAM as read for this page")
                wait_for_page(browser)
                WebDriverWait(browser, wait_timeout).until(ec.presence_of_all_elements_located((By.XPATH,
                                                                                                '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                print("Getting All Msgs checkbox")
                wait_for_page(browser)
                chk_bx_bttn = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath(
                        '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]'))
                wait_for_page(browser)
                print("Select all Msgs")
                print("Defining hover action")
                hover = ActionChains(browser).move_to_element(chk_bx_bttn)
                print("Hover over the checkbox")
                hover.perform()
                print("Hover Done")
                print("Waiting for visibility")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
                                                                                             '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/button')))
                print("Element is visible")
                print("Clicking Checkbox")
                chk_bx_bttn.find_element_by_tag_name("button").click()
                wait_for_page(browser)
                # endregion

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
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                            (By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                        print("Clicking MANS button")
                        mans_btn.click()
                        print("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(lambda driver: browser.find_element_by_xpath(
                            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[3]/div/div[2]/div[1]/span').text == "Junk Email")
                        print("Sending ESC key")
                        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                        print("Waiting for invisibility of element !")
                        WebDriverWait(browser, wait_timeout).until(
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
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
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
                        WebDriverWait(browser, wait_timeout).until(
                            ec.invisibility_of_element_located((By.XPATH, '//*[@title="Autres commandes"]')))
                        print("[-] E-mail marked as not SPAM !")
                except TimeoutException:
                    pass
                print("Done !")
                # endregion

                # region Checking if it was the last page
                try:
                    wait_for_page(browser)
                    print("Getting spam Count")
                    print("Getting Junk span")
                    if email_language == "English":
                        junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    else:
                        junk_span = browser.find_element_by_xpath('//span[@title="Courrier indésirable"]')
                    print("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    spam_count = 0
                except Exception as ex:
                    print("/!\ (Error) Getting SPAM Count")
                    print(type(ex))
                    spam_count = 0
                finally:
                    print("New SPAM count is : %s" % str(spam_count))
                    browser.get(inbox_link)
                    wait_for_page(browser)
                    browser.get(spam_link)
                    wait_for_page(browser)
                    # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Timed Out")
                break
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as Read")
                print(type(ex))
                break
        # endregion

        print("(!) Done marking as not SPAM\n")
    # endregion

    # region Mark SPAM as Safe
    if 'SS' in actions:
        # region Controllers Settings
        print("[+] Mark SPAM as Safe Actions")
        wait_for_page(browser)
        spam_link = str(browser.current_url)[
                    :str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
        inbox_link = spam_link.replace("/junkemail", "/inbox")

        # region Accessing SPAM folder
        try:
            print("[-] Getting SPAM folder")
            browser.get(inbox_link)
            wait_for_page(browser)
            browser.get(spam_link)
            wait_for_page(browser)
        except Exception as ex:
            print("/!\ (Error) Accessing SPAM folder")
            print(type(ex))
        # endregion

        # region Checking results
        spam_count = 0
        try:
            wait_for_page(browser)
            print("Getting spam Count")
            print("Getting Junk span")
            if email_language == "English":
                junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
            else:
                junk_span = browser.find_element_by_xpath('//span[@title="Courrier indésirable"]')
            print("%s" % junk_span.text)
            spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
        except ValueError:
            pass
        except Exception as ex:
            print("/!\ (Error) Getting SPAM Count")
            print(type(ex))
            spam_count = 0
        print("(!) SPAM count is : %s" % str(spam_count))
        # endregion

        # endregion

        # region looping through pages
        while spam_count > 0:
            try:
                try:
                    wait_for_page(browser)
                    print("Getting spam Count")
                    print("Getting Junk span")
                    if email_language == "English":
                        junk_span = browser.find_element_by_xpath('//span[@title="Junk Email"]')
                    else:
                        junk_span = browser.find_element_by_xpath('//span[@title="Courrier indésirable"]')
                    print("%s" % junk_span.text)
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    pass
                except Exception as ex:
                    print("/!\ (Error) Getting SPAM Count")
                    print(type(ex))
                    spam_count = 0
                print("(!) SPAM count is : %s" % str(spam_count))

                # region Accessing 1st messages
                print("Getting Subject SPAN")
                first_mail = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath('//div[@unselectable="on"]/div/span'))
                print("Done ! Subject is ==> %s" % first_mail.text)
                print("Clicking Subject SPAN")
                if first_mail.is_displayed():
                    first_mail.click()
                # endregion

                # region Clicking MANS button
                try:
                    print("Getting Show Content button")
                    show_content_btn = WebDriverWait(browser, 5).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]'))
                    print("Clicking Show Content")
                    # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[4]/div[2]/div/div[1]/div[4]/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/div[10]/div[2]/div/div/div/div/div[2]/div/a[2]')))
                    if show_content_btn.is_displayed():
                        show_content_btn.click()
                        print("[-] 'Show content' button clicked")
                except TimeoutException:
                    print("! 'Show content' button not found !")
                except Exception as ex:
                    print("/!\ (Error) Clicking 'Show content' button")
                    print(type(ex))
                try:
                    print("Getting MANS button")
                    if email_language == "English":
                        mans_btn = WebDriverWait(browser, 5).until(
                            lambda driver: browser.find_element_by_xpath('//span[text()="It\'s not spam"]'))
                    else:
                        mans_btn = WebDriverWait(browser, 5).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//span[text()="Ceci n’est pas du courrier indésirable"]'))

                    print("Clicking MANS button")
                    # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                    if mans_btn.is_displayed():
                        mans_btn.click()
                        print("[-] 'Not SPAM' button clicked")
                    else:
                        print("Getting MANS button")
                        if email_language == "English":
                            mans_btn = WebDriverWait(browser, 5).until(
                                lambda driver: browser.find_element_by_xpath(
                                    '//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                        else:
                            mans_btn = WebDriverWait(browser, 5).until(
                                lambda driver: browser.find_element_by_xpath(
                                    '//button[@title="Déplacer un message légitime dans la boîte de réception"]'))
                        print("Clicking MANS button")
                        # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                        if mans_btn.is_displayed():
                            mans_btn.click()
                            print("[-] 'Not SPAM' button clicked")
                            print("Waiting for action to be performed")
                            WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                            print("Done !")
                            print("[-] Mark SPAM as Safe Button is Clicked")
                except TimeoutException:
                    print("Getting MANS button")
                    if email_language == "English":
                        mans_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Move a message that isn\'t Junk to the Inbox"]'))
                    else:
                        mans_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//button[@title="Déplacer un message légitime dans la boîte de réception"]'))
                    print("Clicking MANS button")
                    # WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH, '//button[@title="Move a message that isn\'t Junk to the Inbox"]')))
                    if mans_btn.is_displayed():
                        mans_btn.click()
                        print("[-] 'Not SPAM' button clicked")
                        print("Waiting for action to be performed")
                        WebDriverWait(browser, wait_timeout).until(ec.staleness_of(first_mail))
                        print("Done !")
                        print("[-] Mark SPAM as Safe Button is Clicked")
                print("(!) Getting Next Mail")
                # endregion

                # region Checking if it was the last page
                try:
                    wait_for_page(browser)
                    print("Getting spam Count")
                    if email_language == "English":
                        junk_span = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//span[@title="Junk Email"]'))
                    else:
                        junk_span = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//span[@title="Courrier indésirable"]'))
                    print("Getting Junk span")
                    spam_count = int(junk_span.find_element_by_xpath('../div[2]/span').text)
                except ValueError:
                    spam_count = 0
                except Exception as ex:
                    print("/!\ (Error) Getting SPAM Count")
                    print(type(ex))
                    spam_count = 0
                print("(!) New SPAM count is : %s" % str(spam_count))
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Mark SPAM as Safe  Timed Out")
                browser.get(inbox_link)
                wait_for_page(browser)
                browser.get(spam_link)
                wait_for_page(browser)
                continue
            except Exception as ex:
                print("/!\ (Error) Mark SPAM as Safe")
                print(type(ex))
        # endregion

        print("(!) Done marking SPAM as Safe !\n")
    # endregion

    # endregion

    # region Inbox Actions

    # region Accessing INBOX folder
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

                # region Clicking MAR button
                if email_language == "English":
                    print("Getting Menu button")
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                    print("Clicking menu button")
                    menu_btn.click()
                    print("Waiting for MAR button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located(
                            (By.XPATH, '//button[@aria-label="Mark as read (Q)"]')))
                    print("Getting MAR button")
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Mark as read (Q)"]'))
                    print("Clicking MAR button")
                    mar_bttn.click()
                    print("(!) Selection Marked as READ")
                else:
                    print("Getting Menu button")
                    menu_btn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath('//button[@title="Autres commandes"]'))
                    print("Clicking menu button")
                    menu_btn.click()
                    print("Waiting for MAR button")
                    WebDriverWait(browser, wait_timeout).until(
                        ec.visibility_of_element_located(
                            (By.XPATH, '//button[@aria-label="Marquer comme lu (Q)"]')))
                    print("Getting MAR button")
                    mar_bttn = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//button[@aria-label="Marquer comme lu (Q)"]'))
                    print("Clicking MAR button")
                    mar_bttn.click()
                    print("(!) Selection Marked as READ")
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
                break
        # endregion

        print("(!) Done marking INBOX as read !\n")

    # endregion

    # region Add contact Inbox / click Links / Flag Mail
    if ('AC' in actions) or ('CL' in actions) or ('FM' in actions):

        # region Controllers Settings
        spam_link = str(browser.current_url)[
                    :str(browser.current_url).index('.com')] + '.com/owa/#path=/mail/junkemail'
        inbox_link = spam_link.replace("/junkemail", "/inbox")
        print("[+] Add Contact / Click Links / Flag Mail Actions: ")
        browser.get(spam_link)
        wait_for_page(browser)
        browser.get(inbox_link)
        wait_for_page(browser)

        # region Accessing INBOX Keyword results TODO-CVC What if there is no results ??
        try:
            print("(!) Getting results for Subject: %s" % keyword)
            wait_for_page(browser)
            if email_language == "English":
                print("Waiting for search inbox")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                    (By.XPATH, '//button[@aria-label="Activate Search Textbox"]/span[2]')))
                print("Selecting search inbox")
                search_span = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath(
                        '//button[@aria-label="Activate Search Textbox"]/span[2]'))
                print("Clicking search inbox")
            else:
                print("Waiting for search inbox")
                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                    (By.XPATH, '//button[@aria-label="Activer la zone de recherche"]/span[2]')))
                print("Selecting search inbox")
                search_span = WebDriverWait(browser, wait_timeout).until(
                    lambda driver: browser.find_element_by_xpath(
                        '//button[@aria-label="Activer la zone de recherche"]/span[2]'))
                print("Clicking search inbox")
            search_span.click()

            print("Waiting for input")
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
                                                                                         '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input')))
            print("Selecting input")
            search_input = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath(
                    '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div/form/div/input'))
            print("sending keyword value")
            search_input.send_keys(keyword)
            print("pressing ENTER key")
            search_input.send_keys(Keys.ENTER)
            print("Waiting for results")
            if email_language == "English":
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Exit search"]')))
            else:
                WebDriverWait(browser, wait_timeout).until(
                    ec.visibility_of_element_located((By.XPATH, '//span[@aria-label="Quitter la recherche"]')))
            wait_for_page(browser)
            WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located((By.XPATH,
                                                                                         '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button')))
            more_results = WebDriverWait(browser, wait_timeout).until(
                lambda driver: browser.find_element_by_xpath(
                    '//*[@id="primaryContainer"]/div[4]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[1]/div/div/div[2]/button'))
            more_results.click()
            print("Done")
        except Exception as ex:
            print("/!\ (Error) Getting INBOX results for Subject: %s" % keyword)
            print(type(ex))
        # endregion

        # region Accessing 1st messages
        print("Getting Subject SPAN")
        first_mail = WebDriverWait(browser, wait_timeout).until(
            lambda driver: browser.find_element_by_css_selector('span.lvHighlightSubjectClass'))
        print("Clicking Subject SPAN")
        first_mail.click()
        WebDriverWait(browser, wait_timeout).until(
            ec.visibility_of_element_located((By.CLASS_NAME, '_rp_r1')))
        print("Done!")
        # endregion

        # region Getting loop settings
        print("Getting Newt button")
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
            try:

                # region Flag mail
                if 'FM' in actions:
                    print("[+] [-] Flag mail action:")
                    print("Clicking menu")
                    if email_language == "English":
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//button[@title="More commands"]'))
                        menu_btn.click()
                        print("Clicking Flag mail")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                            (By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                        flag_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//span[@title="Flag for follow-up (Insert)"]'))
                        flag_btn.click()
                        WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                            (By.XPATH, '//span[@title="Flag for follow-up (Insert)"]')))
                    else:
                        menu_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath('//button[@title="Autres commandes"]'))
                        menu_btn.click()
                        print("Clicking Flag mail")
                        WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                            (By.XPATH, '//span[@title="Indicateur de suivi (Inser)"]')))
                        flag_btn = WebDriverWait(browser, wait_timeout).until(
                            lambda driver: browser.find_element_by_xpath(
                                '//span[@title="Indicateur de suivi (Inser)"]'))
                        flag_btn.click()
                        WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                            (By.XPATH, '//span[@title="Indicateur de suivi (Inser)"]')))
                    print("[-] E-mail flagged !")  # TODO-CVC to Count
                    if 'AC' not in actions:
                        time.sleep(1)
                        print("Done")
                # endregion

                # region add contact
                if 'AC' in actions:
                    print("[+] [-] Add Contact action:")
                    print("Getting contact SPAN")
                    contact_span = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_xpath(
                            '//*[@id="ItemHeader.SenderLabel"]/div[2]/div/span/div/span/span'))
                    print("Hover over contact SPAN")
                    hover = ActionChains(browser).move_to_element(contact_span)
                    hover.perform()
                    print("Clicking Contact SPAN")
                    contact_span.click()
                    try:
                        print("Getting add contact buttons")
                        if email_language == "English":
                            add_contact_buttons = WebDriverWait(browser, wait_timeout).until(
                                lambda driver: browser.find_elements_by_xpath(
                                    '//button[@aria-label="Add to contacts"]'))
                        else:
                            add_contact_buttons = WebDriverWait(browser, wait_timeout).until(
                                lambda driver: browser.find_elements_by_xpath(
                                    '//button[@aria-label="Ajouter aux contacts"]'))
                        print("looping through buttons")
                        for add_contact_button in add_contact_buttons:
                            add_contact_button.click()
                            print("Add to contacts button is clicked")
                            print("Waiting for Save contact button")
                            if email_language == "English":
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                                    (By.XPATH, '//button[@title="Save edit contact"]')))
                                print("Getting Save contact button")
                                save_contact_button = WebDriverWait(browser, wait_timeout).until(
                                    lambda driver: browser.find_element_by_xpath(
                                        '//button[@title="Save edit contact"]'))
                                print("Clicking save to contacts")
                                save_contact_button.click()
                                print('waiting for Popup to fade away')
                                WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                                    (By.XPATH, '//button[@title="Save edit contact"]')))
                                print("[-] From-Email added to contacts")  # TODO-CVC to count
                            else:
                                WebDriverWait(browser, wait_timeout).until(ec.visibility_of_element_located(
                                    (By.XPATH, '//button[@title="Enregistrer la modification du contact"]')))
                                print("Getting Save contact button")
                                save_contact_button = WebDriverWait(browser, wait_timeout).until(
                                    lambda driver: browser.find_element_by_xpath(
                                        '//button[@title="Enregistrer la modification du contact"]'))
                                print("Clicking save to contacts")
                                save_contact_button.click()
                                print('waiting for Popup to fade away')
                                WebDriverWait(browser, wait_timeout).until(ec.invisibility_of_element_located(
                                    (By.XPATH, '//button[@title="Enregistrer la modification du contact"]')))
                                print("[-] From-Email added to contacts")  # TODO-CVC to count
                            if 'CL' not in actions:
                                time.sleep(1)
                    except ElementNotVisibleException:
                        print("From-Email already Added !")
                    except TimeoutException:
                        print("From-Email already Added !")
                    except NoSuchElementException:
                        pass
                # endregion

                # region click Link
                if 'CL' in actions:
                    wait_for_page(browser)
                    print("[+] Clicking the Link Action :")
                    print("Getting the Mail 'Body'")
                    body = WebDriverWait(browser, wait_timeout).until(
                        lambda driver: browser.find_element_by_id('Item.MessageUniqueBody'))
                    try:
                        print("Getting the Link in the Mail !")
                        link = body.find_elements_by_tag_name('a')[1]
                    except Exception as ex:
                        print("/!\ (Warning) Link Not Found !")
                        link = None
                        print(type(ex))
                    wait_for_page(browser)
                    if link is not None:
                        try:
                            print("link is Found ==> %s")
                            wait_for_page(browser)
                            print("Clicking the Link")
                            while not link.is_displayed():
                                pass
                            link.click()
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
                            print("[-] Link clicked ! ==> (%s)" % link.get_attribute('href'))
                        except Exception as ex:
                            print("/!\ (Error) Switching to new Tab")
                            print(type(ex))
                # endregion

                # region Checking if it was the last page
                last_page_checked = last_page if last_page else False
                last_page = True if next_btn.get_attribute("aria-disabled") == "true" else False
                print("(!) Getting next Mail ...")
                next_btn.click()
                time.sleep(1)
                # endregion

            except StaleElementReferenceException:
                pass
            except TimeoutException:
                print("/!\ (Error) Add Contact / Click Links / Flag Mail Timed Out")
                # break
            except Exception as ex:
                print("/!\ (Error) Add Contact / Click Links / Flag Mail Error !")
                print(type(ex))
                break
        # endregion

        print("(!) Done Add Contact / Click Links / Flag Mail\n")
        # endregion
    # endregion
    # endregion

    pass
# endregion


@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, **kwargs):
    # region Settings
    actions = str(kwargs.get('actions', None)).split(',')
    keyword = kwargs.get('subject', None)
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
    # browser.set_window_position(-2000, 0)
    global link
    # endregion

    print("\n******\nStarting JOB for :\n*-Actions: %s\n*-Subject: %s\n*-Email: %s\n*-Password: %s\n*-Proxy: %s\n*-"
          "Port: %s\n******\n" % (kwargs.get('actions', None), keyword, mail, pswd, proxy, port))

    try:
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

        if email_language == "old":
            print("(###) Starting actions for OLD e-mail version\n")
            report_old_version(browser, actions)
        else:
            print("(###) Starting actions for NEW e-mail version\n")

            print("[+] Setting mailbox display")
            configure_mailbox(browser)
            print("[+] End setting mailbox display")

            print("[+] Starting Actions")
            report_new_version(browser, actions)
            print("[+] End Actions")
    except Exception as exc:
        # region Exceptions
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# !! OUPS !! #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*")
        print(type(exc))
        self.retry(exc=exc)
        # endregion
    finally:
        # region Finally
        print("###************************************************************************###")
        print('        (!) [-] Finished Actions for %s [-] (!)' % mail)
        print("###************************************************************************###")
        browser.quit()
        # endregion
