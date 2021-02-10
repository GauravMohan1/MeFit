#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:18:27 2020

@author: varunmeduri
"""
# Python code to illustrate Sending mail with attachments 
# from your Gmail account  
  
# libraries to be imported 
import os
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
fromaddr = "gauravmohan00@gmail.com"
toaddr = "support@mefitvending.com"
   
# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address
msg['To'] = toaddr 
  
# storing the subject  
msg['Subject'] = "Daily MeFit Reports"
  
# string to store the body of the mail 
body = "Body_of_the_mail"
  
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

report_names = ["Graphs","analysis_reports", "error_reports", "cost-analysisdaily_report", "cost-analysisweekly_report", "cost-analysisbiweekly_report", 'routetotal', 'pubd_report', 'pubw_report', 'pubi_report']
  
# open the file to be sent
rootdir = os.getcwd()
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        name = file.split(".")[0]
        if file.endswith((".txt") or file.endswith(".zip")) and name in report_names:
            filename = file 
            print(file)
            p = MIMEBase('application', '.txt')
            attachment = open(filepath, "rb")
            p.set_payload(attachment.read())


# To change the payload into encoded form  
  
# encode into base64 
            encoders.encode_base64(p) 
   
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
            msg.attach(p)



s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()

# Authentication
s.login(fromaddr, "Gaurav2468")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()
'''
        filename = file.split(".txt")[0]
        print(filename)
        for i in range(10):
            if filename == "report" + str(i):
                filepath = "/Users/varunmeduri/Desktop/MeFit/" + str(filename) + ".txt"
                attachment = open(filepath, "rb")
                print("Yes")
    

#filename = "report3.txt"
#attachment = open("/Users/varunmeduri/Desktop/MeFit/report3", "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'zip')
  
# To change the payload into encoded form 
p.set_payload(attachment.read())
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  
# creates SMTP session 

  
# start TLS for security 
'''