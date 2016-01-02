import  base64

def UTF8StrToBase64Str(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def Base64StrToUTF8Str(string):
    return base64.b64decode(string).decode('utf-8')


if __name__=='__main__':
    str = '你好世界!!'
    str1 = UTF8StrToBase64Str(str)
    print(str1)
    str2 = Base64StrToUTF8Str(str1)
    print(str2)
