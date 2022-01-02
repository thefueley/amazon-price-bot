import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class PriceAlert:
    def __init__(self, item, price, link):
        self.item = item
        self.price = price
        self.link = link

    def send_alert(self):

        smpt_host = os.environ['SMTP_HOST']
        sender = os.environ['SMTP_ACCOUNT']
        sender_pass = os.environ['SMTP_PASSWORD']
        recipient = os.environ['SMTP_RECEIVER']
        subject = f"Price Drop on {self.item}!"

        msg = MIMEMultipart('alternative')

        msg['From'] = sender
        msg['To'] = recipient
        msg['subject'] = subject

        text = f"The {self.item} you're watching has dropped to ${self.price}!\nlink: {self.link}"
        html = f"""\
        <html>
        <head></head>
        <body>
            <p>The {self.item} you're watching has dropped to ${self.price}!<p>
            <p>Buy it now? <a href="{self.link}">link</a></p>
        </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            # I have non-ascii in my hostname. `local_hostname` required for me.
            mailserver = smtplib.SMTP(smpt_host, 587, local_hostname='woof@local')
            # mailserver.set_debuglevel(True)
            mailserver.starttls()
            mailserver.login(sender, sender_pass)
            mailserver.send_message(msg)

            # Was receiving this exception prior to setting `local_hostname` above
        except UnicodeEncodeError:
            print("UnicodeEncodeError\n")
            print(msg)
        else:
            print("Message sent.")
        finally:
            mailserver.quit()
