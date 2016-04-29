import base64
import hashlib,binascii,uuid


def UTF8StrToBase64Str(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')


def Base64StrToUTF8Str(string):
    return base64.b64decode(string).decode('utf-8')

salt = 'stTX3ad9R6a2d9kzXYERwsp4F5FNVUw0tLJzjdwj8J=A'
loop = 2384

def SHA512(string):
     dk = hashlib.pbkdf2_hmac('sha512',string.encode('utf-8'),salt.encode('utf-8'),loop)
     return binascii.hexlify(dk).decode()

if __name__ == '__main__':
    '''
    str = '你好世界!!'
    str1 = UTF8StrToBase64Str(str)
    print(str1)
    str2 = Base64StrToUTF8Str(str1)
    '''
    #print(base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes))
    print(SHA512('test2@123456'))

