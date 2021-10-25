import requests
from lxml import etree
import os
import json

os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

def mystr(str):
    return str.replace('\n', '').replace('\u2026', '').strip()

r = requests.get('https://github.com/orgs/apache/repositories', timeout=10)
html = etree.HTML(r.text)


domain_list = html.xpath('//a[@itemprop="name codeRepository"]/@href')

Data = []

for it in domain_list:
    Dic = {}
    r_it = requests.get('https://github.com' + it, timeout=10)
    html_it = etree.HTML(r_it.text)
    I = []
    issue_domain = html_it.xpath('//a[1][@id="issues-tab"]/@href')
    if(issue_domain != []):
        r_issue = requests.get('https://github.com' + issue_domain[0], timeout=10)
        html_issue = etree.HTML(r_issue.text)
        cnt = 0
        for i in html_issue.xpath('//a[@data-hovercard-type = "issue"]/@href'):
            r_new = requests.get('https://github.com' + i)
            html_new = etree.HTML(r_new.text)
            I.append({'Title' : mystr(html_new.xpath('//span[@class="js-issue-title markdown-title"]/text()')[0])})
            #print("LOOOOOOOK",html_new.xpath('//td[1]/p/text()'))
            #print(cnt)
            I[cnt]['Detail'] = ''.join(mystr(html_new.xpath('//td[1]/p/text()')[0]))
            cnt = cnt + 1
            if cnt == 5 :
                break
    Dic['Name'] = mystr(html_it.xpath('//strong[1][@itemprop="name"]/a[1]/text()')[0])
    Dic['Description'] = mystr(html_it.xpath('//p[1][@class="f4 mt-3"]/text()')[0])
    Dic['License'] = ""
    if html_it.xpath('//a[1][@class="Link--muted"]') != []:
        Dic['License'] = mystr(html_it.xpath('//a[1][@class="Link--muted"]/text()')[1])
    Lan = {}
    List_Lan = html_it.xpath('//span[@class="color-fg-default text-bold mr-1"]/text()')
    List_pro = html_it.xpath('//span[@class="color-fg-default text-bold mr-1"]/following-sibling::*/text()')
    cnt_i = 0
    for i in List_Lan:
        Lan[mystr(i)] = mystr(List_pro[cnt_i])
        cnt_i = cnt_i + 1
    Dic['Language'] = Lan
    Dic["Issue"] = I
    Data.append(Dic)
    break

Output = json.dumps(Data, indent =1)
fo = open('Level2.json', 'w')
fo.write(Output)
