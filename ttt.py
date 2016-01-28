import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
while True:
    browser = webdriver.Chrome(executable_path="chromedriver")
    browser.maximize_window()

    def look_for_pub():
        try:
            iframe = browser.find_element_by_css_selector('iframe.OutlookAppUpsellFrame')
            script = 'var element1 = document.getElementById("notificationContainer");element1.parentNode.removeChild(element1);\
            var element2 = document.getElementsByClassName("UI_Dialog_BG")[0];element2.parentNode.removeChild(element2);\
            var element3 = document.getElementsByClassName("OutlookAppUpsellFrame")[0];element3.parentNode.removeChild(element3);'
            browser.execute_script(script)
        except Exception :
            print('')

    def waiit():
        while browser.execute_script('return document.readyState;') != 'complete':
            look_for_pub()

    try:
        email = 'MarkSalazar815@hotmail.com'
        pswd = 'aP4FSdmB15'
        link = 'https://www.outlook.com'
        browser.get(link)

        inputs = browser.find_elements_by_tag_name('input')
        login_champ = inputs[0]
        pswd_champ = inputs[1]
        login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

        login_champ.send_keys(email)
        pswd_champ.send_keys(pswd)
        login_btn.click()
        waiit()
        look_for_pub()
        # Goto Junk
        junk_url = str(browser.current_url)[:str(browser.current_url).rindex('/')] + '/?fid=fljunk'
        browser.get(junk_url)
        waiit()
        look_for_pub()
        email_list = browser.find_element_by_css_selector('ul.mailList')
        waiit()
        look_for_pub()
        emails = email_list.find_elements_by_tag_name('li')
        waiit()
        look_for_pub()
        emails[0].click()
        waiit()
        look_for_pub()
        print('Now What ??')
        waiit()
    except Exception as exc:
        print(exc)
    finally:
        browser.quit()
