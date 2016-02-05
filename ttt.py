import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

while True:
    # region Settings
    PROXY = "67.21.35.254:8674"
    Keyword = 'Funds Request'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    service_args = ['--proxy=%s' % PROXY, '--proxy-type=http']
    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)
    # browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path="chromedriver")
    # browser.maximize_window()

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
        email = 'cap-tst5613@hotmail.com'
        pswd = 'capvalue2015'
        link = 'http://www.hotmail.com'
        browser.get(link)
        if  'ERR_PROXY_CONNECTION_FAILED' in str(browser.page_source):
            print('problem PROXY')
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
            spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
        except Exception:
            spam_count = 0
        print('Total Spam: ' + str(spam_count))

        if spam_count > 0:
            try:
                browser.get(junk_url)
                waiit()
                look_for_pub()
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
            print('Nothing to do here : ')
        # endregion

        # region Inbox Actions
        if not str(browser.current_url).endswith('inbox'): browser.get(inbox_url)
        waiit()
        look_for_pub()
        browser.find_element_by_css_selector('input.c_search_box').send_keys(Keyword)
        browser.find_element_by_css_selector('input.c_search_go').click()
        waiit()
        look_for_pub()
        browser.find_elements_by_tag_name('body')[0].send_keys(Keys.ESCAPE)
        try:
            time.sleep(1)
            emails = browser.find_elements_by_css_selector('li.c-MessageRow')
            waiit()
            look_for_pub()
            emails[0].find_elements_by_tag_name('span')[1].click()
            waiit()
            look_for_pub()
            next_btn = browser.find_element_by_css_selector('a.rmNext').find_element_by_tag_name('img')
            next_btn_attributes = next_btn.get_attribute('class')
            last_msg = True if str(next_btn_attributes).endswith('_d') else False
            waiit()
            look_for_pub()
            try:
                while not last_msg:
                    try:
                        body1 = browser.find_element_by_css_selector('div.readMsgBody')
                        body = body1.find_elements_by_tag_name('div')
                        try:
                            lnk = body[0].find_elements_by_tag_name('p')[0].find_elements_by_tag_name('a')[0]
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
                            print(x)
                            next_btn = None
                        next_btn_attributes = next_btn.get_attribute('class') if next_btn else ''
                        last_msg = True if str(next_btn_attributes).endswith('_d') else False

            except NoSuchElementException as nse:
                print(nse)
                continue
            except StaleElementReferenceException as se:
                print(se)
                continue


        except NoSuchElementException as nse:
            print(nse)
            continue
        except StaleElementReferenceException as se:
            print(se)
            continue
        except Exception as exc:
            print(exc)
            continue
        # endregion

        print('Now What ??')
        waiit()
        look_for_pub()

    except Exception as exc:
        print(exc)
    finally:
        browser.quit()
