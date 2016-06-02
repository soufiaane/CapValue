from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import zipfile
import random
import string
import names
import time

dr1 = webdriver.Firefox()
dr1.get("server1.com")
time.sleep(10)
dr1.get("www.server2.com")
time.sleep(10)
dr1.close()

dr2 = webdriver.Chrome(executable_path='/home/kaoutar/Bureau/chromedriver')
time.sleep(10)
dr2.get("server1.com")
time.sleep(10)
dr2.get("www.server2.com")
dr2.close()


# region Mail Creation
def create_proxyauth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = 'C:\\mailbox\\mailbox_chrome_proxyauth_plugin.zip'

    if proxy_username is None:
        proxy_username = ""

    if proxy_password is None:
        proxy_password = ""

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(host=proxy_host, port=proxy_port, username=proxy_username, password=proxy_password, scheme=scheme, )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path


def wait(active_browser):
    try:
        timeout = time.time() + 30
        while active_browser.execute_script('return document.readyState;') != 'complete':
            if time.time() > timeout:
                break
    except Exception as exxc:
        print(type(exxc))


def generate_credentials():
    l_name = names.get_last_name().replace(" ", "").lower()
    f_name = names.get_first_name().replace(" ", "").lower()
    generated_pswd = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(8, 12)))
    generated_email = "%s.%s_%d@%s" % (
        l_name[:random.randint(1, len(l_name))],
        f_name,
        random.randint(1000, 9999),
        random.choice(["hotmail.com", "outlook.com"])
    )

    return generated_email, generated_pswd


# endregion


def create_mailbox(stgs):
    # region Browser Settings
    proxy_ip, proxy_port, proxy_login, proxy_pswd = stgs.split(";")
    email = ""
    password = ""
    mailbox_created = False
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=proxy_ip, proxy_port=int(proxy_port), proxy_username=proxy_login, proxy_password=proxy_pswd)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_extension(proxyauth_plugin_path)
    browser = webdriver.Chrome(executable_path='C:\\mailbox\\chromedriver.exe', chrome_options=chrome_options)
    # endregion

    try:
        # region Accessing SignUp Page
        browser.get("https://account.microsoft.com/")
        signup_link = browser.find_element_by_id("sign-up-link")
        signup_link.click()
        time.sleep(2)
        wait(browser)
        login_input = browser.find_element_by_id('MemberName')
        pswd_input = browser.find_element_by_id('Password')
        # endregion

        # region Attempting SignUP
        email, password = generate_credentials()

        login_input.send_keys(email)
        pswd_input.click()
        time.sleep(1)
        pswd_input.send_keys(password)
        pswd_input.submit()
        time.sleep(3)
        wait(browser)

        try:
            if browser.find_element_by_id("wlspispHipChallengeContainer").is_displayed():
                browser.quit()
                return False
        except NoSuchElementException:
            pass
        wait(browser)
        # endregion

        # region Asser Account is Created
        created_mailbox = browser.find_element_by_css_selector("div.msame_Header_name")
        if created_mailbox.text == email:
            mailbox_created = True
        # endregion

        # region Accessing MailBox
        browser.get("https://outlook.com")
        wait(browser)

        # region Setting TimeZone & Language
        time_zone_select = WebDriverWait(browser, 30). \
            until(lambda driver: browser.find_element_by_xpath("//select[@id='selTz']/option[@value='UTC']"))
        language_select = WebDriverWait(browser, 30). \
            until(
            lambda driver: browser.find_element_by_xpath("//select[@class='languageInputText']/option[@value='1033']"))
        language_select.click()
        time.sleep(1)
        time_zone_select.click()
        time.sleep(1)
        save_settings_btn = browser.find_element_by_xpath('//div[@onclick="frmSbmt()"]')
        save_settings_btn.click()
        wait(browser)
        # endregion

        # region Escaping PopUp
        next_btn = WebDriverWait(browser, 30).until(lambda driver: browser.find_element_by_css_selector(
            "button.__Microsoft_Owa_ConsumerFirstRun_templates_cs_9"))
        next_btn.click()
        time.sleep(1)
        next_btn.click()
        time.sleep(1)
        next_btn.click()
        time.sleep(10)
        # endregion
        # endregion
    except Exception as exc:
        if not mailbox_created:
            browser.close()
            raise exc
    browser.close()
    return "%s;%s;%s;%s;%s;%s" % (email, password, proxy_ip, proxy_port, proxy_login, proxy_pswd)
