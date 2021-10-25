import requests
from lxml import etree
import os
import json
import re
from requests.api import head

from requests.models import Response

os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

login_url  = 'https://github.com/login'
user = 'tastmytask'
password = 'Tongweixi2003'
user_headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'zh-CN,zh;q=0.9'
}

session = requests.Session()
response = session.get(login_url, headers=user_headers)
html = etree.HTML(response.text)
authenticity_token = html.xpath("//*[@name='authenticity_token']/@value")

login_data = {    
    'commit' : 'Sign in',    
    'utf8' : '%E2%9C%93',    
    'authenticity_token' : authenticity_token,
    'login' : user,    
    'password' : password
}

session_url = 'https://github.com/session'
response = session.post(session_url, headers = user_headers, data = login_data)

def Addstar():
    response = session.get("https://github.com/orgs/apache/repositories", headers=user_headers)
    html = etree.HTML(response.text)
    domain_list = html.xpath('//a[@itemprop="name codeRepository"]/@href')
    for it in domain_list:
        domain = "https://github.com" + it
        Nr = session.get(domain, headers=user_headers)
        Nhtml = etree.HTML(Nr.text)
        token = Nhtml.xpath('//form[@class="unstarred js-social-form"]/input[@type="hidden"]/@value')[0]
        Data = {
            'authenticity_token' : token,
            'context' : 'repository'
        }
        url = domain + '/star'
        response = session.post(url, headers = user_headers, data = Data)
        print(response)

Addstar()
