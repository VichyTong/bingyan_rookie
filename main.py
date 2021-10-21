from selenium import webdriver
from bs4 import BeautifulSoup
import re

browser = webdriver.Chrome()
domain = "https://github.com"
browser.get(domain+"/orgs/apache/repositories")
page_Source = browser.page_source
soup = BeautifulSoup(page_Source, 'lxml')

class Repo:
    name = ""
    description = ""
    license = ""
    language = []
    commit = []
    issue = []

    def __init__ (self, N, D, Li, Lan, C, I):
        name = N
        description = D
        license = Li
        language = Lan
        commit = C
        issue = I

for it in soup.find_all(itemprop="name codeRepository"):
    newbrowser = webdriver.Chrome()
    newdomain = domain + it.attrs['href']
    newbrowser.get(newdomain)
    newpage_Source = newbrowser.page_source
    newsoup = BeautifulSoup(newpage_Source, "lxml")
    D = newsoup.find(class_="f4 mt-3").text
    N = newsoup.find(itemprop="name").contents[1].text
    Li = newsoup.find(attrs={"href" : re.compile('LICENSE$')}).text
    Lan=[]
    for i in newsoup.find_all(class_="color-fg-default text-bold mr-1"):
        Lan.append([i.text, i.find_next_sibling().text])
    
    nextbrowser = webdriver.Chrome()
    nextdomain = newdomain + '/commits'
    nextbrowser.get(nextdomain)
    nextpage_Source = nextbrowser.page_source
    nextsoup = BeautifulSoup(nextpage_Source, "lxml")
    for i in nextsoup.find_all(class_="mb-1"):
        print(i.text)
        for j in i.find_next_sibling().find_all(class_="commit-author user-mention"):
            print(j)
        break
    nextbrowser.close()
    #print (D)
    #print (N)
    #print (Li)
    #print (Lan)
    
    newbrowser.close()
    break
browser.close()