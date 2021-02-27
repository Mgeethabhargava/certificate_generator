import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def SendMail(ImgFileName,email,fullname):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Bonafide Certificate is Generated Successfully'
    msg['From'] = 'scientistforresearch@gmail.com'
    msg['To'] = email

    text = MIMEText("Dear "+fullname+" ,"+"\n\nYour Bonafide Certificate is Generated Successfully and Ready for Print")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('scientistforresearch@gmail.com', 'Bgm@6018')
    s.sendmail('scientistforresearch@gmail.com', email, msg.as_string())
    s.quit()