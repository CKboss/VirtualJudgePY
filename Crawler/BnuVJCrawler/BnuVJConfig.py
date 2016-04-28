import requests

BnuVJ_LogIn_Url = 'https://www.bnuoj.com/v3/ajax/login.php'

BnuVJUser = [
    dict(
        username='JiangOil',
        password='rgbitfkfm',
        cksave='1',
        login='Login',
    ),
]

BnuVJCookies = [
   'bnuoj_v3_username=JiangOil; expires=Fri, 28-Apr-2017 01:44:11 GMT; Max-Age=31536000; path=/v3' ,
   'bnuoj_v3_password=04a49181da1ddb9967dc81122c191e6c36fbaf0a; expires=Fri, 28-Apr-2017 01:44:11 GMT; Max-Age=31536000; path=/v3',
]


def getCookies():
    cookies = dict()
    for string in BnuVJCookies :
        ls = string.split('; ')
        for s in ls :
            key,value = s.split('=')
            cookies[key]=value
    return cookies

def main():
    cokie = getCookies()
    print(cokie)

if __name__=='__main__' :
    main()

