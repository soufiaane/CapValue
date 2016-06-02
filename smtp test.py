import sys
import email.header
import datetime
import imaplib
import getpass
import email
import re

EMAIL_ACCOUNT = "smghanen@outlook.com"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "inbox"


def get_email(line):
    match = re.search(r'[\w\.-]+@[\w\.-]+', line)
    return match.group(0)


def get_ips(line):
    pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
    ips = [each[0] for each in re.findall(pattern, line)]
    for item in ips:
        location = ips.index(item)
        ip = re.sub("[ ()\[\]]", "", item)
        ip = re.sub("dot", ".", ip)
        ips.remove(item)
        ips.insert(location, ip)
    if '127.0.0.1' in ips:
        ips.remove('127.0.0.1')
    if len(ips) == 1:
        return ips[0]
    else:
        return ips


def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        fromEmail = get_email(str(email.header.make_header(email.header.decode_header(msg['From']))))
        senderIP = get_ips(str(email.header.make_header(email.header.decode_header(msg['Received']))))
        print('Message %d: from \'%s\' By \'%s\' ' % (int(num), fromEmail, senderIP))
        print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            print("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            print("*" * 50 + '\n')


M = imaplib.IMAP4_SSL('imap-mail.outlook.com', port=993)

try:
    rv, data = M.login('smghanen@outlook.com', 'Fousiane0')
    # rv, data = M.login('louise.oliver2016@gmail.com', 'menana4ever')
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")
    sys.exit(1)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()
