import requests

login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'

data = dict(
    username='xxx111',
    userpass='123456',
    login='Sign in',
)

r = None


def logIn():
    r = requests.post(login_url, data)


def main():
    logIn()


if __name__ == '__main__':
    main()
