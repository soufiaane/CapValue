from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.PhantomJS(executable_path="phantomjs.exe")
browser = webdriver.Chrome(executable_path="chromedriver")
browser.maximize_window()


def waiit():
    while browser.execute_script('return document.readyState;') != 'complete':
        pass
    return

try:
    email = 'MarkSalazar815@hotmail.com'
    pswd = 'aP4FSdmB15'
    link = 'https://www.outlook.com'
    browser.get(link)
    wait = WebDriverWait(browser, 60)

    inputs = browser.find_elements_by_tag_name('input')
    login_champ = inputs[0]
    pswd_champ = inputs[1]
    login_btn = browser.find_element_by_xpath('//*[@value="Se connecter"]')

    login_champ.send_keys(email)
    pswd_champ.send_keys(pswd)
    login_btn.click()
    waiit()
    # Goto Junk
    junk_url = str(browser.current_url)[:str(browser.current_url).rindex('/')] + '/?fid=fljunk'
    browser.get(junk_url)
    email_list = browser.find_element_by_css_selector('ul.mailList')
    emails = email_list.find_elements_by_tag_name('li')
    emails[0].click()
    print('Now What ??')



except Exception as exc:
    print(exc)
finally:
    browser.quit()
