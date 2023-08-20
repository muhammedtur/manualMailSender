import os

from dotenv import load_dotenv
from os.path import basename
from utilities.mailSender import sendEmail, sendEmailWithAttachment

load_dotenv()

zipFilesPath = os.getenv('ZIP_FOLDER')
zipFiles = os.listdir(zipFilesPath)

customers = []
start = "["
end = "]"

files = [f for f in zipFiles if os.path.isfile(zipFilesPath + '/' + f)]

for file in files:
    idx1 = file.index(start)
    idx2 = file.index(end)

    emailAddress = file[idx1 + 1: idx2]
    fileName = file[idx2 + 1:]

    if emailAddress:
        emailSent = sendEmailWithAttachment(emailAddress, os.getenv('EMAIL_SUBJECT'), os.getenv('EMAIL_TEXT'), fileName, zipFilesPath + file)
    else:
        continue

    if emailSent:
        customers.append([emailAddress, fileName])
        try:
            os.replace(zipFilesPath + file, zipFilesPath + "sent/" + fileName)
        except:
            os.remove(zipFilesPath + file)

if customers:
    sendEmail(os.getenv('EMAIL_PROVIDER_TO'), os.getenv('EMAIL_PROVIDER_SUBJECT'), str(customers))
