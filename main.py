from smtplib import SMTP
import email
import csv
import argparse
import os
from pathlib import Path
import json

def getDomainInfo(tld):
    global domain
    tldPath = os.path.join((Path(os.path.realpath(__file__))).parent, "le-scan", "results", "{}.txt".format(tld))
    if (os.path.exists(tldPath)):
        with open(tldPath) as csvFile:
            rd = csv.reader(csvFile, delimiter=",")
            domain = {rows[0]:rows[1] for rows in rd}
        return domain

def getAdmin(domain):
    pass

def sendMails(domain, conf):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tld', type=str, help="tld")
    parser.add_argument('--mailconf', type=str, help="path to mailconfig")
    parser.add_argument('--domaininfo', type=str, help="path to domaininfo")
    args = parser.parse_args()
    print(args)

    domain = getDomainInfo(args.tld)
    print(domain)
