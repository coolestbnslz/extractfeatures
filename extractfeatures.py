from flask import Flask,render_template,request
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime
my_date = datetime.now()
fromaddr = 'bansalz1208@gmail.com'
toaddr = ""

app=Flask(__name__)
app.config["IMAGE_UPLOADS"] = "C:/Users/Nikhil Bansal/PycharmProjects/course/uploads"
@app.route("/")
def index():
    return render_template("email.html")

@app.route("/",methods=['GET','POST'])
def my_link():
    file=''
    fromaddr = 'bansalz1208@gmail.com'
    if request.method == "POST":
        if request.files:
            file = request.files["filename"]
            file.save(os.path.join(app.config["IMAGE_UPLOADS"], file.filename))
            print(file)
    user = request.form['email']
    toaddr=user
    print(user)
    print('clicked')
    columns_name = ['SN', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'Class']
    result = []
    log = []
    a=[f'C:/Users/Nikhil Bansal/PycharmProjects/course/uploads/{file.filename}']
    dict = {'+': 1, '-': 0}
    for i in a:
        df1 = pd.read_csv(i)
        count = 1
        for j in df1.values.tolist():
            if (j[0].isalpha()):
                try:
                    result.append(
                        [count, j[0].count('N'), j[0].count('H'), j[0].count('Q'), j[0].count('G'), j[0].count('D'),
                         j[0].count('T'), dict[j[1]]])
                except:
                    log.append([i, j[0], ''])
            else:
                log.append([i, j[0], j[1]])
            count += 1
    flnm = str(datetime.now().strftime('%Y%m%d'))
    result1 = pd.DataFrame(result, columns=columns_name)
    result1.to_csv('result' + flnm + '.csv', index=False)
    log1 = pd.DataFrame(log, columns=['Filename', 'Sequence','class'])
    log1.to_csv('log' + flnm + '.csv', index=False)
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Result File"

    # string to store the body of the mail
    body = "File"

    # open the file to be sent
    filename = "Result.csv"
    attachment = open(f"C:/Users/Nikhil Bansal/PycharmProjects/course/result{flnm}.csv", "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    filename = "Log.csv"
    attachment = open(f"C:/Users/Nikhil Bansal/PycharmProjects/course/log{flnm}.csv", "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "nb9501059082")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    return 'Clicked. Please check your mail'

if __name__=='__main__':
    app.run( port=5000)
