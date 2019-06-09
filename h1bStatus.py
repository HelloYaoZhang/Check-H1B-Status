import requests, subprocess, sys
from bs4 import BeautifulSoup

caseNumber = ''

if len(sys.argv) < 2:
    caseNumber = input("please provide your h1b case number: ")
else:
    caseNumber = sys.argv[1]

url = "https://egov.uscis.gov/casestatus/mycasestatus.do"

querystring = {"changeLocale": "",
               "completedActionsCurrentPage": "0",
               "upcomingActionsCurrentPage": "0",
               "appReceiptNum": caseNumber,
               "caseStatusSearchBtn": "CHECK+STATUS"
               }

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "text/html,application/xhtml+xml,"
              "application/xml;q=0.9,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh,en;q=0.9,zh-CN;q=0.8",
    'Host': "egov.uscis.gov"
    }

response = requests.request("POST", url, headers=headers, params=querystring)

parsed_html = BeautifulSoup(response.text, features="html.parser")

h1bStatus = parsed_html.body.find('div', attrs={'class':'current-status-sec'}).text.replace('\t', '').replace('+\n', '').replace("  ", "")

exec = """osascript -e 'display notification "{}" with title "H1B Status"'""".format(h1bStatus)

subprocess.call(exec, shell=True)
