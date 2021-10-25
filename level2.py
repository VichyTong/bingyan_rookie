import requests

r = requests.get('https://github.com/orgs/apache/repositories')

print(r.text)