from smtplib import SMTP_SSL
import ssl
import email
import csv
import argparse
import os
from pathlib import Path
import json

template = """
Sehr geehrte Kontaktperson der domain <{domainRecord}>

Ich möchte Sie darüber informieren, dass Ihr Zertifikat für die Domäne <{domainRecord}> vorraussichtlich heute Abend um 20:00 UTC (21:00 MEZ) widerrufen wird.

TODO ADD STUFF HERE

"""

def getDomainInfo(tld):
    tldPath = os.path.join((Path(os.path.realpath(__file__))).parent, "le-scan", "results", "{}.txt".format(tld))
    if (os.path.exists(tldPath)):
        with open(tldPath) as csvFile:
            rd = csv.reader(csvFile, delimiter=",")
            domain = {rows[0]:rows[1] for rows in rd}
        return domain

def getAdminInfo():
    adminInfoPath = os.path.join((Path(os.path.realpath(__file__))).parent, "admininfo.json")
    if (os.path.exists(adminInfoPath)):
        with open(adminInfoPath) as adminInfoFile:
            return json.load(adminInfoFile)

def sendMails(domain, conf):
    with open(os.path.join((Path(os.path.realpath(__file__))).parent, "mail.json")) as mailconfFile:
        mailConf = json.load(mailconfFile)

    context = ssl.create_default_context()
    with SMTP_SSL(host=mailConf.smtpServer, port=mailConf.port, context=context) as server:
        server.user = mailConf.username
        server.password = mailConf.password
        server.auth_login()
    # TODO hier weitermachen


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tld', type=str, help="tld")
    args = parser.parse_args()
    print(args)

    domain = getDomainInfo(args.tld)
    contacts = getAdminInfo()
    print(domain)
    print(contacts)
