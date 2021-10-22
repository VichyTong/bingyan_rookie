from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json

browser = webdriver.Chrome()
domain = "https://github.com"
browser.get(domain+"/orgs/apache/repositories")
page_Source = browser.page_source
browser.close()
soup = BeautifulSoup(page_Source, 'lxml')

Data = []

def mystr( str ):
    return str.replace('\n', '').replace('\u2026', '')
    
for it in soup.find_all(itemprop="name codeRepository"):
    Dic={}
    newbrowser = webdriver.Chrome()
    newdomain = domain + it.attrs['href']
    newbrowser.get(newdomain)
    newpage_Source = newbrowser.page_source
    newbrowser.close()
    newsoup = BeautifulSoup(newpage_Source, "lxml")
    I = []
    if newsoup.find(id="issues-tab") != None:
        issuebrowser = webdriver.Chrome()
        issuedomain = newdomain + "/issues"
        issuebrowser.get(issuedomain)
        issuepage_Source = issuebrowser.page_source
        issuebrowser.close()
        issuesoup = BeautifulSoup(issuepage_Source, "lxml")
        cnt = 0
        for i in issuesoup.find_all(attrs={"data-hovercard-type" : "issue"}):
            browser4 = webdriver.Chrome()
            domain4 = domain + i.attrs['href']
            browser4.get(domain4)
            page_Source4 = browser4.page_source
            browser4.close()
            soup4 = BeautifulSoup(page_Source4, "lxml")
            I.append({'Title' : mystr(soup4.find(class_="js-issue-title markdown-title").text)})
            I[cnt]['Detail'] = mystr(soup4.find(name = 'td').p.text)
            cnt = cnt + 1
            if cnt==5 :
                break
    Dic["Name"] = mystr(newsoup.find(itemprop="name").contents[1].text)
    Dic["Description"] = mystr(newsoup.find(class_="f4 mt-3").text)
    Dic["License"] = ""
    if newsoup.find(attrs={"href" : re.compile('LICENSE$')}) != None:
        Dic["License"] =mystr(newsoup.find(attrs={"href" : re.compile('LICENSE$')}).text)
    Lan={}
    for i in newsoup.find_all(class_="color-fg-default text-bold mr-1"):
        Lan[mystr(i.text)] = mystr(i.find_next_sibling().text)
    Dic["Language"] = Lan
    nextbrowser = webdriver.Chrome()
    nextdomain = newdomain + '/commits'
    nextbrowser.get(nextdomain)
    nextpage_Source = nextbrowser.page_source
    nextbrowser.close()
    nextsoup = BeautifulSoup(nextpage_Source, "lxml")
    C = []
    cnt = 0
    for i in nextsoup.find_all(class_="mb-1"):
        C.append({"commit message" : mystr(i.text)})
        cnt = cnt + 1
        if cnt == 5 :
            break
    cnt = 0
    for i in nextsoup.find_all(class_="f6 color-text-secondary min-width-0"):
        for j in i.find_all(attrs={'href' : re.compile('/apache')}):
            C[cnt]["author"] = mystr(j.text)
        cnt = cnt + 1
        if cnt == 5 :
            break
    cnt = 0
    for i in nextsoup.find_all(class_="text-mono f6 btn btn-outline BtnGroup-item"):
        C[cnt]["hash"] = mystr(i.text)
        cnt = cnt + 1
        if cnt == 5 :
            break
    Dic["Commit"] = C
    Dic["Issue"] = I
    Data.append(Dic)

Output = json.dumps(Data, indent=1)
fo = open('output.json', 'w')
fo.write(Output)
