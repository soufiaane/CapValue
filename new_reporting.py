from reporting import report_hotmail
from threading import Thread
from queue import Queue
import time

actions_hide_browsers = False
mailbox_queue = Queue()
actions_time_out = 15
actions_subject = "a"
mailboxes = []
actions = ""


def report_mailbox_list():
    while True:
        mailbox_settings = mailbox_queue.get()
        settings = mailbox_settings.split(";")
        email, pswd, proxy_ip, proxy_port, proxy_user, proxy_pswd = None, None, None, None, None, None

        if len(settings) is 2:
            email, pswd = mailbox_settings.split(";")
        elif len(settings) is 4:
            email, pswd, proxy_ip, proxy_port = mailbox_settings.split(";")
        elif len(settings) is 6:
            email, pswd, proxy_ip, proxy_port, proxy_user, proxy_pswd = mailbox_settings.split(";")
        try:
            report_hotmail(actions=actions, subject=actions_subject, wait_timeout=actions_time_out,
                           email={'login': email, 'password': pswd},
                           proxy={'ip_address': proxy_ip, 'ip_port': proxy_port, 'proxy_user': proxy_user,
                                  'proxy_pswd': proxy_pswd})
        except Exception as exc:
            print(type(exc))
        mailbox_queue.task_done()


if __name__ == "__main__":
    try:
        # region Read Emails
        print('*' * 40)
        print("Getting Emails started at: %s" % time.strftime("%H:%M:%S"))
        for line in open('C:\\reporting\\mailboxes.txt'):
            if line not in ["\n", ""]:
                mailboxes.append(line.replace("\n", ""))
        print("[!] {} Emails are loaded.".format(len(mailboxes)))
        print("Proxies check ended at: %s" % time.strftime("%H:%M:%S"))
        print('*' * 40)
        # endregion

        # region User Settings
        print("")
        print('*' * 40)
        actions_subject = input("[?] Enter Subject : ")
        navs_to_open = int(input("[?] Number of browsers to open ? (1) ") or 1)
        actions_time_out = int(input("[?] Time Out (s) ? (15 s) ") or 15)

        actions_rs = str(input("[?] Mark spam as read ? (y/N) ") or "N")
        actions_ns = str(input("[?] Mark as not spam ? (y/N) ") or "N")
        actions_ri = str(input("[?] Mark inbox as read ? (y/N) ") or "N")
        actions_oi = str(input("[?] Mark inbox as open ? (y/N) ") or "N")
        actions_ss = str(input("[?] Mark spam as safe ? (y/N) ") or "N")
        actions_ac = str(input("[?] Add sender to contacts ? (y/N) ") or "N")
        actions_cl = str(input("[?] Click link in email ? (y/N) ") or "N")
        actions_fm = str(input("[?] Flag email  ? (y/N) ") or "N")
        # endregion

        # region Format Settings
        if actions_rs.lower() in ["y", "yes", "o", "oui"]:
            actions += "RS,"
        if actions_ns.lower() in ["y", "yes", "o", "oui"]:
            actions += "NS,"
        if actions_ri.lower() in ["y", "yes", "o", "oui"]:
            actions += "RI,"
        if actions_oi.lower() in ["y", "yes", "o", "oui"]:
            actions += "OI,"
        if actions_ss.lower() in ["y", "yes", "o", "oui"]:
            actions += "SS,"
        if actions_ac.lower() in ["y", "yes", "o", "oui"]:
            actions += "AC,"
        if actions_cl.lower() in ["y", "yes", "o", "oui"]:
            actions += "CL,"
        if actions_fm.lower() in ["y", "yes", "o", "oui"]:
            actions += "FM,"
        # endregion

        # region Browser Threads
        for i in range(navs_to_open):
            t = Thread(target=report_mailbox_list)
            t.daemon = True
            t.start()
        # endregion

        for mailbox in mailboxes:
            mailbox_queue.put(mailbox)
        mailbox_queue.join()
    except Exception as ex:
        print(type(ex))
