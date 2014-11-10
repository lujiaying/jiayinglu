# -*- coding: utf-8 -*-

'''mailsend.py

邮件发送模块
'''

__author__ = "jiaying.lu"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2014/3/19 12:15:19 $"
__copyright__ = "Copyright (c) 2014 lujiaying"
__license__ = "Python"

import smtplib, os
import email.mime.text
import email.mime.multipart
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class MailSender:

    def __init__(self):
        self.__mail_server = 'smtp.exmail.qq.com'
        self.__mail_user = 'report@xxx.com'
        self.__mail_password = 'xxxx'
        self.__mail_from = 'report@xxx.com'
        #TODO: add a correct email account



    def send(self, to_addrs, subject, html_txt):
         # 设定root信息
        msg_root = email.mime.multipart.MIMEMultipart('related')
        msg_root['Subject'] = isinstance(subject, str) and subject.decode('utf-8') or subject
        msg_root['From'] = self.__mail_from
        msg_root['To'] = ', '.join(to_addrs)
        msg_root.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # ‘alternative’ part, so message agents can decide which they want to display.
        msg_alt = email.mime.multipart.MIMEMultipart('alternative')
        msg_txt = email.mime.text.MIMEText(html_txt, 'html', 'utf-8')
        msg_alt.attach(msg_txt)
        msg_root.attach(msg_alt)

        #发送邮件
        smtp = smtplib.SMTP()
        #设定调试级别，依情况而定
        smtp.set_debuglevel(1)
        smtp.connect(self.__mail_server)
        smtp.login(self.__mail_user, self.__mail_password)
        smtp.sendmail(self.__mail_from, to_addrs, msg_root.as_string())
        smtp.quit()


def send_mail (addrs, subject, msg ) :
	if len ( subject ) <= 0 :
		subject = "无主题"
	ms =MailSender ()
	ms.send ( addrs, subject, msg )


#jiaying.lu add
def send_att_mail(send_to, subject, text, files=[]):
    '''发送带附件的邮件

    Args:
        send_to: 收件人列表
        subject: 主题
        text: 正文
        files: 附件
    '''

    assert isinstance(send_to, list)
    assert isinstance(files, list)
    if len ( subject ) <= 0 :
            subject = "无主题"

    # 设定发送server
    mail_server = 'smtp.exmail.qq.com'
    mail_user = 'report@xxx.com'
    mail_password = 'dataxxx'
    send_from = 'report@xxx.com'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(mail_server)
    smtp.login(mail_user, mail_password)

    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == '__main__' :
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    #print BASE_DIR

    to_addrs = ['jiaying.lu@lejent.com']
    subject = 'csv发送测试'
    text = '正文文本'
    #files = ['/data/home/lujiaying/r_back/log/out.csv']
    file_path = os.path.join(BASE_DIR, 'log/out.csv')
    #print file_path
    files = [file_path]

    send_att_mail(to_addrs, subject, text, files)
