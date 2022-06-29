import os.path
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# noinspection PyBroadException
def send(log_filename, todays_date, path):
    # todays_date = datetime.datetime.now().strftime("%d-%m-%y")
    # 'news.recommendation.kritgyan@gmail.com' #'traveller.tale@gmail.com' # Your email
    email = 'news.recommendation.kritgyan@gmail.com'
    password = 'Kritgyan@Jaipu'  # 'Kritgyan@Jaipur' # Your email account password
    send_to_email = ['news.recommendation.kritgyan@gmail.com']  # ,'ankindian007@gmail.com'] # Who you are sending the message  to
    subject = 'Scraped News logs for today'
    message = 'Hello sir,<br>I am sending this through my dummy email. Now it is running completely fine, now i wil look into some error while extracting articles out of 815 it is fetching 513 something, i will look into the other why it is not working. This is an automated mail.<br>To unsubscribe please send an email to the sender.<br>PFA the logs for '+ todays_date +'.<br>Thanks.'
    # file_location = log_filename

    loop_count = 0
    while loop_count < 3:
        try:
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = ','.join(send_to_email)
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))
            # Set up the attachment
            filename = os.path.basename(path + "logs/" + log_filename)
            attachment = open(path + "logs/" + log_filename + '.txt', "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # Attach the attachment to the MIMEMultipart object
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()
            print("mail sent")
            break
        except:
            print("mail not sent")
            loop_count += 1
