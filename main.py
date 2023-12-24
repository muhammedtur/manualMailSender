import os
import time

from dotenv import load_dotenv
from os.path import basename
from utilities.mailSender import sendEmail, sendEmailWithAttachment

load_dotenv()

invoiceFilesPath = os.getenv('INVOICE_FOLDER')
invoiceFiles = os.listdir(invoiceFilesPath)

customers = []
start = "["
end = "]"

files = [f for f in invoiceFiles if os.path.isfile(invoiceFilesPath + '/' + f)]

for file in files:
    if file.endswith('.html'):
        idx1 = file.find(start)
        idx2 = file.find(end)

        emailAddress = file[idx1 + 1: idx2]
        fileName = file[idx2 + 1:]

        if emailAddress:
            emailSent = sendEmailWithAttachment(emailAddress, os.getenv('EMAIL_SUBJECT'), os.getenv('EMAIL_TEXT'), fileName, invoiceFilesPath + file)
        else:
            continue

        if emailSent:
            customers.append([emailAddress, fileName])
            try:
                os.replace(invoiceFilesPath + file, invoiceFilesPath + "sent/" + fileName)
            except:
                os.remove(invoiceFilesPath + file)

        time.sleep(2)
    else:
        continue

if customers:
    sendEmail(os.getenv('EMAIL_PROVIDER_TO'), os.getenv('EMAIL_PROVIDER_SUBJECT'), str(customers))
