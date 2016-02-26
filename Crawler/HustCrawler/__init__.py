import requests

data = dict(
    username='w750636248',
    password='123852',
)

problemdata = {
    'language': '0',
    'isOpen': '0',
    'source': 'I2luY2x1ZGUgPGlvc3RyZWFtPgoKdXNpbmcgbmFtZXNwYWNlIHN0ZDsKCmludCBtYWluKCkKewppbnQgYSxiOwp3aGlsZShjaW4+PmE+PmIpCnsKY291dDw8YStiPDxlbmRsOwp9CnJldHVybiAwOwp9',
    'id': '11524',
}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

print('login ....')
r = requests.post('http://acm.hust.edu.cn/vjudge/user/login.action', data=data, headers=headers)
f = open('/tmp/test.html', 'w')
f.write(r.text)
print(r.text)

for cookie in r.cookies:
    print(cookie)

print('submit....')
r = requests.post('http://acm.hust.edu.cn/vjudge/problem/submit.action', data=problemdata, allow_redirects=False)
print(r.status_code)
f = open('/tmp/test2.html', 'w')
f.write(r.text)
