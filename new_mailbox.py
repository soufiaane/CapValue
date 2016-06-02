from __future__ import print_function, absolute_import
from queue import Queue
from mailbox import create_mailbox
from threading import Thread, Lock
from random import shuffle
import requests
import imaplib
import string
import math
import time

mailbox_queue = Queue()
proxy_queue = Queue()
valid_proxy_list = []
lock = Lock()
mailboxes_to_create = 0
number_lines = 0
number_valid = 0
loop_number = 0
navs_to_open = 0
check_imap = False


# region Proxy Verification

def check_proxy(proxy_to_check, timeout=20, url="http://example.com", title="<title>Example Domain</title>"):
    proxies = {"http": "http://" + proxy_to_check, "https": "https://" + proxy_to_check}
    try:
        r = requests.get(url, proxies=proxies, timeout=timeout)
    except Exception as e:
        return e is False
    return title in r.text


def print_proxy(status, proxy_to_print, port_to_print, login_to_print, pswd_to_print):
    global number_valid
    global valid_proxy_list
    if status:
        valid_proxy_list.append("%s;%s;%s;%s" % (proxy_to_print, port_to_print, login_to_print, pswd_to_print))
        number_valid += 1


def check_proxy_list():
    while True:
        st = proxy_queue.get()
        settings = st.split(";")
        log, pswd, prox, port, status = None, None, None, None, None

        if len(settings) is 2:
            prox, port = st.split(";")
            status = check_proxy("%s:%s" % (prox, port))
        elif len(settings) is 4:
            prox, port, log, pswd = st.split(";")
            status = check_proxy("%s:%s@%s:%s" % (log, pswd, prox, port))

        print_proxy(status, prox, port, log, pswd)

        proxy_queue.task_done()


# endregion

# region MailBox Creation
def print_mailbox(mailbox):
    if mailbox:
        user, psswd, ip, port, ip_user, ip_psswd = mailbox.split(";")
        if check_imap:
            m = imaplib.IMAP4_SSL('imap-mail.outlook.com', port=993)
            try:
                m.login(user, psswd)
                with open("C:\\mailbox\\mailboxes.txt", "a") as file:
                    file.write("%s;%s;%s;%s;%s;%s\n" % (user, psswd, ip, port, ip_user, ip_psswd))
            except imaplib.IMAP4.error:
                pass
        else:
            with open("C:\\mailbox\\mailboxes.txt", "a") as file:
                file.write("%s;%s;%s;%s;%s;%s\n" % (user, psswd, ip, port, ip_user, ip_psswd))


def create_mailbox_list():
    while True:
        prox = mailbox_queue.get()
        try:
            email = create_mailbox(prox)
            lock.acquire()
            print_mailbox(email)
            lock.release()
        except:
            pass
        mailbox_queue.task_done()
# endregion

if __name__ == "__main__":
    try:
        # region Proxy Threads
        for i in range(500):
            t = Thread(target=check_proxy_list)
            t.daemon = True
            t.start()
        # endregion

        # region Check Proxies
        print('*' * 40)
        print("Proxies check started at: %s" % time.strftime("%H:%M:%S"))
        for line in open('C:\\mailbox\\proxies.txt'):
            number_lines += 1
            proxy_queue.put(str(line.replace("\n", "")))
        proxy_queue.join()
        shuffle(valid_proxy_list)
        print("[!] {} Proxies are checked.".format(number_lines))
        print("[!] {} Valid proxies are found.".format(number_valid))
        print("Proxies check ended at: %s" % time.strftime("%H:%M:%S"))
        print('*' * 40)
        # endregion

        start_job = False
        while not start_job:
            # region User Settings
            print("")
            print('*' * 40)
            mailboxes_to_create = int(input("[?] Number of MailBoxes to create ? (1000) ") or 1000)
            navs_to_open = int(input("[?] Number of browsers to open ? (1) ") or 1)
            check_imap = str(input("[?] Check IMAP access after mailbox Creation ? (y/N) ") or "N")
            check_imap = True if check_imap.lower() in ["y", "yes", "o", "oui"] else False
            # endregion

            # region Confirm Settings
            loop_number = int(math.ceil(mailboxes_to_create / len(valid_proxy_list)))

            print("")
            print('*' * 40)
            print("[-] Creating %d MailBoxes" % mailboxes_to_create)
            print("[-] Looping %d times over %d proxies" % (loop_number, len(valid_proxy_list)))
            print("[-] Using %d Simultaneous browsers for creation" % navs_to_open)
            print("[-] Chacking IMAP access after creation: %s" % str(check_imap))
            print('*' * 40)

            confirm_settings = str(input("[?] Continue with these settings ? (Y/n) ") or "Y")
            start_job = True if confirm_settings.lower() in ["y", "yes", "o", "oui"] else False
            # endregion

        # region Browser Threads
        for i in range(navs_to_open):
            t = Thread(target=create_mailbox_list)
            t.daemon = True
            t.start()
        # endregion

        for _ in range(loop_number):
            if mailbox_queue.qsize() >= mailboxes_to_create:
                break
            for suggested_proxy in valid_proxy_list:
                mailbox_queue.put(suggested_proxy)
                if mailbox_queue.qsize() >= mailboxes_to_create:
                    break
        mailbox_queue.join()
    except Exception as ex:
        print(type(ex))
