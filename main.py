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
    newbrowser.get(domain + it.attrs['href'])
    newpage_Source = newbrowser.page_source
    newsoup = BeautifulSoup(newpage_Source, "lxml")
    D = newsoup.find(class_="f4 mt-3").string
    N = newsoup.find(itemprop="name").children.string
    Li = newsoup.find(attrs={"href" : re.compile(r'$LICENSE')})
    print (D)
    print (N)
    print (Li)
    newbrowser.close()
    break
browser.close
()