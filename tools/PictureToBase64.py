import base64
import requests

def PictureToBase64(File = None,Url = None):
    if File is not None:
        filestream = open(File,'rb').read()
    elif Url is not None:
        r = requests.get(Url)
        if r.status_code==200:
            filestream = r.content
        else: return None
    else : return None

    b64 = base64.b64encode(filestream).decode()
    #imgsrc = '<img src="data:image/gif;base64,{}">'.format(b64)
    imgsrc = 'data:image/gif;base64,{}'.format(b64)
    return imgsrc


def test1():
    f = open('0.jpg','rb')
    url = 'http://ss.bdimg.com/static/superman/img/logo/bd_logo1_31bdc765.png'
    #img = PictureToBase64(File='0.jpg')
    img = PictureToBase64(Url=url)
    print(img)

def test3():
    url = 'http://ss.bdimg.com/static/superman/img/logo/bd_logo1_31bdc765.png'
    r = requests.get(url)
    img = PictureToBase64(r.content)
    print(img)

if __name__=='__main__':
    #test1()
    #test2()
    test1()

