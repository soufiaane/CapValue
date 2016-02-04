from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
while True:
    PROXY = "67.21.35.254:8674"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    service_args = ['--proxy=%s' % PROXY, '--proxy-type=http']

    # browser = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)
    browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    browser.maximize_window()


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


    try:
        email = 'cap-tst5613@hotmail.com'
        pswd = 'capvalue2015'
        link = 'http://www.hotmail.com'
        browser.get(link)
        # browser.get('http://whatismyipaddress.com/')
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
        # Is Verified ?
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

        # Spam Actions
        try:
            browser.get(junk_url)
            waiit()
            look_for_pub()
            spam_count = int(browser.find_elements_by_css_selector('span.count')[2].text)
        except Exception:
            spam_count = 0
        print('Total Spam: ' + str(spam_count))

        if spam_count > 0:
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
            print('Nothing to do here : ')

        # Inbox Actions
        browser.get(inbox_url)
        waiit()
        look_for_pub()
        try:
            inbox_count = int(browser.find_elements_by_css_selector('span.count')[0].text)
            waiit()
            look_for_pub()
            print(inbox_count)
        except:
            inbox_count = 0

        while inbox_count > 0:
            try:
                emails = browser.find_elements_by_css_selector('li.c-MessageRow')
                waiit()
                look_for_pub()
                emails[0].find_elements_by_tag_name('span')[3].click()
                waiit()
                look_for_pub()
            except Exception:
                pass

            try:
                inbox_count = int(browser.find_elements_by_css_selector('span.count')[0].text)
                waiit()
                look_for_pub()
                print(inbox_count)
            except:
                inbox_count = 0

            try:
                waiit()
                look_for_pub()
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
                bb = browser.find_elements_by_tag_name('body')[0]
                bb.send_keys(Keys.CONTROL + ';')
                waiit()
                look_for_pub()
            except Exception as ex:
                print(ex)
                pass
                # Mark Not Spam

        print('Now What ??')
        waiit()
        look_for_pub()
        waiit()
        look_for_pub()
    except Exception as exc:
        print(exc)
    finally:
        browser.quit()
