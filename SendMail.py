import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from Config import *
 
class SendEmail(object):
    def __init__(self):
        super(SendEmail, self).__init__()
 
        # default value
        self._smtp_host = EMAIL_SENDER_HOST
        self._smtp_port = EMAIL_SENDER_PORT
        self._email_address = EMAIL_ADDRESS
        self._email_password = EMAIL_PASSWORD
 
        self.email_from = None
        self.password = None
        self.email_to = None
        self.email_cc = None
        self.email_bcc = None
        self.email_title = None
        self.email_content = None
        self.attach_path = None
        self.attach_path_list = None
 
    def set_args(self, email_from_in:str=None, password_in:str=None, email_to_in:list=None, email_cc_in:list=None, email_bcc_in:list=None, email_title_in:str=None, email_content_in:str=None, email_attach_path_in:list=None):
        if email_from_in:
            self.email_from = email_from_in
            if not password_in:
                raise Exception('[-] error: Set a password for email!')
            else:
                self.password = password_in
        else:
            self.email_from = self._email_address
            self.password = self._email_password
        self.email_to = ','.join(email_to_in)
        self.email_cc = ','.join(email_cc_in)
        self.email_bcc = ','.join(email_bcc_in)
        self.email_title = email_title_in
        self.email_content = email_content_in
        if email_attach_path_in is not None:
            self.attach_path_list = email_attach_path_in
 
    def send_email(self):
        # init data field
        multi_part = MIMEMultipart()
        multi_part['From'] = self.email_from
        multi_part['To'] = self.email_to
        multi_part['Cc'] = self.email_cc
        multi_part['Bcc'] = self.email_bcc
        multi_part['Subject'] = Header(self.email_title, "utf-8")

        email_body = MIMEText(self.email_content, 'plain', 'utf-8')
        multi_part.attach(email_body)
 
        # attachment file
        for attach_path in self.attach_path_list:
            attach = MIMEText(open(attach_path, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            attach_file_name = str(attach_path.split('/')[-1])
            attach.add_header('Content-Disposition', 'attachment', filename=attach_file_name.encode('UTF-8').decode())
            print('[!] email attach file:' + attach_file_name)
            multi_part.attach(attach)

        # send email
        smtp_server = smtplib.SMTP_SSL(host=self._smtp_host, port=self._smtp_port)
        try:
            smtp_server.login(self.email_from, self.password)
            smtp_server.sendmail(self.email_from, self.email_to, multi_part.as_string())
        except smtplib.SMTPException as e:
            print("[-] " + __name__  + " smtp error: send fail", e)
        else:
            print("[+] " + __name__  + " smtp send success")
        finally:
            try:
                smtp_server.quit()
            except smtplib.SMTPException:
                print("[-] " + __name__  + " smtp quit fail")
            else:
                print("[+] " + __name__  + " smtp quit success")
 