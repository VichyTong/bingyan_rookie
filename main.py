from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
browser.get("https://github.com/orgs/apache/repositories")
page_Source = browser.page_source
soup = BeautifulSoup(page_Source, 'lxml')
cnt = 0
for it in soup.find_all(itemprop="name codeRepository"):
    print(it.string)
    cnt = cnt + 1
print(cnt)
browser.close()