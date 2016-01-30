from __future__ import absolute_import
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from smtplib import
import smtplib

html = """\
<img src="http://acre.nationalauthority.net/CH.tg?IlgyqriWpseja=IWcQgJKJyiuVy03ahcrb0131yt01c1el020fg050ik64i403wd" width="1" height="1">
<P style="text-align: center;">
<a href="http://acre.nationalauthority.net/CH.tg?gLFtiBZDFARaZ=ANaxPqlbjJbbV13ahcrb0131yt01c1el020fg050ik64i403wd">
<center>
<FONT face="Consolas" color=#549192 size=7 >
 Hi, <br></FONT>
<FONT size=5 face="Cooper Black" color="#A33D31">We like to say YES!  Apply for a Fingerhut Credit Account and Shop Today
</FONT>
</center>
</a>
</p>
<br />
<center>
<a href="http://acre.nationalauthority.net/CH.tg?gLFtiBZDFARaZ=ANaxPqlbjJbbV13ahcrb0131yt01c1el020fg050ik64i403wd">
<img src="http://i.imgur.com/w3pRtQF.jpg">
</a>
</CENTER>
<br />
<CENTER>
<a href="http://acre.nationalauthority.net/CH.tg?gLFtiBZDFARaZ=ANaxPqlbjJbbV13ahcrb0131yt01c1el020fg050ik64i403wd">
<img src="http://i.imgur.com/M8ja4oy.jpg">
</a>
</CENTER>
<br />
<CENTER>
<a href="http://acre.nationalauthority.net/CH.tg?gLFtiBZDFARaZ=ANaxPqlbjJbbV13ahcrb0131yt01c1el020fg050ik64i403wd">
<img src="http://i.imgur.com/DgPZhLX.png">
</a>
</CENTER>
<br>
"""

lines = [line.rstrip('\n') for line in open('facebook_results_newlist.txt')]
x = 0
for line in lines:
    # while x < 20:
    try:
        (email, password, to, subj, msg) = (
            'b007.mgh@gmail.com',
            'fousiane0',
            'mgh.soufiane@gmail.com, naoufal.adnani@gmail.com, stayconnected41@yahoo.com',
            'SubjAutoHotm',
            'Message Texte2'
        )  # [to, 'naoufal.adnani@gmail.com', 'stayconnected41@yahoo.com']
        msgs = MIMEMultipart()
        msgs['From'] = '🎸<-----Apply-Today,-Buy-Today-at-Fingerhut----->🎮' + '<' + email + '>'
        msgs['To'] = line + '@facebook.com'
        msgs['Subject'] = subj
        part1 = MIMEText(msg, 'plain')
        part2 = MIMEText(html, 'html')
        # msgs.attach(part1)
        msgs.attach(part2)
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.set_debuglevel(1)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, password)
        mailserver.sendmail(email, line + '@facebook.com', msgs.as_string())
        mailserver.quit()
    except smtplib.SMTPSenderRefused as smtpError:
        print('# - Error ' + str(smtpError.smtp_code) + ': ' + str(smtpError.smtp_error))
    except Exception as e:
        print(e)
    finally:
        x += 1
