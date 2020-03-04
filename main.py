from smtplib import SMTP_SSL
import ssl
import email
import csv
import argparse
import os
from pathlib import Path
import json

template = """
Sehr geehrte Kontaktperson der Webseite <{domainRecord}>

Ich möchte Sie darüber informieren, dass Ihr Zertifikat für die Webseite <{domainRecord}> vorraussichtlich heute Abend um 20:00 UTC (21:00 MEZ) widerrufen wird.

Hintergrund ist ein Fehler seitens Let's Encrypt.
Heise schreibt darüber: https://www.heise.de/security/meldung/Achtung-Let-s-Encrypt-macht-heute-nacht-3-Millionen-Zertifikate-ungueltig-4676017.html

Sie sind bei einer automatischen Überprüfung aufgefallen.

Betroffen ist folgendes Zertifikat:

Webseite: {domainRecord}
Seriennummer: {sn}

Sie können selbst Überprüfen, ob Ihre Website betroffen ist:
https://checkhost.unboundtest.com/

Mit freundlichen Grüßen

{sender}
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
            return dict(json.load(adminInfoFile))

def sendMails(domainInfo, contacts, domain=""):
    with open(os.path.join((Path(os.path.realpath(__file__))).parent, "mail.json")) as mailconfFile:
        mailConf = json.load(mailconfFile)

    context = ssl.create_default_context()
    with SMTP_SSL(host=mailConf["smtpServer"], port=mailConf["port"], context=context) as server:
        server.user = mailConf.username
        server.password = mailConf.password
        server.auth_login()
        if (len(domain) == 0):
            for domain, contactAddress in contacts:
                server.send_message(
                    msg=template.format(
                        domainRecord=domain,
                        sn=domainInfo[domain],
                        sender=mailConf["sender"]
                    ),
                    to_addrs=contactAddress,
                    from_addr=mailConf["senderMail"]
                )
        else:
            server.send_message(
                msg=template.format(
                    domainRecord=domain,
                    sn=domainInfo[domain],
                    sender=mailConf["sender"]
                ),
                to_addrs=contacts[domain],
                from_addr=mailConf["senderMail"]
            )



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tld', type=str, help="tld")
    args = parser.parse_args()

    domain = getDomainInfo(args.tld)
    contacts = getAdminInfo()
    sendMails(domain, contacts)
